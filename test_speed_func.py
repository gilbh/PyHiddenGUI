import datetime 

def pp(s, cnt=[0]):
    cnt[0] += 1
    print(f"{cnt[0]}: {s}")

alist = [str(x) for x in range(10000000)]
pp("Standard loop.") 
a = datetime.datetime.now() 
result = [] 
for item in alist: 
    result.append(len(item)) 
b = datetime.datetime.now() 
print((b-a).total_seconds(), '\n') 
pp("Standard loop with function name in local namespace.") 
a = datetime.datetime.now() 
result = [] 
fn = len 
for item in alist:
    result.append(fn(item))
b = datetime.datetime.now()
print((b-a).total_seconds(), '\n')
pp("Using map.")
a = datetime.datetime.now()
result = list(map(len, alist))
b = datetime.datetime.now()
print((b-a).total_seconds(), '\n')
pp("Using map with function name in local namespace.")
a = datetime.datetime.now() 
fn = len 
result = list(map(fn, alist)) 
b = datetime.datetime.now() 
print((b-a).total_seconds(), '\n') 
pp("List comprehension.") 
a = datetime.datetime.now() 
result = [len(i) for i in alist] 
b = datetime.datetime.now() 
print((b-a).total_seconds(), '\n') 
pp("List comprehension with name in local namespace.") 
a = datetime.datetime.now() 
fn = len 
result = [fn(i) for i in alist] 
b = datetime.datetime.now() 
print((b-a).total_seconds(), '\n')
