#/bin/python

def test(a, name=None, **argv):
    print a
    print argv
    print name

test('11')
test('22', key="key", k2="k2")
test("33", name="name")
