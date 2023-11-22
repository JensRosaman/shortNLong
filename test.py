import requests
class b:
    def __init__(self, kod) -> None:
        self.kod = kod

    def __repr__(self):
        return f"{self.kod}"

    def __eq__(self, other):
        if self.kod == other.kod:
            return True
        else:
            return False
if __name__ == "__main__":
    print(requests.get("http://192.168.0.17:5000/").text)