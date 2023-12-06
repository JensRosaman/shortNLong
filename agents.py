import requests


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

    def request_lay_card(self):
        """Requests an action asking what player to lay a card to"""



class HumanAgent:
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
        response = self._return_bool(self.post_request(data={"agentID":self.agentID, "request":"declare"}))
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

    def request_lay_card(self):
        """Requests an action asking what player to lay a card to"""
        response = self._return_int(self.post_request(data={"agentID":self.agentID, "request":"lay_card"}))

        return response
    def post_request(self, data):
        print(f"{self.agentID}: sending a request to the front end {data}")
        return (requests.post(url=self.url, json=data)).json()




