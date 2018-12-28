import types
import dis
import operator
import builtins
import collections
import sys


def make_cell():
    function = (lambda x: lambda: x)(0)
    return function.__closure__[0]


Block = collections.namedtuple('Block', 'type, start, end, stack_height')


class Frame:
    def __init__(self, code, global_names={}, local_names={}, previous_frame=None):
        self.stack = []
        self.code = code
        self.previous_frame = previous_frame
        self.global_names = global_names
        self.local_names = local_names
        self.builtin_names = dir(builtins)
        self.last_instruction = 0
        self.block_stack = []
        self.bytecode = dis.Bytecode(self.code)
        self.instructions = {}
        for instruction in self.bytecode:
            self.instructions[instruction.offset] = instruction
        self.max_offset = max(self.instructions.keys())

        if code.co_cellvars:
            self.cells = {}
            if not previous_frame.cells:
                previous_frame.cells = {}
            for var in code.co_cellvars:
                cell = Cell(self.local_names.get(var))
                previous_frame.cells[var] = self.cells[var] = cell
        else:
            self.cells = None

        if code.co_freevars:
            if not self.cells:
                self.cells = {}
            for var in code.co_freevars:
                assert self.cells is not None
                assert previous_frame.cells, "previous_frame.cells: %r" % (previous_frame.cells,)
                self.cells[var] = previous_frame.cells[var]

    def frame_info(self):
        print(self.stack)
        print(self.local_names)
        print(self.block_stack)
        print('<----------------------->')


class Function:
    def __init__(self, code, name, defaults, kwonly_defaults, annotations, cells, closure, vm):
        self.code = code
        self.vm = vm
        self.argcount = self.code.co_argcount
        self.varnames = self.code.co_varnames
        self.defaults = defaults  # tuple
        self.kwonly_defaults = kwonly_defaults
        self.annotations = annotations
        self.cells = cells
        self.closure = closure
        self.has_args = False
        self.has_kwargs = False
        if code.co_flags & 0x4:
            self.has_args = True
        if code.co_flags & 0x08:
            self.has_kwargs = True

    def __call__(self, *args, **kwargs):
        args = list(args)
        if self.defaults:
            args.extend(list(self.defaults[0]))
        if args:
            callargs = {varname: value for varname, value in zip(self.varnames[0:self.argcount], args)}
        else:
            callargs = {}
        if self.has_args:
            callargs[self.varnames[self.argcount]] = args[self.argcount:]
            if self.has_kwargs:
                callargs[self.varnames[self.argcount + 1]] = kwargs
        else:
            if self.has_kwargs:
                callargs[self.varnames[self.argcount]] = kwargs
        callargs.update(self.kwonly_defaults)
        callargs.update(kwargs)
        if self.annotations:
            callargs['__annotations__'] = self.annotations
        frame = self.vm.make_frame(self.code, callargs)
        return self.vm.run_frame(frame)


class Cell:
    def __init__(self, value):
        self.contents = value

    def get(self):
        return self.contents

    def set(self, value):
        self.contents = value

    def empty(self):
        del self.contents


