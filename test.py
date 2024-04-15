def f(lst=[]):
    lst = lst or []
    lst.append(1)
    print(lst)

f()
f()
