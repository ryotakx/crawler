import random


class Proxy:

    def __init__(self, url_list: list):
        self.length = len(url_list)
        self.scoreboard = [[i, 10] for i in url_list]
        self.shuffle()
        self.order = 0

    def pop(self):
        self.order += 1
        return self.scoreboard[self.order - 1][0]

    def success(self):
        self.scoreboard[self.order - 1][1] += 1
        self.shuffle()
        self.order = 0

    def fail(self):
        self.scoreboard[self.order - 1][1] -= 1

    def shuffle(self):
        random.shuffle(self.scoreboard)
        self.scoreboard = [i for i in self.scoreboard if i[1] > 0]
        self.length = len(self.scoreboard)
        if self.length == 0:
            raise ValueError