class VirtualMachine:
    def __init__(self):
        self.frames = []
        self.frame = None
        self.returned_value = None
        self.last_exception = None
        self.unary = {
            'UNARY_POSITIVE': operator.pos,
            'UNARY_NEGATIVE': operator.neg,
            'UNARY_NOT': operator.not_,
            'UNARY_INVERT': operator.inv
        }
        self.binary = {
            'BINARY_ADD': operator.add,
            'BINARY_SUBTRACT': operator.sub,
            'BINARY_MULTIPLY': operator.mul,
            'BINARY_POWER': operator.pow,
            'BINARY_FLOOR_DIVIDE': operator.floordiv,
            'BINARY_TRUE_DIVIDE': operator.truediv,
            'BINARY_MODULO': operator.mod,
            'BINARY_SUBSCR': operator.getitem,
            'BINARY_LSHIFT': operator.lshift,
            'BINARY_RSHIFT': operator.rshift,
            'BINARY_AND': operator.and_,
            'BINARY_XOR': operator.xor,
            'BINARY_OR': operator.or_,
            'BINARY_MATRIX_MULTIPLY': operator.matmul,
        }
        self.inplace = {
            'INPLACE_ADD': operator.iadd,
            'INPLACE_SUBTRACT': operator.isub,
            'INPLACE_MULTIPLY': operator.imul,
            'INPLACE_POWER': operator.ipow,
            'INPLACE_FLOOR_DIVIDE': operator.ifloordiv,
            'INPLACE_TRUE_DIVIDE': operator.itruediv,
            'INPLACE_MODULO': operator.imod,
            'INPLACE_LSHIFT': operator.ilshift,
            'INPLACE_RSHIFT': operator.irshift,
            'INPLACE_AND': operator.iand,
            'INPLACE_XOR': operator.ixor,
            'INPLACE_OR': operator.ior,
            'INPLACE_MATRIX_MULTIPLY': operator.imatmul
        }
        self.compare = {
            '<': operator.lt,
            '<=': operator.le,
            '>': operator.gt,
            '>=': operator.ge,
            '==': operator.eq,
            '!=': operator.ne,
            'is': operator.is_,
            'is not': operator.is_not,
            'in': lambda x, y: x in y,
            'not in': lambda x, y: x not in y,
            'isinstance': lambda x, y: issubclass(x, Exception) and issubclass(x, y),
        }
        self.jump = [
            'JUMP_FORWARD',
            'POP_JUMP_IF_TRUE',
            'POP_JUMP_IF_FALSE',
            'JUMP_IF_TRUE_OR_POP',
            'JUMP_IF_FALSE_OR_POP',
            'JUMP_ABSOLUTE'
        ]

    def make_frame(self, code, callargs={}):
        if self.frames:
            global_names = self.frame.global_names
            local_names = self.frame.local_names
        else:
            global_names = {
                '__name__': '__main__',
                '__doc__': None,
                '__package__': None,
                '__spec__': None,
                '__loader__': None
                }
            local_names = {}
        if callargs:
            local_names.update(callargs)
        return Frame(code, global_names, local_names, self.frame)

    def run_frame(self, frame):
        self.push_frame(frame)
        while self.frame.last_instruction <= self.frame.max_offset:
            instruction = self.frame.instructions[self.frame.last_instruction]
            opname = instruction.opname
            args = instruction.argval
