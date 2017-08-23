def Dict1():
    return {'key1': 'value1'}
def Dict2():
    return {'key2': 'value1'}
# print(Dict1().update(Dict2())) # None
d = Dict1()
d.update(Dict2())
print(d)
