##conversation begin
* greet
    - utter_what_is_name
* my_name_is
    - action_greet_user
* affirm
    - utter_we_can_talk_about_topics
* decide_topic
    - action_decide_topic
> check_which_topic


## check_ready_to_begin -> no
* greet
    - utter_what_is_name
* my_name_is
    - action_greet_user
* deny
    - utter_too_bad
    - utter_bye

## topic_check -> movies
> check_which_topic
* movie_name_action
    - utter_movie_old
* movie_old OR affirm
    - utter_movie_about
* out_of_scope OR deny OR affirm
    - utter_movie_follow_up
* out_of_scope OR deny OR affirm
    - utter_movie_end
* out_of_scope OR deny OR affirm
    - utter_bye
    
## topic_check -> sports
> check_which_topic
* sports
    - utter_sport_continue