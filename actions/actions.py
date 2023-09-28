from typing import Any, Coroutine, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, AllSlotsReset, UserUtteranceReverted, FollowupAction
from word2number import w2n
import random
import json
from .functions import resetStates

filePath = './mockdata.json'

filter_list = [
    "type",
    "tag",
    "price",
    "color"
]

stateDict = {
    'action_name': None,
    'video_link': None,
    'entities': {
        "type": None,
        "color": None,
        "tag" : None,
        "price" : None,
        "size" : None,
        "page" : None,
        "product" : None   
    }
}

resetStates(stateDict)


def createDict(action, video_link, entities_type=None, entities_color=None,
                             entities_tag=None, entities_price=None, entities_size=None,
                             entities_page=None, entities_sale=None, entities_product=None):
    dict = {
        'action_name': action,
        'video_link': video_link,
        'entities': {
            'type': entities_type,
            'color': entities_color,
            'tag': entities_tag,
            'price': entities_price,
            'size': entities_size,
            'page': entities_page,
            'product': entities_product
        }
    }
    
    return dict

class ActionShowEntities(Action):
    def name(self) -> Text:
        return "action_show_entities"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Extract the 'color' and 'size' entities from the latest message
        color = tracker.get_slot("color")
        size = tracker.get_slot("size")
        item = tracker.get_slot("page")
        price = tracker.get_slot("price")
        tag = tracker.get_slot("tag")
        product = tracker.get_slot("name")

        # Format a response string
        dataSend = {
            "action_name": "open-item",
            "video_link": "/general-2.mp4",
            "entities": {
                "type": item,
                "color": color,
                "tag": tag,
                "price": price,
                "size": size,
                "page": None,
                "sale": None,
                "product": product,
            },
        }

        # Send the response
        dispatcher.utter_message(json_message=dataSend)

        return []


class ApplyFilter(Action):
    def name(self) -> Text:
        return "action_filter"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        global stateDict
        
        stateDict["action_name"] = 'search'

        slots = tracker.current_slot_values()
        for key, value in slots.items():
            if key in stateDict['entities']:
                stateDict['entities'][key] = value
        
        # Send the response
        randomVids = [
            {'text': "All set on my end! Whenever you're ready, just give me a shout if you have questions!", 'video': '/Template_12.mp4'},
            {'text': "Got it all set for you! Take your time and feel free to ask any questions!", 'video': '/Template_13.mp4'}
        ]
        choice = random.choice(randomVids)
        textVal = choice['text']
        stateDict['video_link'] = choice['video']
        dispatcher.utter_message(textVal)
        dispatcher.utter_message(json_message=stateDict)

        return []


class OpenItem(Action):
    def name(self) -> Text:
        return "action_open_item"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        global stateDict
        
        stateDict["action_name"] = 'open-item'
        slots = tracker.current_slot_values()
        
        # Extract the slots entities from the latest message
        for key, value in slots.items():
            if key in stateDict['entities']:
                stateDict['entities'][key] = value
        
        # Send the response
        randomVids = [
            {'text': "Item accessed! What's the next step you'd like to take?", 'video': '/item_open_1.mp4'},
            {'text': "Item's open! Ready for the next move?", 'video': '/item_open_2.mp4'},
            {'text': "Item opened! What would you like to do with it now?", 'video': '/open_item.mp4'}
        ]
        choice = random.choice(randomVids)
        textVal = choice['text']
        stateDict['video_link'] = choice['video']
        dispatcher.utter_message(textVal)
        dispatcher.utter_message(json_message=stateDict)

        return []

class ChangeItemColor(Action):
    def name(self) -> Text:
        return "action_item_color"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        global stateDict
        stateDict["action_name"] = 'open-item'
        
        # Extract the slots entities from the latest message
        slots = tracker.current_slot_values()
        for key, value in slots.items():
            if key in stateDict['entities']:
                stateDict['entities'][key] = value

        # Send the response
        randomVids = [
            {'text': "Color changed! What do you think of the new look?", 'video': '/color_change_1.mp4'},
            {'text': "Voila! New colors are in play. Do you like the vibe?", 'video': '/color_change_2.mp4'},
            {'text': "Color switched! How's it looking now?", 'video': '/item_color.mp4'}
        ]
        choice = random.choice(randomVids)
        textVal = choice['text']
        stateDict["video_link"] = choice['video']
        dispatcher.utter_message(textVal)
        dispatcher.utter_message(json_message=stateDict)

        return []


