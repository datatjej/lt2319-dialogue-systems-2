### Requirements

They are already installed in eduserv and the lab computers, but in case you want to work in your own computer we leave them here. All of them are console-based and we can confirm that they work in Linux and Mac (Unix) consoles. 
We don't know about Windows, but we guess if you use WSL you shouldn't have any issue as in that case you're in fact running a Linux console.
- Tala (`pip install tala`). NOTE: Tala works with python 3.7! It should work with newer versions as well, but we cannot assure it.
- Okteto CLI (https://okteto.com/docs/getting-started/installation)
- Kubectl (https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- ONLY for MacOS users: libmagic (`brew install libmagic`).


### Intro

For testing and interacting with your dialogue applications you will use a remote Kubernetes cluster which is running in "eduserv". You will develop your DDDs in your local machine and sync your local files with your namespace in the remote cluster. Sounds like a lot of stuff that you may never heard about before. But don't worry, this document will guide you along your way there!


### Setting up access to the remote Kubernetes cluster

You may need to follow the following steps only once (we cannot assure it though).

1. Log into to "eduserv" via SSH. In order to access the Kubernetes cluster from your machine, you need to tunnel the port 16443 to your localhost (aka 127.0.0.1).
`$ ssh -p 62266 -Y -L 16443:127.0.0.1:16443 guserbto@eduserv.flov.gu.se`
You just need to start this session and let it run on the background. Run the rest of the steps in your own machine as the requirements specified above are not installed in the eduserv.

2. Download the "microk8s-eduserv.config" file, which you can find in the Lab 2 instructions and in the "Filer" section in Canvas. Rename it to just "config".

3. Ok, I have just seen that installing "kubectl" doesn't create the kube config file a lot of times ("~/.kube/config). If you don't have it, you can create it manually: 
  - `mkdir ~/.kube`
  - Copy and paste the "config" file inside the ".kube" folder that you just created. 

4. In Kubectl, you have to select the "microk8s-eduserv" context to connect it to the Kubernetes cluster.
`$ kubectl config use-context microk8s-eduserv`

5. Each of you has a namespace in the Kubernetes cluster (called "gusXXXXXX"). Such namespace contains all the different components necessary to run your dialogue applications in it. To access your namespace:
`$ kubectl config set-context microk8s-eduserv --namespace=gusXXXXXX`


### Preparing Rasa for training models

You need to do this only once.

1. Log into "mltgpu" via SSH.
`$ ssh -p 62266 -Y -L 5010:127.0.0.1:5010 gusXXXXXX@mltgpu.flov.gu.se`

2. In the mltgpu, you need to install rasa (1.10.14) and tensorflow-text (2.1.1) via pip
pip install --user rasa==1.10.14 tensorflow-text==2.1.1


### Training Rasa models

1. We need to generate data to train a Rasa model based on what you have in your "grammar_eng.xml" file. 
In your console of your local machine go into the "call_john_2020/ddds/call_john/" directory (the one that contains "backend.config.json") and run:
`$ tala generate rasa weather eng > ../../rasa-nlu/rasa_training_data.md`
This will create the "rasa_training_data.md" file, which contains the intents and entries. The file will be in the "call_john_2020/rasa-nlu/" directory.

2. Log into to "mltgpu" via SSH. However, you need to tunnel a port to your localhost. This is the port that you will use to train your rasa model. For instance, let's take the port 5010:
ssh -p 62266 -Y -L 5010:127.0.0.1:5010 guserbto@mltgpu.flov.gu.se

3. Then inside "mltgpu" run the following to start a Rasa server (see that the port is 5010 again):
rasa run --enable-api -vv -p 5010

4. In your local machine go to the "call_john_2020/rasa-nlu/" directory and run the "train.py" script with the following arguments:
  -t TRAINING_DATA, --training-data TRAINING_DATA
                        path to the file that contains markdown training data
  -c CONFIG, --config CONFIG
                        path to the file that contains YAML config
  -u URL, --url URL     URL to Rasa server
Then, for instance:
python train.py -t rasa_training_data.md -c config.yml -u http://127.0.0.1:5010/model/train
This script trains a model with your data in the Rasa server and download it to your local machine when it's done (again, see that we are using port 5010).

5. When the training is done you can just stop the Rasa server (ctrl+C) and close your SSH to mltgpu.


### Syncing your local files to the Kubernetes cluster with Okteto

1. Log into "eduserv" via SSH.
`$ ssh -p 62266 -Y -L 16443:127.0.0.1:16443 gusXXXXXX@eduserv.flov.gu.se`
You just need to start this ssh session and let it run on the background. Run the rest of the steps in your own machine as the requirements specified above are not installed in the eduserv.

2. To be able to test and interact with your dialogue apps running in the Kubernetes cluster, you need to sync your local files using Okteto in three different command consoles. Each of these Okteto instances will sync the files specified below with three deployments that run each different parts of your code:

  - Your Rasa model will be synced to the "nlu-rasa" deployment in your namespace.
    1. Go into the "call_john_2020/rasa-nlu/" folder
    2. Run in your console:
    `$ okteto up --namespace gusXXXXXX`
    This starts an Okteto session that syncs your files in that folder (except the ones specified in the ".stignore" file) with the "nlu-rasa" deployment in your namespace. It also takes care of running the rasa model, so you just need to wait it to load.
    When you see the console output `INFO     root  - Rasa server is up and running.`, then the model is loaded.
    NOTE: Don't worry about the CUDA error, it's expected (`E tensorflow/stream_executor/cuda/cuda_driver.cc:351] failed call to cuInit: UNKNOWN ERROR (303)`). It will continue loading the model after the error.
    IMPORTANT! If for some reason `okteto up` fails, which we have seen happening a bunch of times, read the note at the bottom of the file.

  - Your "http_service.py" will be synced to the "http-service" deployment in your namespace.
    1. Go into the "call_john_2020/ddds/call_john/" folder
    2. Run in your console:
    `$ okteto up -f okteto-http-service.yml --namespace gusXXXXXX`
    This starts an Okteto session that syncs your files in that folder (except the ones specified in the ".stignore" file) with the "http-service" deployment in your namespace. It also takes care of running the http-service, so you just need to wait it to load.
    When you see 3 console outputs containing `[INFO] Booting worker with pid:`, then it's loaded.
    If you change something in your http_service.py you don't need to worry, it will reload the file with the new changes automatically.
    IMPORTANT! If for some reason `okteto up` fails, which we have seen happening a bunch of times, read the note at the bottom of the file.

  - Your DDD files will be synced to the "tdm" deployment in your namespace.
    1. Go into the "call_john_2020/ddds/call_john/" folder
    2. Run in your console:
    `$ okteto up --namespace gusXXXXXX`
    This starts an Okteto session that syncs your files in that folder (except the ones specified in the ".stignore" file) with the "tdm" deployment in your namespace.
    IMPORTANT! If for some reason `okteto up` fails, which we have seen happening a bunch of times, read the note at the bottom of the file.
    3. When the syncing has finished, you will be in a command console inside the deployment with which you're synced. There you have to use the TDM library to build and serve your DDD so you can test and interact with it.
    ```
    $ tdm build
    $ tdm serve eng --log-to-stdout
    ```
    You will see that the last command generated the url "http://localhost:9090/interact". You don't have to open it in a browser, but you will use it for test and interact with your DDDs. You will see it further down.
    IMPORTANT: If you change something in your DDD, you need to stop (press ctrl+C) the `tdm serve` and repeat both commands!

3. In another console in your local machine, run the following command:
`$ kubectl port-forward services/pipeline 9090:80 --namespace gusXXXXXX`
This will let you interact with your served DDD accessible through the url "http://localhost:9090/interact".

FOR LAB 2
 If you want to interact and test your DDD without using NLU models, run this command instead:
 `$ kubectl port-forward services/tdm 9090:80 --namespace gusXXXXXX`
 This may be also useful for you to test Lab 3 and the project without NLU, but remember that for those ones you need to make them work with NLU.


### Test and interact with your DDDs

1. OK, you can (finally) test your DDD with Tala. For that, in another console (yes, we know, lots of them), go into "call_john_2020/ddds/call_john/" and run: 
`$ tala test http://localhost:9090/interact call_john/test/interaction_tests_eng.txt`
tala test http://localhost:9090/interact weather/test/interaction_tests_eng.txt


You can also run an individual test in the file with the argument `-t`. For instance:
`$ tala test http://localhost:9090/interact call_john/test/interaction_tests_eng.txt -t "call (incremental)"`

2. If you want to interact with your DDD via text interface, you can do it with Tala as well.
`$ tala interact http://localhost:9090/interact`

3. Once you're done and you don't want to sync your local files anymore, don't forget to exit all the cluster deployments (the three consoles in which you have `okteto up` running). To do so, stop (ctrl+C) the commands running in the deployments. This will exit the consoles running in the deployments "nlu-rasa" and "http-service". To exit the "tdm" one, press ctrl+D.
Then, when you're in your local machine run the following commands:
  - In the directory "call_john_2020/rasa-nlu/":
  `$ okteto down --namespace gusXXXXXX`
  - In the directory "call_john_2020/ddds/call_john/" run both:
  `$ okteto down -f okteto-http-service.yml --namespace gusXXXXXX`
  `$ okteto down --namespace gusXXXXXX`

NOTE: Run `okteto down` if for some reason `okteto up` fails. If it keeps failing after you've tried `down` and then `up` again about 3 times, contact José as something is surely not working.