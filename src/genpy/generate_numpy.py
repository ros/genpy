################################################################################
# numpy support

# this could obviously be directly generated, but it's nice to abstract

## maps ros msg types to numpy types
NUMPY_DTYPE = {
    'float32': 'numpy.float32',
    'float64': 'numpy.float64',
    'bool': 'numpy.bool',
    'int8': 'numpy.int8',
    'int16': 'numpy.int16',
    'int32': 'numpy.int32',
    'int64': 'numpy.int64',
    'uint8': 'numpy.uint8',
    'uint16': 'numpy.uint16',
    'uint32': 'numpy.uint32',
    'uint64': 'numpy.uint64',
    # deprecated type
    'char' : 'numpy.uint8',
    'byte' : 'numpy.int8',
    }
# TODO: this doesn't explicitly specify little-endian byte order on the numpy data instance
def unpack_numpy(var, count, dtype, buff):
    """
    create numpy deserialization code
    """
    return var + " = numpy.frombuffer(%s, dtype=%s, count=%s)"%(buff, dtype, count)

def pack_numpy(var):
    """
    create numpy serialization code
    :param vars: name of variables to pack
    """
    return serialize("%s.tostring()"%var)

