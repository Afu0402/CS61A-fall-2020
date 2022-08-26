class Insect:
    def __init__(self, armor):
        print("insect")
        self.armor = armor

    def add_armor(self, amount):
        self.armor += amount


class Ant(Insect):
    def __init__(self, name):
        print("Ant")
        Insect.__init__(self, 10)
        self.name = name


class HarvesterAnt(Ant):
    def say(self, words):
        print(words)
