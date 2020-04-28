##conversation begin
* greet
    - utter_what_is_name
* my_name_is
    - action_greet_user
* affirm
    - utter_we_can_talk_about_topics
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
* decide_topic{"topics": "movies"}
    - slot{"topics": "movies"}    
    - action_decide_topic
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
* decide_topic{"topics": "sports"}
    - slot{"topics": "sports"}    
    - action_decide_topic  
* sports
    - utter_sport_fav_player
* fav_player
    - utter_sport_fav_moment
* out_of_scope
    - action_user_response

## topic_check -> traveling
> check_which_topic
* decide_topic{"topics": "traveling"}
    - slot{"topics": "traveling"}
    - action_decide_topic
* traveling
    - utter_traveling_continue
* travel_somewhere
    - utter_traveling_end

## topic_check -> space
> check_which_topic
* decide_topic{"topics": "space"}
    - slot{"topics": "space"}
    - action_decide_topic
* out_of_scope
    - utter_space_zero_g
* out_of_scope
    - action_user_response
    - utter_user_response
    
## topic_check -> other
> check_which_topic
* decide_topic
    - action_decide_topic
    - utter_talk_other_continue
    - action_decide_topic

## fallback story
* out_of_scope OR did_not_understand
  - action_default_fallback