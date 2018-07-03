class Borg(object):
    """Python singleton, all instances have same reference for __dict__"""
    __shared_dict = {}

    def __init__(self):
        self.__dict__ = self.__shared_dict
        super().__init__()
