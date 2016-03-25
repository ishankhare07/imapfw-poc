#!/usr/bin/python3
#
# https://github.com/OfflineIMAP/imapfw/wiki/sync-05
#



class Message(object):
    def __init__(self, uid=None, body=None, flags=['unread']):
        self.uid = uid
        self.body = body
        self.flags = flags

    def __repr__(self):
        return "<Message %s [%s] '%s'>"% (self.uid,
            ','.join(self.flags), self.body)


# Messages
m1 = Message(1, "1 body")
m2 = Message(2, "2 body")
m3 = Message(3, "3 body")
m4 = Message(4, "4 body")


class Messages(list):
    """Enable collections of messages the easy way."""
    pass


class LeftDriver(object):
    def __init__(self):
        self.messages = Messages([m1, m2])

    def search(self):
        return self.messages


class RightDriver(object):
    def __init__(self):
        self.messages = Messages([m1, m3])

    def search(self):
        return self.messages


class StateController(object):
    def __init__(self, driver):
        self.driver = driver

    def search(self):
        messages = self.driver.search()
        messages.append(m4)
        return messages

    def __getattr__(self, name):
        return getattr(self.driver, name)


class Engine(object):
    """The engine."""
    def __init__(self):
        self.left = LeftDriver()
        self.right = RightDriver()

    def run(self):
        # Driver will need API to work on chained controllers.
        self.right = StateController(self.right)

        leftMessages = self.left.search()
        rightMessages = self.right.search()
        print(leftMessages)
        print(rightMessages)


if __name__ == '__main__':
    engine = Engine()
    engine.run()
