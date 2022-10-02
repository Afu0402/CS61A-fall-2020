class Insect:
    def __init__(self, name) -> None:
        print("call Insect constructor")
        self.name = name

    def getName(self):
        return self.name


class Ant(Insect):
    def getAntName(self):
        return self.name + "-Ant"
