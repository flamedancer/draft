
class A(object):
    wwc= 'ok'
    @classmethod
    def aa(cls):
        return 'im cls'
    def __init__(self):
        print 'Iam self You are {}'.format(self.aa())

print(A.aa())
a = A()
print('a wwc', a.wwc)
print('A wwc', a.wwc)
a.wwc = 333
print('a wwc', a.wwc)
print('A wwc', a.wwc)
del a.wwc
print('a wwc', a.wwc)
print('A wwc', a.wwc)

id = 3
print('id is', id)
del id
print(id)