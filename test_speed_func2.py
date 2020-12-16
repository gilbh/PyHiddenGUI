import datetime

alist = [str(x) for x in range(10000000)]

print("Using map.")
a = datetime.datetime.now()
result = list(map(len, alist))
b = datetime.datetime.now()
print((b-a).total_seconds(), '\n')

print("List comprehension.")
a = datetime.datetime.now()
result = [len(i) for i in alist]
b = datetime.datetime.now()
print((b-a).total_seconds(), '\n')
