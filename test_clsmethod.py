
class A(object):
    @classmethod
    def aa(cls):
        return 'im cls'
    def __init__(self):
        print 'Iam self You are {}'.format(self.aa())

print A.aa()
a = A()
