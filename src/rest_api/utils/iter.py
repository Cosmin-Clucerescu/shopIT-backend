class Iterator:
    def __init__(self, members):
        self.members = members
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.members):
            member = self.members[self.index]
            self.index += 1
            return member
        raise StopIteration


class IterableMeta(type):
    def __iter__(cls):
        return Iterator([getattr(cls, attr) for attr in dir(cls) if not attr.startswith("__")])


class Iterable(metaclass=IterableMeta):
    pass
