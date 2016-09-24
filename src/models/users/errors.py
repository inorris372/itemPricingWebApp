__author__ = 'Ian'


class UserNonexistentError():
    def __init__(self, message):
        self.message = message

class IncorrectPasswordError():
    def __init__(self, message):
        self.message = message

