
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
    d = [b(1),b(1),b(3)]
    c = d[0]
    e = []
    e.append(d[0])
    e.append(d[1])
    e.remove(d[0])
    print(id(c),id(d[1]))