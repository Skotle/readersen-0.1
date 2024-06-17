class CustomClass:
    def __init__(self, name):
        self.name = name
        self.num = 1
        self.view = 0
        self.recom = 0
        self.reple = 0

    def add_member(self, view, recom, reple):
        self.num += 1
        self.recom += recom
        self.view += view
        self.reple += reple
