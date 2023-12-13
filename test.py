import requests
class Card:
    def __init__(self, rank):
        self.rank = rank

    def __eq__(self, other):
        return True

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return str(id(self))


if __name__ == "__main__":
    g = Card(1)
    h = Card(1)
    pp = id(g)
    ppp = id(h)
    print(pp,ppp)
    lista = [g,h]
    lista.remove(h)
    print(lista)
