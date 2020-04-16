## conversation begin
* greet
    - utter_what_is_name
* my_name_is
    - action_greet_user
    - utter_nicetomeeyou
    - utter_are_you_ready_to_start
> check_ready_to_begin

## check_ready_to_begin -> no
> check_ready_to_begin
* deny
    - utter_too_bad
    - utter_bye

## check_ready_to_begin -> yes
> check_ready_to_begin
* affirm
    - utter_we_can_talk_about_topics
* decide_topic
    - action_decide_topic
> check_which_topic

## topic_check -> movies
> check_which_topic
* movie_name_action
    - utter_movie_continue
* out_of_scope
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

## interactive_story_1
* greet
    - utter_what_is_name
* my_name_is{"name": "Ben"}
    - slot{"name": "Ben"}
    - action_greet_user
    - utter_nicetomeeyou
    - utter_are_you_ready_to_start
* affirm
    - utter_we_can_talk_about_topics
* decide_topic{"topics": "sports"}
    - slot{"topics": "sports"}
    - action_decide_topic
* sports
    - utter_sport_continue