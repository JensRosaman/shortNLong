import requests
import random

class Agent:
    """ serves as the template to create other agent classes of"""

    def __init__(self, agentID: int) -> None:
        self.agentID = agentID

    def __hash__(self) -> int:
        return self.agentID

    def __repr__(self) -> str:
        return str(self.agentID)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.agentID == other.agentID
        return False

    def request_declare(self, state: dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        pass

    def request_card2Play(self, state: dict) -> int:
        "Asks for the index of the card to play -> index int of played card"
        pass

    def request_take_discard(self, state: dict) -> bool:
        """Gets state of the game and returns ans"""

    def request_lay_cards(self):
        """Requests an action asking what player to lay a card to"""



class ConsoleAgent:
    """Agent that takes input from the command line"""
    def __init__(self, agentID: int) -> None:
        self.human = True
        self.agentID = agentID
        self.isHuman = True

    def __hash__(self) -> int:
        return self.agentID

    def __repr__(self) -> str:
        return f"HumanAgent({self.agentID})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Agent):
            return self.agentID == other.agentID
        return False

    # -------------------- Agent requests
    def request_declare(self, state: dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        print(state)
        ans = input(f"u wnna declare your cards? y/n p{self.agentID}")
        if ans:
            return True
        else:
            return False

    def request_card2Play(self, state: dict) -> int:
        "Asks for the index of the card to play -> index int of played card"
        print(f"State: {state}")
        ans = input(f"{self.agentID} Vilket kort vill du lägga (skriv index) {state['hand']}")
        return int(ans)

    def request_take_discard(self, state: dict) -> bool:
        """Gets state of the game and returns ans"""

        if self.isHuman:
            print(f"Current state is {state}")
            ans = input(f"{self.agentID}Ta kortet från discard? any key for yes")
            if ans:
                return True



class GuiAgent:
    """ serves as the template to create other agent classes of"""

    def __init__(self, agentID: int, apiUrl = "http://192.168.0.17:5000/") -> None:
        self.agentID = agentID
        self.url = apiUrl + 'request_agent'
        self.guiAgent = True # game checks for guiAgent in __dict__

    def __hash__(self) -> int:
        return self.agentID

    def __repr__(self) -> str:
        return str(self.agentID)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.agentID == other.agentID
        return False

    def _return_bool(self, data):
        """Extracts the bool from the response and returns the converted answer"""
        return {"yes":True,"no":False}[data["response"]]

    def _return_int(self,data):
        """Extracts the int from the data and returns the int"""
        return int(data["response"])

    def request_declare(self, state: dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        response = self._return_bool(self.post_request(data={"agentID": self.agentID, "request":"declare"}))
        return response

    def request_card2Play(self, state: dict) -> int:
        """Asks for the index of the card to play -> index int of played card
        pass"""
        ans = self._return_int(self.post_request(data={"agentID":self.agentID, "request":"card2Play"}))
        return ans

    def request_take_discard(self, state: dict) -> bool:
        """Gets state of the game and returns ans"""
        response = self._return_bool(self.post_request(data={"agentID":self.agentID, "request":"take_discard"}))
        return response

    def request_lay_cards(self):
        """Requests an action asking what player to lay a card to"""
        response = self._return_int(self.post_request(data={"agentID":self.agentID, "request":"lay_cards"}))

        return response
    def post_request(self, data):
        print(f"{self.agentID}: sending a request to the front end {data}")
        return (requests.post(url=self.url, json=data)).json()



class randAgent:
    """ serves as the template to create other agent classes of"""

    def __init__(self, agentID: int) -> None:
        self.agentID = agentID

    def __hash__(self) -> int:
        return self.agentID

    def __repr__(self) -> str:
        return str(self.agentID)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.agentID == other.agentID
        return False

    def request_declare(self, state: dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        return True

    def request_card2Play(self, state: dict) -> int:
        "Asks for the index of the card to play -> index int of played card"
        cardAmount = len(state["hand"])
        return random.randint(0,cardAmount - 1)

    def request_take_discard(self, state: dict) -> bool:
        """Gets state of the game and returns ans"""
        return bool(random.randint(0, 1))

    def request_lay_cards(self,state):
        """Requests an action asking what player to lay a card to"""
        availableToLayTo = state["availableToLayTo"]
        chosenAgent = random.choice(list(availableToLayTo))
        if len(availableToLayTo[chosenAgent]["runs"]) > 0 and len(availableToLayTo[chosenAgent]["sets"]) > 0:
            layToRun = bool(random.randint(0,1))
        elif len(availableToLayTo[chosenAgent]["runs"]) > 0:
            layToRun = True
        else:
            layToRun = False

        # return the first card in the sets list or the runs list
        if layToRun:
            return {"layToRun": layToRun, "agentToLayTo": chosenAgent, "cardToLay": availableToLayTo[chosenAgent]["runs"][0]}
        return {"layToRun": layToRun, "agentToLayTo": chosenAgent, "cardToLay": availableToLayTo[chosenAgent]["sets"][0]}


class Mormor:
    """ serves as the template to create other agent classes of"""
    def __init__(self, agentID: int) -> None:
        self.agentID = agentID

    def __hash__(self) -> int:
        return self.agentID

    def __repr__(self) -> str:
        return str(self.agentID)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.agentID == other.agentID
        return False

    def request_declare(self, state: dict) -> bool:
        """Returns bool if the agent wants to declare their cards"""
        return True


    def request_card2Play(self, state: dict) -> int:
        "Asks for the index of the card to play -> index int of played card"
        def is_element_in_nested_list(element, nested_list):
            for sublist in nested_list:
                if isinstance(sublist, list):
                    # If the element is in the sublist (recursive call)
                    if is_element_in_nested_list(element, sublist):
                        return True
                else:
                    # If the element is in the current sublist
                    if sublist is element or sublist == element:
                        return True
            return False
        lastCard = None
        for card in state["hand"]:
            if not is_element_in_nested_list(card,state["completeSets"]) or is_element_in_nested_list(card,state["completeRuns"]):
                if card._point_value >= 10:
                    return state["hand"].index(card)
                lastCard = card
            else:
                continue

        if len(state["completeSets"]) > 0 and state["winConditions"]["runs"] is not None:
            pass
        if lastCard is None:
            return random.randint(0,len(state["hand"]) - 1)
        return state["hand"].index(lastCard)
    def request_take_discard(self, state: dict) -> bool:
        """Gets state of the game and returns ans"""
        topDiscard = state["discard"][-1]
        if self in state["declaredCards"]:
            return False
        if state["isCurrentPlayer"] and not (topDiscard._point_value >= 10):
            for card in state["hand"]:
                if state["winConditions"]["runs"] is not None:
                    if (card._rank_value < topDiscard or
                            topDiscard < card._rank_value
                        ) and topDiscard._suit_value == card._suit_value:
                        return True
                else:
                    if card._rank_value == topDiscard._rank_value:
                        return True
        else:
            return False


    def request_lay_cards(self,state):
        """Requests an action asking what player to lay a card to"""
        availableToLayTo = state["availableToLayTo"]
        chosenAgent = random.choice(list(availableToLayTo))

        if len(availableToLayTo[chosenAgent]["runs"]) > 0: # if run is available lay there
            layToRun = True
        else:
            layToRun = False

        # return the first card in the sets list or the runs list
        if layToRun:
            return {"layToRun": True, "agentToLayTo": chosenAgent,
                    "cardToLay": availableToLayTo[chosenAgent]["runs"][0]}
        return {"layToRun": False, "agentToLayTo": chosenAgent,
                "cardToLay": availableToLayTo[chosenAgent]["sets"][0]}

