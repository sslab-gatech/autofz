from abc import ABCMeta, abstractmethod


class Controller(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def scale(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def stop(self):
        pass