#             self.frame.frame_info()
#             print(opname, args)
            if opname in self.unary:
                self.UNARY_OP(opname)
            elif opname in self.binary:
                self.BINARY_OP(opname)
            elif opname in self.inplace:
                self.INPLACE_OP(opname)
            elif hasattr(self, opname):
                if args is not None:
                    why = getattr(self, opname)(args)
                else:
                    why = getattr(self, opname)()
            if why == 'exception':
                pass
            else:
                while why and frame.block_stack:
                    why = self.manage_block(why)
            if self.frame:
                self.frame.last_instruction += 2
            else:
                break

        return self.returned_value

    # Blocks

    def push_block(self, type, start, end, height=None):
        if height is None:
            height = len(self.frame.stack)
        block = Block(type, start, end, height)
        self.frame.block_stack.append(block)

    def pop_block(self):
        self.frame.block_stack.pop()

    def top_block(self):
        return self.frame.block_stack[-1]

    def unwind_block(self, block):
        if block.type == 'except-handler':
            offset = 3
        else:
            offset = 0

        while len(self.frame.stack) > block.stack_height + offset:
            self.pop()

        if block.type == 'except-handler':
            tb, value, exctype = self.popn(3)
            self.last_exception = exctype, value, tb

    def manage_block(self, why):
        block = self.top_block()
        if block.type == 'loop' and why == 'continue':
            self.frame.last_instruction = self.returned_value

        self.pop_block()
        self.unwind_block(block)

        if block.type == 'loop' and why == 'break':
            self.frame.last_instruction = block.end - 2

    # elif why == 'exception' and block.type in ['setup-except', 'finally']:
    #     self.push_block('except-handler', self.frame.last_instruction + 2, )
    #     exctype, value, tb = self.last_exception
    #     self.push(tb, value, exctype)
    #     # PyErr_Normalize_Exception goes here
    #     self.push(tb, value, exctype)
    #     self.frame.last_instruction = block.end - 2
        elif block.type == 'finally':
            if why in ('return', 'continue'):
                self.push(self.returned_value)
            self.push(why)
            self.frame.last_instruction = block.end - 2

    # Frames

    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()
        if self.frames:
            self.frame = self.frames[-1]
        else:
            self.frame = None

    def top(self):
        return self.frame.stack[-1]

    def pop(self):
        return self.frame.stack.pop()

    def push(self, *values):
        self.frame.stack.extend(values)

    def popn(self, n):
        if n > 0:
            popped_items = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return popped_items
        else:
            return []

    def topn(self, n):
        if n > 0:
            popped_items = self.frame.stack[-n:]
            return popped_items
        else:
            return []

    # Weird stuff with a

    def GET_AWAITABLE(self):
        TOS = self.pop()
        try:
            TOS = TOS.__await__
            self.push(TOS)
        except Exception:
            pass

    def GET_AITER(self):
        TOS = self.pop()
        try:
            TOS = TOS.__aiter__()
            self.push(TOS)
        except Exception:
            pass

    def GET_ANEXT(self):
        TOS = self.pop()
        try:
            TOS = TOS.__anext__().__await__
            self.push(TOS)
        except Exception:
            pass

    def BEFORE_ASYNC_WITH(self):
        try:
            TOS = self.pop()
            self.push(TOS.__aexit__)
            self.push(TOS.__aenter__())
        except Exception:
            pass

    # Loading and storing variables

    def LOAD_CONST(self, number=None):
        self.push(number)

    def LOAD_NAME(self, name=None):
        frame = self.frame
        value = 0
        if name in frame.local_names:
            value = frame.local_names[name]
        elif name in frame.global_names:
            value = frame.global_names[name]
        elif name in frame.builtin_names:
            value = getattr(builtins, name)
        else:
            raise NameError("name '%s' is not defined" % name)
        self.push(value)

    def STORE_NAME(self, name=None):
        self.frame.local_names[name] = self.pop()

    def DELETE_NAME(self, name=None):
        del self.frame.local_names[name]

    def STORE_ATTR(self, name=None):
        TOS1, TOS = self.popn(2)
        setattr(TOS, name, TOS1)
        self.push(TOS1, TOS)

    def DELETE_ATTR(self, name=None):
        delattr(self.top(), name)

    def LOAD_ATTR(self, name):
        TOS = self.pop()
        self.push(getattr(TOS, name))

    def STORE_GLOBAL(self, name=None):
        self.frame.global_names[name] = self.pop()

    def DELETE_GLOBAL(self, name=None):
        del self.frame.global_names[name]

    def LOAD_FAST(self, name=None):
        frame = self.frame
        value = 0
        if name in frame.local_names:
            value = frame.local_names[name]
        else:
            raise NameError("name '%s' is not defined" % name)
        self.push(value)

    def STORE_FAST(self, name=None):
        self.frame.local_names[name] = self.pop()

    def DELETE_FAST(self, name=None):
        del self.frame.local_names[name]

    def STORE_SUBSCR(self):
        TOS2, TOS1, TOS = self.popn(3)
        TOS1[TOS] = TOS2
        self.push(TOS2, TOS1, TOS)

    def DELETE_SUBSCR(self):
        TOS1, TOS = self.popn(2)
        del TOS1[TOS]
        self.push(TOS1, TOS)

    def LOAD_GLOBAL(self, name=None):
        frame = self.frame
        value = 0
        if name in frame.global_names:
            value = frame.global_names[name]
        elif name in frame.builtin_names:
            value = getattr(builtins, name)
        else:
            raise NameError("name '%s' is not defined" % name)
        self.push(value)

    def EXTENDED_ARG(self, count):
        pass

    # Stack manipulation

    def POP_TOP(self):
        self.pop()

    def ROT_TWO(self):
        popped_items = self.popn(2)
        self.push(popped_items[1])
        self.push(popped_items[0])

    def ROT_THREE(self):
        popped_items = self.popn(3)
        self.push(popped_items[2])
        self.push(popped_items[0])
        self.push(popped_items[1])

    def DUP_TOP(self):
        self.push(self.top)

    def DUP_TOP_TWO(self):
        popped_items = self.popn(2)
        self.push(popped_items)
        self.push(popped_items)

    # Arithmetical operations

    def UNARY_OP(self, opname):
        top = self.pop()
        self.push(self.unary[opname](top))

    def BINARY_OP(self, opname):
        popped_items = self.popn(2)
        self.push(self.binary[opname](*popped_items))

    def INPLACE_OP(self, opname):
        popped_items = self.popn(2)
        self.push(self.inplace[opname](*popped_items))

    def COMPARE_OP(self, opname):
        popped_items = self.popn(2)
        self.push(self.compare[opname](*popped_items))

    # Jumps

    def JUMP_ABSOLUTE(self, target):
        self.frame.last_instruction = target - 2

    def JUMP_FORWARD(self, delta):
        self.frame.last_instruction = delta - 2  # maybe it is absolute

    def POP_JUMP_IF_TRUE(self, target):
        top = self.pop()
        if top:
            self.frame.last_instruction = target - 2

    def POP_JUMP_IF_FALSE(self, target):
        top = self.pop()
        if not top:
            self.frame.last_instruction = target - 2

    def JUMP_IF_TRUE_OR_POP(self, target):
        if self.top():
            self.frame.last_instruction = target - 2
        else:
            self.pop()

    def JUMP_IF_FALSE_OR_POP(self, target):
        if not self.top():
            self.frame.last_instruction = target - 2
        else:
            self.pop()

    # Containers

    def BUILD_TUPLE(self, count):
        items = self.popn(count)
        self.push(tuple(items))

    def BUILD_LIST(self, count):
        items = self.popn(count)
        self.push(list(items))

    def BUILD_SET(self, count):
        items = self.popn(count)
        self.push(set(items))

    def BUILD_MAP(self, count):
        items = self.popn(2 * count)
        new_dict = {}
        for i in range(0, 2 * count, 2):
            new_dict[items[i]] = items[i + 1]
        self.push(new_dict)

    def BUILD_CONST_KEY_MAP(self, count):
        keys = self.pop()
        items = self.popn(count)
        new_dict = {}
        for key, item in zip(keys, items):
            new_dict[key] = item
        self.push(new_dict)

    def BUILD_STRING(self, count):
        items = self.popn(count)
        self.push(''.join(items))

    def BUILD_SLICE(self, argc):
        popped_items = self.popn(argc)
        self.push(slice(*popped_items))

    def LIST_APPEND(self, i):
        list.append(self.top()[-i], self.top())

    def SET_ADD(self, i):
        TOS1, TOS = self.popn(2)
        set.add(TOS1[-i], TOS)
        self.push(TOS1, TOS)

    def MAP_ADD(self, i):
        TOS1, TOS = self.popn(2)
        dict.setitem(TOS1[-i], TOS, TOS1)
        self.push(TOS1, TOS)

    def UNPACK_SEQUENCE(self, count):
        sequence = self.pop()
        for elem in reversed(sequence):
            self.push(elem)

    def BUILD_TUPLE_UNPACK(self, count):
        popped_items = self.popn(count)
        new_tuple = tuple([i for item in popped_items for i in item])
        self.push(new_tuple)

    def BUILD_TUPLE_UNPACK_WITH_CALL(self, count):
        popped_items = self.popn(count)
        new_tuple = tuple([i for item in popped_items for i in item])
        self.push(new_tuple)

    def BUILD_LIST_UNPACK(self, count):
        popped_items = self.popn(count)
        new_list = [i for item in popped_items for i in item]
        self.push(new_list)

    def BUILD_SET_UNPACK(self, count):
        popped_items = self.popn(count)
        new_set = {i for item in popped_items for i in item}
        self.push(new_set)

    def BUILD_MAP_UNPACK(self, count):
        popped_items = self.popn(count)
        new_dict = {key: value for item in popped_items for key, value in zip(item.keys(), item.values())}
        self.push(new_dict)

    def BUILD_MAP_UNPACK_WITH_CALL(self, count):
        popped_items = self.popn(count)
        new_dict = {key: value for item in popped_items for key, value in zip(item.keys(), item.values())}
        self.push(new_dict)

    def UNPACK_EX(self, counts):
        TOS = self.pop()
        before = counts % 256
        after = counts // 256
        tuple_len = len(TOS)
        for i in range(1, after + 1):
            self.push(TOS[-i])
        self.push(list(TOS[before:(tuple_len - after)]))
        for i in range(before - 1, -1, -1):
            self.push(TOS[i])

    # Iterators

    def GET_ITER(self):
        self.push(iter(self.pop()))

    def FOR_ITER(self, target):
        try:
            self.push(next(self.top()))
        except StopIteration:
            self.pop()
            self.frame.last_instruction = target - 2

    # Loops

    def SETUP_LOOP(self, target):
        self.push_block('loop', self.frame.last_instruction + 2, target)

    def BREAK_LOOP(self):
        # self.manage_block('break')
        return 'break'

    def CONTINUE_LOOP(self, target):
        # self.manage_block('continue')
        self.returned_value = target
        return 'continue'

    def POP_BLOCK(self):
        self.pop_block()

    # Functions

    def CALL_FUNCTION(self, argc):
        posargs = self.popn(argc)
        function = self.pop()
        returned_value = function(*posargs)
        if self.frame:
            self.push(returned_value)

    def CALL_FUNCTION_KW(self, argc):
        kwargs_keys = self.pop()
        kwargs_count = len(kwargs_keys)
        kwargs_values = self.popn(kwargs_count)
        kwargs = {key: value for key, value in zip(kwargs_keys, kwargs_values)}
        posargs = self.popn(argc - kwargs_count)
        function = self.pop()
        returned_value = function(*posargs, **kwargs)
        if self.frame:
            self.push(returned_value)

    def CALL_FUNCTION_EX(self, argval):
        kwargs = self.pop()
        if isinstance(kwargs, tuple):
            function = self.pop()
            args = kwargs
            kwargs = {}
            returned_value = function(*args, **kwargs)
        else:
            args = self.pop()
            function = self.pop()
            returned_value = function(*args, **kwargs)
        if self.frame:
            self.push(returned_value)

    def MAKE_FUNCTION(self, argc):
        name = self.pop()
        code = self.pop()

        cells = ()
        annotations = {}
        kwonly_defaults = {}
        defaults = ()
        if argc >= 8:
            cells = self.pop()
            argc -= 8
        if argc >= 4:
            annotations = self.pop()
            argc -= 4
        if argc >= 2:
            kwonly_defaults = self.pop()
            argc += 1
        if argc == 1:
            defaults = self.pop()
            argc = 0

        func = Function(code, name, defaults, kwonly_defaults, annotations, cells, None, self)
        self.push(func)

    def LOAD_CLOSURE(self, name):
        self.push(self.frame.cells[name])

    def RETURN_VALUE(self):
        self.returned_value = self.top()
        self.pop_frame()
        if self.frame:
            self.push(self.returned_value)
        return 'return'

    # Annotations

    def SETUP_ANNOTATIONS(self):
        if '__annotations__' not in self.frame.local_names:
            self.frame.local_names['__annotations__'] = {}

    def STORE_ANNOTATION(self, name):
        self.frame.local_names['__annotations__'][name] = self.pop()

    # Importing

    def IMPORT_NAME(self, name):
        level, fromlist = self.popn(2)
        module = builtins.__import__(name, level=level, fromlist=fromlist)
        self.push(module)

    def IMPORT_FROM(self, name):
        module = self.top()
        self.push(getattr(module, name))

    def IMPORT_STAR(self):
        module = self.pop()
        for attribute in dir(module):
            if attribute[0] != '_':
                self.frame.local_names[attribute] = getattr(module, attribute)

    # Classes

    def LOAD_DEREF(self, name):
        self.push(self.frame.cells[name].get())

    def STORE_DEREF(self, name):
        self.frame.cells[name].set(self.pop())

    def DELETE_DEREF(self, name):
        self.frame.cells[name].empty()

    def LOAD_BUILD_CLASS(self):
        self.push(builtins.__build_class__)

    # Format

    # def FORMAT_VALUE(self, flags):
    #     fmt_spec = None
    #     if (flags & 0x04) == 0x04:
    #         fmt_spec = self.pop()
    #     value = self.pop()
    #     if (flags & 0x03) == 0x01:
    #         value = builtins.str(value)
    #     if (flags & 0x03) == 0x02:
    #         value = builtins.repr(value)
    #     if (flags & 0x03) == 0x03:
    #         value = builtins.repr(value)
    #     self.push(builtins.format(value, format_spec=fmt_spec))

    # Exceptions

    def RAISE_VARARGS(self, argc):
        if argc == 3:
            traceback, param, exc = self.popn(3)
            self.push(exc(param, traceback))
        elif argc == 2:
            exc, param = self.popn(2)
            self.push(exc(param))
        elif argc == 1:
            exc = self.pop()
            self.push(exc())

    def POP_EXCEPT(self):
        block = self.pop_block()
        if block.type != 'except-handler':
            raise Exception("popped block is not an except handler")
        self.unwind_block(block)

    def SETUP_EXCEPT(self, target):
        self.push_block('setup-except', self.frame.last_instruction + 2, target)

    def SETUP_FINALLY(self, target):
        self.push_block('finally', self.frame.last_instruction + 2, target)

    def END_FINALLY(self):
        v = self.pop()
        if isinstance(v, str):
            why = v
            if why in ('return', 'continue'):
                self.returned_value = self.pop()
        elif v is None:
            why = None
        return why

    def SETUP_WITH(self, delta):
        cntxt = self.pop()
        self.push(cntxt.__exit__)
        cntxt_enter = cntxt.__enter__()
        self.push_block('finally', self.frame.last_instruction + 2, delta)
        self.push(cntxt_enter)

    # Zero level ops

    def NOP(self):
        pass

    def PRINT_EXPR(self):
        answer = self.pop()

    def run(self, code: types.CodeType) -> None:
        """
        :param code: code for interpreting
        """
        global_frame = self.make_frame(code)
        self.run_frame(global_frame)


if __name__ == '__main__':
    code = r"""
def f(x):
    return x * 2
print(f(3))
"""
    ccode = compile(code, '<stdin>', 'exec')

    vm = VirtualMachine()
    vm.run(ccode)
