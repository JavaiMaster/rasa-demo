# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from typing import Any, Dict, List, Text, Union, Optional
import json
from rasa_sdk.events import FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)
import random

logger = logging.getLogger(__name__)


class ActionStoreUnknownProduct(Action):
    """Stores unknown tools people are migrating from in a slot"""

    def name(self) -> Text:
        return "action_store_unknown_product"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        # if we dont know the product the user is migrating from,
        # store his last message in a slot.
        return [SlotSet("unknown_product", tracker.latest_message.get("text"))]


class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        print("intent is ", intent)
        if intent == "my_name_is":  # or (intent == "enter_data" and name_entity):
            if name_entity and name_entity.lower() not in ["sara", "sarah", "desire"]:
                dispatcher.utter_message(template="utter_greet_name", name=name_entity)
            else:
                dispatcher.utter_message(template="utter_greet_noname")
        dispatcher.utter_message(template="utter_nicetomeeyou")
        dispatcher.utter_message(template="utter_are_you_ready_to_start")
        return []


class ActionDecideTopic(Action):
    """Greets the user with/without privacy policy"""

    def name(self) -> Text:
        return "action_decide_topic"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")
        topic_name = next(tracker.get_latest_entity_values("topics"), None)
        print("intent is ", intent)
        if intent == "decide_topic":
            print("topic is ", topic_name)
            if topic_name == "movies":
                dispatcher.utter_message(template="utter_talk_movies")
                dispatcher.utter_message(template="utter_movie_start")
                return []
            elif topic_name == "sports":
                dispatcher.utter_message(template="utter_talk_sports")
                dispatcher.utter_message(template="utter_sport_start")
                return []
            elif topic_name == "traveling":
                dispatcher.utter_message(template="utter_talk_traveling")
                dispatcher.utter_message(template="utter_traveling_start")
                return []
            elif topic_name == "space":
                dispatcher.utter_message(template="utter_talk_space")
                dispatcher.utter_message(template="utter_space_start")
                return []
            elif topic_name is None:
                dispatcher.utter_message(template="utter_talk_other")
                topic_choose = random.choice(["movies", "sports", "traveling", "space"])
                return [SlotSet("topics", topic_choose), FollowupAction('utter_talk_other_continue'),
                        FollowupAction("utter_talk_{}".format(topic_choose))]

        return []


class ActionUserResponse(Action):
    """Stores the problem description in a slot."""

    def name(self) -> Text:
        return "action_user_response"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        problem = tracker.latest_message.get("text")

        return [SlotSet("user_response", problem)]
