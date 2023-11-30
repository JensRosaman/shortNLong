import requests
class GuiAgent:
    """ serves as the template to create other agent classes of"""

    def __init__(self, agentID: int, apiUrl = "http://192.168.0.17:5000/") -> None:
        self.agentID = agentID
        self.url = apiUrl + 'request_agent'
        guiAgent = True # game checks for guiAgent in __dict__

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
        response = self.post_request(data={"agentID":self.agentID, "request":"request_declare"})
        if response.ok:
            return bool(response.text["bool"])


    def request_card2Play(self, state: dict) -> int:
        """Asks for the index of the card to play -> index int of played card
        pass"""
        response = self.post_request(data={"agentID":self.agentID, "request":"request_card2Play"})


    def request_take_discard(self, state: dict) -> bool:
        """Gets state of the game and returns ans"""
        response = self.post_request(data={"agentID":self.agentID, "request":"request_take_discard"})

    def post_request(self, payLoad):
        return requests.post(url=self.url, data=payLoad)




f = GuiAgent(1,"")
print(f.__dict__)