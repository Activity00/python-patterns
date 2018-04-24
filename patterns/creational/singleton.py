# coding: utf-8

"""
@author: 武明辉 
@time: 2018/4/24 16:33
"""
from functools import wraps


# wrap


def singleton(cls):
    instance = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return get_instance


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Python2
# class MyClass(object):
#    __metaclass__ = Singleton

# Python3
# class MyClass(metaclass=Singleton):
#    pass


if __name__ == '__main__':
    pass
