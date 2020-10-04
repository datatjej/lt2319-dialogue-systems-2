abstract time = TDM, Integers ** {

cat

Sort_alarm_time;
Sort_domain;
Sort_string;
Sort_integer;
Predicate_current_time;
Predicate_hour_to_set;
Predicate_selected_alarm_time;
Predicate_current_alarm;
Predicate_minute_to_set;
Unknown;

fun

top : VpAction;
set_time : VpAction;
set_time_request_1 : Predicate_hour_to_set -> UsrRequest;
set_time_request_2 : Predicate_hour_to_set -> Predicate_minute_to_set -> UsrRequest;
up : VpAction;
set_alarm : VpAction;
set_alarm_request_3 : Predicate_selected_alarm_time -> UsrRequest;
eight : Sort_alarm_time;
eight_thirty : Sort_alarm_time;
nine : Sort_alarm_time;
alarm_off : Sort_alarm_time;
current_time : Predicate;
current_time_resolve_ynq_4 : SysResolveGoal;
ask_current_time : UsrQuestion;
current_time_sys_answer : Placeholder -> SysAnswer;
current_time_sortal_usr_answer : Sort_string -> UsrAnswer;
current_time_propositional_usr_answer : Unknown -> Predicate_current_time;
hour_to_set : Predicate;
hour_to_set_sys_answer_small : Integer -> SysAnswer;
hour_to_set_sys_answer_large : Placeholder -> SysAnswer;
hour_to_set_propositional_usr_answer : Integer -> Predicate_hour_to_set;
hour_to_set_sortal_usr_answer : Integer -> UsrAnswer;
selected_alarm_time : Predicate;
selected_alarm_time_sys_answer : Sort_alarm_time -> SysAnswer;
selected_alarm_time_sortal_usr_answer : Sort_alarm_time -> UsrAnswer;
selected_alarm_time_propositional_usr_answer : Sort_alarm_time -> Predicate_selected_alarm_time;
alarm_time_user_answer : Sort_alarm_time -> UsrAnswer;
alarm_time_individual : Sort_alarm_time -> Individual;
current_alarm : Predicate;
current_alarm_resolve_ynq_5 : SysResolveGoal;
ask_current_alarm : UsrQuestion;
current_alarm_sys_answer : Sort_alarm_time -> SysAnswer;
current_alarm_sortal_usr_answer : Sort_alarm_time -> UsrAnswer;
current_alarm_propositional_usr_answer : Sort_alarm_time -> Predicate_current_alarm;
alarm_time_user_answer : Sort_alarm_time -> UsrAnswer;
alarm_time_individual : Sort_alarm_time -> Individual;
minute_to_set : Predicate;
minute_to_set_sys_answer_small : Integer -> SysAnswer;
minute_to_set_sys_answer_large : Placeholder -> SysAnswer;
minute_to_set_propositional_usr_answer : Integer -> Predicate_minute_to_set;
minute_to_set_sortal_usr_answer : Integer -> UsrAnswer;
mkUnknown : String -> Unknown;
unknown_string : Unknown -> Sort_string;
report_ended_SetTime_6 : SysAnswer -> SysAnswer -> SysReportEnded;
report_failed_SetTime_undefined_failure_7 : SysAnswer -> SysAnswer -> SysReportFailed;
report_ended_SetAlarm_8 : SysAnswer -> SysReportEnded;
report_failed_SetAlarm_undefined_failure_9 : SysAnswer -> SysReportFailed;
}
