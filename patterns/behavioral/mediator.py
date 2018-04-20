# coding: utf-8

"""
@author: 武明辉 
@time: 2018/4/19 14:30
"""


class IMediator:
    def __init__(self):
        self.colleagues = []

    def register(self, colleague):
        self.colleagues.append(colleague)

    def execute(self, content, num):
        raise NotImplemented


class IColleague:
    mediator = None

    def __init__(self, mediator):
        self.mediator = mediator


