def test_reduce_pattern():
    from genpy.generate_struct import reduce_pattern
    tests = [
        ('', ''),
        ('hhhh', '4h'),
        ('hhhhi', '4hi'),
        ('hhhhiiiibbb', '4h4i3b'),
        ('1h2h3h', '1h2h3h'),
        ('hIi', 'hIi'),
        ('66h', '66h'),
        ('%ss', '%ss'),  # don't reduce strings with format chars in them
        ('<I', '<I'),
        ('<11s', '<11s'),
        ]
    for input_, result in tests:
        assert result == reduce_pattern(input_)


def test_pack():
    from genpy.generate_struct import pack
    assert 'buff.write(_get_struct_3lL3bB().pack(foo, bar))' == pack('lllLbbbB', 'foo, bar')


def test_pack2():
    from genpy.generate_struct import pack2
    assert 'buff.write(struct.Struct(patt_name).pack(foo, bar))' == pack2('patt_name', 'foo, bar')


def test_unpack():
    from genpy.generate_struct import unpack
    assert 'var_x = _get_struct_I3if2I().unpack(bname)' == unpack('var_x', 'IiiifII', 'bname')


def test_unpack2():
    from genpy.generate_struct import unpack2
    assert 'x = struct.unpack(patt, b)' == unpack2('x', 'patt', 'b')


def test_unpack3():
    from genpy.generate_struct import unpack3
    assert 'x = s.unpack(b)' == unpack3('x', 's', 'b')


def test_compute_struct_pattern():
    from genpy.generate_struct import compute_struct_pattern
    assert compute_struct_pattern(None) is None
    assert compute_struct_pattern([]) is None
    # string should immediately bork any simple types
    assert compute_struct_pattern(['string']) is None
    assert compute_struct_pattern(['uint32', 'string']) is None
    assert compute_struct_pattern(['string', 'int32']) is None
    # array types should not compute
    assert compute_struct_pattern(['uint32[]']) is None
    assert compute_struct_pattern(['uint32[1]']) is None

    assert 'B' == compute_struct_pattern(['uint8'])
    assert 'BB' == compute_struct_pattern(['uint8', 'uint8'])
    assert 'B' == compute_struct_pattern(['char'])
    assert 'BB' == compute_struct_pattern(['char', 'char'])
    assert 'b' == compute_struct_pattern(['byte'])
    assert 'bb' == compute_struct_pattern(['byte', 'byte'])
    assert 'b' == compute_struct_pattern(['int8'])
    assert 'bb' == compute_struct_pattern(['int8', 'int8'])
    assert 'H' == compute_struct_pattern(['uint16'])
    assert 'HH' == compute_struct_pattern(['uint16', 'uint16'])
    assert 'h' == compute_struct_pattern(['int16'])
    assert 'hh' == compute_struct_pattern(['int16', 'int16'])
    assert 'I' == compute_struct_pattern(['uint32'])
    assert 'II' == compute_struct_pattern(['uint32', 'uint32'])
    assert 'i' == compute_struct_pattern(['int32'])
    assert 'ii' == compute_struct_pattern(['int32', 'int32'])
    assert 'Q' == compute_struct_pattern(['uint64'])
    assert 'QQ' == compute_struct_pattern(['uint64', 'uint64'])
    assert 'q' == compute_struct_pattern(['int64'])
    assert 'qq' == compute_struct_pattern(['int64', 'int64'])
    assert 'f' == compute_struct_pattern(['float32'])
    assert 'ff' == compute_struct_pattern(['float32', 'float32'])
    assert 'd' == compute_struct_pattern(['float64'])
    assert 'dd' == compute_struct_pattern(['float64', 'float64'])

    assert 'bBhHiIqQfd' == compute_struct_pattern(['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32', 'float64'])