class AddToCart(Action):
    def name(self) -> Text:
        return "action_add_cart"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        
        # Extract the 'color' and 'size' entities from the latest message
        product = tracker.get_slot("product")
        color = tracker.get_slot("color")
        size = tracker.get_slot("size")
        cartList = tracker.get_slot('cartList') or []
        
        checkProduct = 1
        
        randomVids = [
            {'text': "Done and done! Your selected shoes are safely in your cart. Need anything else?", 'video': '/Template_2.mp4'},
            {'text': "Perfect! The shoes you picked are in your cart. Want to explore more items?", 'video': '/Template_3.mp4'},
            {'text': "Awesome! I've just popped the shoes you picked into your cart for you. Anything else you'd like to explore?", 'video': '/action_add_cart.mp4'}
        ]
        choice = random.choice(randomVids)
        textVal = choice['text']
        videoVal = choice['video']
        
        if (checkProduct == 1):
            showDict = createDict('add-item', videoVal, entities_color=color, entities_size=size, entities_product=product)
            cartList.append(product)
            dispatcher.utter_message(textVal)
            dispatcher.utter_message(json_message=showDict)
            resetStates(stateDict)
            return [SlotSet("color", None),SlotSet("size", None),SlotSet("product", None), SlotSet('price', None), SlotSet('tag', None) , SlotSet('cartList', cartList)]
        else:
            showDict = createDict('no-action', '/negative-3.mp4')
            dispatcher.utter_message("Please repeat your selection")
            dispatcher.utter_message(json_message=showDict)
            return [UserUtteranceReverted()]

class PageChange(Action):
    def name(self) -> Text:
        return "action_page_change"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        global stateDict
        stateDict["action_name"] = 'navigation'
        
        # Extract the slots entities from the latest message
        slots = tracker.current_slot_values()
        for key, value in slots.items():
            if key in stateDict['entities']:
                stateDict['entities'][key] = value
        
        
        # Send the response
        randomVids = [
            {'text': "There you have it! Anything else you fancy? I am here to help", 'video': '/utter_happy_updated.mp4'},
            {'text': "Is there anything else you'd like to know? I'm all ears!", 'video': '/page_change_1.mp4'},
            {'text': "Anything more you're curious about? Just give me a shout, I'm here to help!", 'video': '/page_change_2.mp4'}
        ]
        choice = random.choice(randomVids)
        textVal = choice['text']
        stateDict['video_link'] = choice['video']
        dispatcher.utter_message(textVal)
        dispatcher.utter_message(json_message=stateDict)

        return [SlotSet("color", None), SlotSet("price", None), SlotSet('tag', None)]

class RemoveFilter(Action):
    def name(self) -> Text:
        return "action_remove_filter"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        global stateDict        

        filter_slot = tracker.get_slot("filter")
        # Extract the slots entities from the latest message
        type = tracker.get_slot('type')
        color = tracker.get_slot('color')
        tag = tracker.get_slot('tag')
        price = tracker.get_slot('price')
        
        filter_dict = createDict("remove-filter", "/okay-1.mp4", entities_color=color, entities_price=price, entities_type=type, entities_tag=tag)
        
        if (filter_slot is None):
            dataSend = createDict('remove-filter', '/utter_happy_updated.mp4', entities_color=None, entities_tag=None, entities_price=None)
            dispatcher.utter_message("Filters are off! What's next on your list?")
            dispatcher.utter_message(json_message=dataSend)
            resetStates(stateDict)
            return [AllSlotsReset()]
        elif (filter_slot in filter_list):
            filter_dict['entities'][filter_slot] = None
            dispatcher.utter_message("Okay!")
            dispatcher.utter_message(json_message=filter_dict)
            return [SlotSet(filter_slot, None), SlotSet('filter', None)]
        else:
            return [FollowupAction('action_default_fallback')]
        
    
class ActionRemove(Action):
    def name(self) -> Text:
        return "action_remove"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        slot_item = tracker.get_slot("index")
        cartList = tracker.get_slot("cartList")
                
        if (slot_item is None):
            showDict = createDict('remove-cart-all', '/cart-1.mp4')
            dispatcher.utter_message("Clearing your cart")
            dispatcher.utter_message(json_message=showDict)
            return [SlotSet('index', None), SlotSet('cartList', None)]
        
        numberMap = {
            "first": 1,
            "1st": 1,
            "one": 1,
            "second": 2,
            "2nd": 2,
            "two": 2,
            "third": 3,
            "3rd": 3,
            "three": 3,
            "fourth": 4,
            "4th": 4,
            "four": 4,
            "fifth": 5,
            "5th": 5,
            "five": 5,
            "sixth": 6,
            "6th": 6,
            "six": 6,
            "seventh": 7,
            "7th": 7,
            "seven": 7,
            "eighth": 8,
            "8th": 8,
            "eight": 8,
            "ninth": 9,
            "9th": 9,
            "nine": 9,
            "tenth": 10,
            "10th": 10,
            "ten": 10
        }        
        position = numberMap.get(slot_item.lower(), None)
                
        if position is None:
            try:
                position = w2n.word_to_num(slot_item)
            except ValueError as e:
                print(f"Error in conversion: {e}")
                dispatcher.utter_message("CAN NOT")
                return []
            
        if position <= len(cartList):
            show_dict = createDict("remove-cart-index", "/remove-cart1.mp4", entities_product=position)
            dispatcher.utter_message("Okay, I'm Removing It from Your Cart")
            dispatcher.utter_message(json_message=show_dict)
            del cartList[position - 1]
            return [SlotSet("index", None), SlotSet('cartList', cartList)]
        else:
            dispatcher.utter_message("Not in the cart")
            return []
        
class DefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        
        toSend = createDict('no-action', '/utter_confusion.mp4')
        dispatcher.utter_message('Oops, my bad! What can I do for you next? Lets get things sorted.')
        dispatcher.utter_message(json_message=toSend)
        
        return [UserUtteranceReverted()]