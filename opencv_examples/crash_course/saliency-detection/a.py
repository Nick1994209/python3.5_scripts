class List(list):
    def __hash__(self):
        return hash(tuple(self))

l = List()
print(l)
print(hash(l))