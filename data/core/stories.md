## check_ready_to_begin -> no
* greet
    - utter_what_is_name
* my_name_is
    - action_greet_user
* deny
    - utter_too_bad
    - utter_bye

## topic_check -> movies
* greet
    - utter_what_is_name
* my_name_is
    - action_greet_user
* affirm
    - utter_we_can_talk_about_topics
* decide_topic{"topics": "movies"}
    - slot{"topics": "movies"}
    - action_decide_topic
* movie_name_action{"movie_name": "Jumanji"}
    - slot{"movie_name": "Jumanji"}
    - movie_old_form
    - form{"name": "movie_old_form"}
    - slot{"requested_slot": "movie_old"}
* form: movie_name_action
    - form: movie_old_form
    - slot{"movie_old": "Yes. It is an old movie"}
    - slot{"requested_slot": "movie_detail"}
* form: decide_topic{"movie_name": "board"}
    - slot{"movie_name": "board"}
    - form: movie_old_form
    - slot{"movie_detail": "It's about a board game that goes wild"}
    - slot{"requested_slot": "movie_philosophy"}
* form: affirm
    - form: movie_old_form
    - slot{"movie_philosophy": "Kind of. I guess"}
    - slot{"requested_slot": "movie_anything_else"}
    
    
## topic_check -> sports
* greet
    - utter_what_is_name
* my_name_is
    - action_greet_user
* affirm
    - utter_we_can_talk_about_topics
* decide_topic{"topics": "sports"}
    - slot{"topics": "sports"}    
    - action_decide_topic  
* sports
    - utter_sport_fav_player
* fav_player
    - utter_sport_fav_moment
* out_of_scope
    - action_user_response