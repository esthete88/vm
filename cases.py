class Case:
    def __init__(self, name: str, text_code: str):
        self.name = name
        self.text_code = text_code


TEST_CASES = [
    Case(
        name="dict",
        text_code=r"""
d = {1: 2, 3: 4}
print(d[1])
"""),
    Case(
        name="class",
        text_code=r"""
class T(object):
    def __init__(self):
        self._a = 1

t = T()
print(t._a)
"""),
    Case(
        name="with",
        text_code=r"""
with open('a.txt', 'w') as a:
    print(3)
"""),
    Case(
        name="binary_add",
        text_code=r"""
print(4 + 5)
"""),
    Case(
        name="sub_variables",
        text_code=r"""
a = 5
b = 4
print(a - b)
"""),
    Case(
        name="while",
        text_code=r"""
a = 5
while a >= 0:
    print(a)
    a -= 1
"""),
    Case(
        name="if",
        text_code=r"""
x = 7
if (x > 6):
    print(1)
"""),
    Case(
        name="else",
        text_code=r"""
x = 6
if (x > 6):
    print(1)
elif (x == 6):
    print(2)
else:
    print(3)
"""),
    Case(
        name="inplace_add",
        text_code=r"""
a = 5
a += 6
print(a)
"""),
    Case(
        name="pass",
        text_code=r"""
pass
"""),
    Case(
        name="binary_add",
        text_code=r"""
print(4 + 5)
"""),
    Case(
        name="constant0",
        text_code=r"""
print(0)
"""),
    Case(
        name="while_break",
        text_code=r"""
a = 5
while True:
    print(a)
    if a == 0:
        break
    a -= 1
"""),
    Case(
        name="while_continue",
        text_code=r"""
a = 5
while True:
    print(a)
    if a != 0:
        a -= 1
        continue
    break
"""),
    Case(
        name="for",
        text_code=r"""
for i in [1, 2, 3]:
    print(i)
"""),
    Case(
        name="forfor",
        text_code=r"""
for i in [1, 2]:
    for j in [3, 4]:
        print([i, j])
"""),
    Case(
        name="func",
        text_code=r"""
def f():
    print(1)
f()
"""),
    Case(
        name="func_with_return",
        text_code=r"""
def f():
    return 1
print(f())
"""),
    Case(
        name="func_with_args",
        text_code=r"""
def f(x):
    return x * 2
print(f(3))
"""),
    Case(
        name="func_with_packed_args",
        text_code=r"""
def f(*args):
    for arg in args:
        print(arg * 3)
f(1, 2, 3, 4, 5)
"""),
    Case(
        name="import",
        text_code=r"""
import numpy
"""),
    Case(
        name="import_star",
        text_code=r"""
from numpy import *
"""),
    Case(
        name="import_from",
        text_code=r"""
from numpy import cos

print(cos(1.57))
"""),
    Case(
        name="multiple_import_from",
        text_code=r"""
from numpy import cos, abs, sin
"""),
    Case(
        name="import_alias",
        text_code=r"""
from numpy import linalg as lg
"""),
    Case(
        name="mytest1",
        text_code=r"""
print(17, 12, 0)
"""),
    Case(
        name="mytest2",
        text_code=r"""
print(5>3)
"""),
    Case(
        name="mytest3",
        text_code=r"""
print([1, 2, 3, 4])
"""),
    Case(
        name="mytest4",
        text_code=r"""
print([1, 2, 3, 4] + [1, 2])
"""),
    Case(
        name="mytest5",
        text_code=r"""
a = 9
print(4 + a)
"""),
    Case(
        name="mytest6",
        text_code=r"""
mas = [1, 2, 3, 4, 5]
print(mas[1:4])
"""),
    Case(
        name="mytest7",
        text_code=r"""
for i in range(5):
    print(i)
"""),
    Case(
        name="mytest8",
        text_code=r"""
i = 1
while i < 5:
    print(i)
    i += 1
"""),
    Case(
        name="mytest9",
        text_code=r"""
mas = [0]
i = 1
while i < 5:
    mas.append(i)
    i += 1
print(mas)
"""),
    Case(
        name="mytest10",
        text_code=r"""
if 3 < 6:
    print({1:"1", 2:"2"})
"""),
    Case(
        name="mytest11",
        text_code=r"""
print({**{}})
"""),
    Case(
        name="mytest12",
        text_code=r"""
print({**{"a": 1, "b": 2}})
"""),
    Case(
        name="mytest13",
        text_code=r"""
a = {1, 2}
b = {3, 4}
c = {5, 6}
print({*a, *b, *c})
"""),
    Case(
        name="mytest14",
        text_code=r"""
print([*["a", "b", "c"]])
"""),
    Case(
        name="mytest15",
        text_code=r"""
a = (1, 2)
b = (3, 4)
print((*a, *b))
"""),
    Case(
        name="mytest16",
        text_code=r"""
x = ("Guru99", 20, "Education")
(company, emp, profile) = x
print(company, emp)
"""),
    Case(
        name="mytest17",
        text_code=r"""
for i in range(10):
    print(i)
    if i % 5 == 0:
        break
"""),
    Case(
        name="mytest18",
        text_code=r"""
for i in range(10):
    if i % 5 == 0:
        continue
    print(i)
"""),
    Case(
        name="mytest19",
        text_code=r"""
i = 0
while i < 10:
    print(i)
    if i % 5 == 0:
        break
"""),
    Case(
        name="mytest20",
        text_code=r"""
i = 0
while True:
    print(i)
    if i % 5 == 0:
        break
"""),
    Case(
        name="mytest21",
        text_code=r"""
i = 0
while True:
    print(i)
    i += 1
    for j in range(10):
        for k in range(5, -2, -1):
            t = 0
            while True:
                t += 1
                if t == 3:
                    break
    if i % 5 == 0:
        break
"""),
    Case(
        name="mytestFUNC",
        text_code=r"""
def f(x, y, a, b, c, d):
    def ff(x):
        print("nested function")

    ff(0)
    new_var = 123
    print(a, b, c, d)
    new_var += 5000
    print(new_var)
    return 5

a = {"a": "1", "b": "2"}
b = {"c": "3", "d": "4"}
d = (1, 2, 4, 8)
print(f(1, 2, *d))
"""),
    Case(
        name="mytest22",
        text_code=r"""
i = 0
while True:
    print(i)
    i += 1
    for j in range(10):
        for k in range(5, -2, -1):
            t = 0
            while True:
                t += 1
                if t == 3:
                    break
    if i % 15 == 0:
        break
    if i % 5 == 0:
        continue
"""),
    Case(
        name="mytest23",
        text_code=r"""
i = 0
while True:
    print(i)
    i += 1
    for j in range(10):
        break
    break
"""),
    Case(
        name="mytest24",
        text_code=r"""
for i in range(5):
    for j in range(6):
        for k in range(7):
            print(i, j, k)
"""),
    Case(
        name="mytest25",
        text_code=r"""
for i in range(5):
    for j in range(6):
        for k in range(7, -1):
            print(i, j, k)
            if k == -7:
                print("BREAK")
                break
"""),
    Case(
        name="mytest26",
        text_code=r"""
for i in range(5):
    for j in range(6, -5):
        for k in range(7, -1):
            print(i, j, k)
            if k == -7:
                print("BREAK")
                break
            break
"""),
    Case(
        name="mytest27",
        text_code=r"""
for i in range(5):
    for j in range(6, -5):
        for k in range(7, -1):
            print(i, j, k)
            if k == -7:
                print("BREAK")
                break
            if j == -20:
                break
"""),
    Case(
        name="mytest28",
        text_code=r"""
a = (1, 2)
b = (3, 4)
print(*a, *b)
"""),
    Case(
        name="mytest29",
        text_code=r"""
a = {1: "1", 2 : "2"}
b = {3 : "3", 4 : "4"}
print(**a, **b)
"""),
    Case(
        name="ListAppend",
        text_code=r"""
a = [1, 2, 3]
a.append(4)
print(a)
"""),
    Case(
        name="mytest30",
        text_code=r"""
print(isinstance(1, int))
"""),
    Case(
        name="constant",
        text_code=r"""
print(17)
"""),
    Case(
        name="test102",
        text_code=r"""
d = {1: 2, 3: 4}
print(d[1])
"""),
    Case(
        name="catching_IndexError",
        text_code=r"""
try:
    [][1]
    print("Shouldn't be here...")
except IndexError:
    print("caught it!")
"""),

    Case(
        name="tricky_loop",
        text_code=r"""
for i in range(5, -1):
    for j in range(7):
        if j == 6:
            break
    if j == 6:
        break
"""),
    Case(
        name="FUNCTION4",
        text_code=r"""
def other_function(x, y, z, u, w, i = 9, j = 10):
    print(x, y, z, u, w + 1)

def print_msg(msg):

    def printer(x = 8):
        print(msg)

    return printer  # this got changed

another = print_msg("Hello")
another()
"""),
    Case(
        name="BUILD_TUPLE_UNPACK",
        text_code=r"""
x = ("a", "b")
y = ("c", "d")
z = (*x, *y)
print(z)
"""),
    Case(
        name="BUILD_SET_UNPACK",
        text_code=r"""
x = ("a", "b")
y = ("c", "d")
z = {*x, *y}
print(z)
"""),
    Case(
        name="ANNOTATIONS",
        text_code=r"""
a : int = 0
print(a)
"""),
    Case(
        name="JUMP_IF_FALSE_OR_POP",
        text_code=r"""
print(4 << 9)
"""
    ),
    Case(
        name="JUMP_IF_TRUE_OR_POP",
        text_code=r"""
print(x and x or 'no x available')
"""
    ),
    Case(
        name="FUNCTION_TEST_1",
        text_code=r"""
def f():
    print(5)

f()
"""
    ),
    Case(
        name="FUNCTION_TEST_2",
        text_code=r"""
def f(x):
    print(x)

f(5)
"""
    ),
    Case(
        name="FUNCTION_TEST_3",
        text_code=r"""
def f(x, y, z):
    print(x)
    y += 3
    print(z - y)
    return 0

print(5, 6, 7)
"""
    ),
    Case(
        name="FUNCTION_TEST_4",
        text_code=r"""
def f(x, y, z):
    print(x)
    y += 3
    print(z - y)
    return 0

print(x = 5, y = 6, z = 7)
"""
    ),
    Case(
        name="FUNCTION_TEST_5",
        text_code=r"""
def f(x, y, z, k):
    print(x)
    print(k)
    y += 3
    print(z - y)
    return 0

print(8, x = 5, y = 6, z = 7)
"""
    ),
    Case(
        name="UNPACK_EX",
        text_code=r"""
a, *b, c = 1, 2, 3, 4, 5, 6
print(a, b, c)
"""
    ),

    Case(
        name="UNPACK_EX",
        text_code=r"""
a, *b, t, c = 1, 2, 3, 4, 5, 6
print(a, b, c)
"""
    ),
    Case(
        name="BUILD_MAP_UNPACK_WITH_CALLBACK",
        text_code=r"""
def f(x, y, a, b, c, d):
    print(a, b, c, d)

a = {"a": "1", "b": "2"}
b = {"c": "3", "d": "4"}
f(1, 2, **a, **b)
""",
    ),
    Case(
        name="BUILD_TUPLE_UNPACK_WITH_CALLBACK",
        text_code=r"""
def f(x, y, a, b, c, d):
    print(a, b, c, d)
    return 5

a = {"a": "1", "b": "2"}
b = {"c": "3", "d": "4"}
d = (1, 2, 4, 8)
print(f(1, 2, *d))
"""
    ),
    Case(
        name="FUNCTION_COARGCOUNT",
        text_code=r"""
def f(x, y, a, b, c, d):
    def ff(x):
        print("nested function")

    print(a, b, c, d)
    return 5

a = {"a": "1", "b": "2"}
b = {"c": "3", "d": "4"}
d = (1, 2, 4, 8)
print(f(1, 2, *d))
"""
    ),
    Case(
        name="nested_loop",
        text_code=r"""
k = 2
for u in range(k):
    if k == 2:
        for z in range(k):
            break
"""),
    Case(
        name="nested_loop",
        text_code=r"""
k = 9
for u in range(k):
    if k == 9:
        for z in range(k):
            if z == 5:
                break
"""),
    Case(
        name="EXTENDED_ARG",
        text_code=r"""
x = false
if x:
    x += 1
    x ** 2
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x += 1
    x -= 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    x += 1
    x -= 1
    print(x)
else:
    print(hello)

"""
    ),

    Case(
        name="KeyboardInterrupt",
        text_code=r"""
raise KeyboardInterrupt
"""),
    Case(
        name="NameError",
        text_code=r"""
raise NameError('HiThere')
"""),
]
