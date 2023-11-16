
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
    print([123] + [12354])