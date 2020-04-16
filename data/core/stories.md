## movie flow begin
* greet
    - action_greet_user
* next_step
    - utter_movie_start
> check_movie_response

## movie flow 1
> check_movie_response
* movie_name_action
    - utter_movie_continue
* out_of_scope OR movies
    - utter_movie_about
* out_of_scope OR movies OR ask_howold OR deny OR affirm OR react_negative OR react_positive
    - utter_movie_follow_up
* out_of_scope OR movies OR ask_howold OR deny OR affirm OR react_negative OR react_positive
    - utter_movie_end
* out_of_scope OR movies OR ask_howold OR deny OR affirm OR react_negative OR react_positive
    - utter_thank_suggestion
    - utter_bye
    
## movie flow 2
> check_movie_response
* movies
    - utter_too_bad
* affirm
    - utter_bye

