from .base import SIMPLE_TYPES_DICT

_context_patterns = []
def add_pattern(p):
    """
    Record struct pattern that's been used for (de)serialization
    """
    _context_patterns.append(p)
def clear_patterns():
    """
    Clear record of struct pattern that have been used for (de)serialization
    """
    del _context_patterns[:]
def get_patterns():
    """
    :returns: record of struct pattern that have been used for (de)serialization
    """
    return _context_patterns[:]

def compute_struct_pattern(types):
    """
    :param types: type names, ``[str]``
    :returns: format string for struct if types are all simple. Otherwise, return None, ``str``
    """
    if not types: #important to filter None and empty first
        return None
    try: 
        return ''.join([SIMPLE_TYPES_DICT[t] for t in types])
    except:
        return None

def reduce_pattern(pattern):
    """
    Optimize the struct format pattern. 
    :param pattern: struct pattern, ``str``
    :returns: optimized struct pattern, ``str``
    """
    if not pattern or len(pattern) == 1 or '%' in pattern:
        return pattern
    prev = pattern[0]
    count = 1
    new_pattern = ''
    nums = [str(i) for i in range(0, 9)]
    for c in pattern[1:]:
        if c == prev and not c in nums:
            count += 1
        else:
            if count > 1:
                new_pattern = new_pattern + str(count) + prev
            else:
                new_pattern = new_pattern + prev
            prev = c
            count = 1
    if count > 1:
        new_pattern = new_pattern + str(count) + c
    else:
        new_pattern = new_pattern + prev
    return new_pattern

## :param expr str: string python expression that is evaluated for serialization
## :returns str: python call to write value returned by expr to serialization buffer
def serialize(expr):
    return "buff.write(%s)"%expr
    
# int32 is very common due to length serialization, so it is special cased
def int32_pack(var):
    """
    :param var: variable name, ``str``
    :returns: struct packing code for an int32
    """
    return serialize('_struct_I.pack(%s)'%var)

# int32 is very common due to length serialization, so it is special cased
def int32_unpack(var, buff):
    """
    :param var: variable name, ``str``
    :returns: struct unpacking code for an int32
    """
    return '(%s,) = _struct_I.unpack(%s)'%(var, buff)

#NOTE: '<' = little endian
def pack(pattern, vars):
    """
    create struct.pack call for when pattern is a string pattern
    :param pattern: pattern for pack, ``str``
    :param vars: name of variables to pack, ``str``
    """
    # - store pattern in context
    pattern = reduce_pattern(pattern)
    add_pattern(pattern)
    return serialize("_struct_%s.pack(%s)"%(pattern, vars))
def pack2(pattern, vars):
    """
    create struct.pack call for when pattern is the name of a variable
    :param pattern: name of variable storing string pattern, ``struct``
    :param vars: name of variables to pack, ``str``
    """
    return serialize("struct.pack(%s, %s)"%(pattern, vars))

def unpack(var, pattern, buff):
    """
    create struct.unpack call for when pattern is a string pattern
    :param var: name of variable to unpack, ``str``
    :param pattern: pattern for pack, ``str``
    :param buff: buffer to unpack from, ``str``
    """
    # - store pattern in context
    pattern = reduce_pattern(pattern)
    add_pattern(pattern)
    return var + " = _struct_%s.unpack(%s)"%(pattern, buff)

def unpack2(var, pattern, buff):
    """
    Create struct.unpack call for when pattern refers to variable
    :param var: variable the stores the result of unpack call, ``str``
    :param pattern: name of variable that unpack will read from, ``str``
    :param buff: buffer that the unpack reads from, ``StringIO``
    """
    return "%s = struct.unpack(%s, %s)"%(var, pattern, buff)

