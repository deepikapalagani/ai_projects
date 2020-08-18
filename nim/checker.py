def f1(a, b):
    return a+b
def f2(a, b):
    return a-b
def caller():
    li= [f1(1, 2), f2(2, 1)]
    print(li[1])
caller()
