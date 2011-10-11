# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import genmsg.msgs
from genmsg.msgs import MsgSpec
from genmsg.msg_loader import MsgContext

import cStringIO
import time
import sys


def test_exceptions():
    from genpy.generator import MsgGenerationException
    try:
        raise MsgGenerationException('bad')
    except MsgGenerationException:
        pass

def test_reduce_pattern():
    import genpy.generator
    tests = [
        ('', ''),
        ('hhhh', '4h'),
        ('hhhhi', '4hi'),
        ('hhhhiiiibbb', '4h4i3b'),            
        ('1h2h3h', '1h2h3h'),            
        ('hIi', 'hIi'),
        ('66h', '66h'),
        ('%ss', '%ss'), #don't reduce strings with format chars in them
        ('<I', '<I'),
        ('<11s', '<11s'),            
        ]
    for input, result in tests:
        assert result == genpy.generator.reduce_pattern(input)
        
def test_is_simple():
    import genpy.generator
    for t in ['uint8', 'int8', 'uint16', 'int16', 'uint32', 'int32', 'uint64', 'int64', 'float32', 'float64', 'byte', 'char']:
        assert genpy.generator.is_simple(t)

def test_SIMPLE_TYPES():
    import genpy.generator
    # tripwire to make sure we don't add builtin types without making sure that simple types has been updated
    assert set(['string', 'time', 'duration']) == set(genmsg.msgs.BUILTIN_TYPES) - set(genpy.generator.SIMPLE_TYPES)
    
def test_is_special():
    import genpy.generator
    for t in ['time', 'duration', 'Header']:
        assert genpy.generator.is_special(t)
        
def test_Simple():
    import genpy.generator
    val = genpy.generator.get_special('time').import_str
    assert 'import genpy' == val, val
    assert 'import genpy' == genpy.generator.get_special('duration').import_str
    assert 'import std_msgs.msg' == genpy.generator.get_special('Header').import_str

    assert 'genpy.Time()' == genpy.generator.get_special('time').constructor
    assert 'genpy.Duration()' == genpy.generator.get_special('duration').constructor
    assert 'std_msgs.msg._Header.Header()' == genpy.generator.get_special('Header').constructor

    assert 'self.foo.canon()' == genpy.generator.get_special('time').get_post_deserialize('self.foo')
    assert 'bar.canon()' == genpy.generator.get_special('time').get_post_deserialize('bar')
    assert 'self.foo.canon()' == genpy.generator.get_special('duration').get_post_deserialize('self.foo')
    assert None == genpy.generator.get_special('Header').get_post_deserialize('self.foo')

def test_compute_post_deserialize():
    import genpy.generator
    assert 'self.bar.canon()' == genpy.generator.compute_post_deserialize('time', 'self.bar')
    assert 'self.bar.canon()' == genpy.generator.compute_post_deserialize('duration', 'self.bar')
    assert None == genpy.generator.compute_post_deserialize('Header', 'self.bar')

    assert None == genpy.generator.compute_post_deserialize('int8', 'self.bar')
    assert None == genpy.generator.compute_post_deserialize('string', 'self.bar')

def test_compute_struct_pattern():
    import genpy.generator
    assert None == genpy.generator.compute_struct_pattern(None)
    assert None == genpy.generator.compute_struct_pattern([])
    # string should immediately bork any simple types
    assert None == genpy.generator.compute_struct_pattern(['string'])
    assert None == genpy.generator.compute_struct_pattern(['uint32', 'string'])
    assert None == genpy.generator.compute_struct_pattern(['string', 'int32'])
    # array types should not compute
    assert None == genpy.generator.compute_struct_pattern(['uint32[]'])
    assert None == genpy.generator.compute_struct_pattern(['uint32[1]'])

    assert "B" == genpy.generator.compute_struct_pattern(['uint8'])
    assert "BB" == genpy.generator.compute_struct_pattern(['uint8', 'uint8'])
    assert "B" == genpy.generator.compute_struct_pattern(['char'])
    assert "BB" == genpy.generator.compute_struct_pattern(['char', 'char'])        
    assert "b" == genpy.generator.compute_struct_pattern(['byte'])
    assert "bb" == genpy.generator.compute_struct_pattern(['byte', 'byte'])        
    assert "b" == genpy.generator.compute_struct_pattern(['int8'])
    assert "bb" == genpy.generator.compute_struct_pattern(['int8', 'int8'])        
    assert "H" == genpy.generator.compute_struct_pattern(['uint16'])
    assert "HH" == genpy.generator.compute_struct_pattern(['uint16', 'uint16'])        
    assert "h" == genpy.generator.compute_struct_pattern(['int16'])
    assert "hh" == genpy.generator.compute_struct_pattern(['int16', 'int16'])        
    assert "I" == genpy.generator.compute_struct_pattern(['uint32'])
    assert "II" == genpy.generator.compute_struct_pattern(['uint32', 'uint32'])        
    assert "i" == genpy.generator.compute_struct_pattern(['int32'])
    assert "ii" == genpy.generator.compute_struct_pattern(['int32', 'int32'])        
    assert "Q" == genpy.generator.compute_struct_pattern(['uint64'])
    assert "QQ" == genpy.generator.compute_struct_pattern(['uint64', 'uint64'])        
    assert "q" == genpy.generator.compute_struct_pattern(['int64'])
    assert "qq" == genpy.generator.compute_struct_pattern(['int64', 'int64'])        
    assert "f" == genpy.generator.compute_struct_pattern(['float32'])
    assert "ff" == genpy.generator.compute_struct_pattern(['float32', 'float32'])
    assert "d" == genpy.generator.compute_struct_pattern(['float64'])
    assert "dd" == genpy.generator.compute_struct_pattern(['float64', 'float64'])

    assert "bBhHiIqQfd" == genpy.generator.compute_struct_pattern(['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32', 'float64'])

def test_flatten():
    import genpy.generator
    msg_context = MsgContext.create_default()

    simple = MsgSpec(['string'], ['data'], [], 'string data\n')
    simple2 = MsgSpec(['string', 'int32'], ['data', 'data2'], [], 'string data\nint32 data2\n')
    assert simple == genpy.generator.flatten(msg_context, simple)
    assert simple2 == genpy.generator.flatten(msg_context, simple2)

    b1 = MsgSpec(['int8'], ['data'], [], 'X')
    b2 = MsgSpec(['f_msgs/Base'], ['data'], [], 'X')
    b3 = MsgSpec(['f_msgs/Base2', 'f_msgs/Base2'], ['data3', 'data4'], [], 'X')
    b4 = MsgSpec(['f_msgs/Base3', 'f_msgs/Base3'], ['dataA', 'dataB'], [], 'X')

    msg_context.register('f_msgs/Base', b1)
    msg_context.register('f_msgs/Base2', b2)
    msg_context.register('f_msgs/Base3', b3)
    msg_context.register('f_msgs/Base4', b4)

    assert MsgSpec(['int8'], ['data.data'], [], 'X') == genpy.generator.flatten(msg_context, b2)
    assert MsgSpec(['int8', 'int8'], ['data3.data.data', 'data4.data.data'], [], 'X') == genpy.generator.flatten(b3)
    assert MsgSpec(['int8', 'int8', 'int8', 'int8'],
                              ['dataA.data3.data.data', 'dataA.data4.data.data', 'dataB.data3.data.data', 'dataB.data4.data.data'],
                              [], 'X') == genpy.generator.flatten(b4)
        
def test_numpy_dtype():
    import genpy.generator
    for t in genpy.generator.SIMPLE_TYPES:
        assert t in genpy.generator._NUMPY_DTYPE

def test_default_value():
    import genpy.generator
    msg_context = MsgContext.create_default()

    msg_context.register('fake_msgs/String', MsgSpec(['string'], ['data'], [], 'string data\n'))
    msg_context.register('fake_msgs/ThreeNums', MsgSpec(['int32', 'int32', 'int32'], ['x', 'y', 'z'], [], 'int32 x\nint32 y\nint32 z\n'))

    # trip-wire: make sure all builtins have a default value
    for t in genmsg.msgs.BUILTIN_TYPES:
        assert type(genpy.generator.default_value(t, 'roslib')) == str

    # simple types first
    for t in ['uint8', 'int8', 'uint16', 'int16', 'uint32', 'int32', 'uint64', 'int64', 'byte', 'char']:
        assert '0' == genpy.generator.default_value(t, 'std_msgs')
        assert '0' == genpy.generator.default_value(t, 'roslib')
    for t in ['float32', 'float64']:
        assert '0.' == genpy.generator.default_value(t, 'std_msgs')
        assert '0.' == genpy.generator.default_value(t, 'roslib')
    assert "''" == genpy.generator.default_value('string', 'roslib')

    # builtin specials
    assert 'genpy.Time()' == genpy.generator.default_value('time', 'roslib')
    assert 'genpy.Duration()' == genpy.generator.default_value('duration', 'roslib')
    assert 'std_msgs.msg._Header.Header()' == genpy.generator.default_value('Header', 'roslib')

    assert 'genpy.Time()' == genpy.generator.default_value('time', 'std_msgs')
    assert 'genpy.Duration()' == genpy.generator.default_value('duration', 'std_msgs')
    assert 'std_msgs.msg._Header.Header()' == genpy.generator.default_value('Header', 'std_msgs')

    # generic instances
    # - unregistered type
    assert None == genpy.generator.default_value("unknown_msgs/Foo", "unknown_msgs")
    # - wrong context
    assert None == genpy.generator.default_value('ThreeNums', 'std_msgs')

    # - registered types
    assert 'fake_msgs.msg.String()' == genpy.generator.default_value('fake_msgs/String', 'std_msgs')
    assert 'fake_msgs.msg.String()' == genpy.generator.default_value('fake_msgs/String', 'fake_msgs')
    assert 'fake_msgs.msg.String()' == genpy.generator.default_value('String', 'fake_msgs')
    assert 'fake_msgs.msg.ThreeNums()' == genpy.generator.default_value('fake_msgs/ThreeNums', 'roslib')
    assert 'fake_msgs.msg.ThreeNums()' == genpy.generator.default_value('fake_msgs/ThreeNums', 'fake_msgs')
    assert 'fake_msgs.msg.ThreeNums()' == genpy.generator.default_value('ThreeNums', 'fake_msgs')

    # var-length arrays always default to empty arrays... except for byte and uint8 which are strings
    for t in ['int8', 'uint16', 'int16', 'uint32', 'int32', 'uint64', 'int64', 'float32', 'float64', 'char']:
        assert '[]' == genpy.generator.default_value(t+'[]', 'std_msgs')
        assert '[]' == genpy.generator.default_value(t+'[]', 'roslib')

    assert "''" == genpy.generator.default_value('uint8[]', 'roslib')
    assert "''" == genpy.generator.default_value('byte[]', 'roslib')

    # fixed-length arrays should be zero-filled... except for byte and uint8 which are strings
    for t in ['float32', 'float64']:
        assert '[0.,0.,0.]' == genpy.generator.default_value(t+'[3]', 'std_msgs')
        assert '[0.]' == genpy.generator.default_value(t+'[1]', 'std_msgs')
    for t in ['int8', 'uint16', 'int16', 'uint32', 'int32', 'uint64', 'int64', 'char']:
        assert '[0,0,0,0]' == genpy.generator.default_value(t+'[4]', 'std_msgs')
        assert '[0]' == genpy.generator.default_value(t+'[1]', 'roslib')

    assert "chr(0)*1" == genpy.generator.default_value('uint8[1]', 'roslib')
    assert "chr(0)*4" == genpy.generator.default_value('uint8[4]', 'roslib')
    assert "chr(0)*1" == genpy.generator.default_value('byte[1]', 'roslib')
    assert "chr(0)*4" == genpy.generator.default_value('byte[4]', 'roslib')

    assert '[]' == genpy.generator.default_value('fake_msgs/String[]', 'std_msgs')
    assert '[fake_msgs.msg.String(),fake_msgs.msg.String()]' == genpy.generator.default_value('fake_msgs/String[2]', 'std_msgs')

def test_make_python_safe():
    import genpy.generator
    from genmsg.msgs import Constant
    s = MsgSpec(['int32', 'int32', 'int32', 'int32'], ['ok', 'if', 'self', 'fine'],
                [Constant('int32', 'if', '1', '1'), Constant('int32', 'okgo', '1', '1')],
                'x')
    s2 = genpy.generator.make_python_safe(s)
    assert s != s2
    assert ['ok', 'if_', 'self_', 'fine'] == s2.names
    assert s2.types == s.types
    assert [Constant('int32', 'if_', '1', '1') == Constant('int32', 'okgo', '1', '1')], s2.constants
    assert s2.text == s.text
    
def test_compute_pkg_type():
    import genpy.generator
    try:
        genpy.generator.compute_pkg_type('std_msgs', 'really/bad/std_msgs/String')
    except genpy.generator.MsgGenerationException: pass
    assert ('std_msgs', 'String') == genpy.generator.compute_pkg_type('std_msgs', 'std_msgs/String')
    assert ('std_msgs', 'String') == genpy.generator.compute_pkg_type('foo', 'std_msgs/String')    
    assert ('std_msgs', 'String') == genpy.generator.compute_pkg_type('std_msgs', 'String')
        
def test_compute_import():

    assert [] == genpy.generator.compute_import('foo', 'bar')
    assert [] == genpy.generator.compute_import('foo', 'int32')

    msg_context = MsgContext.create_default()
    msg_context.register('ci_msgs/Base', MsgSpec(['int8'], ['data'], [], 'int8 data\n'))
    msg_context.register('ci2_msgs/Base2', MsgSpec(['ci_msgs/Base'], ['data2'], [], 'ci_msgs/Base data2\n'))
    msg_context.register('ci3_msgs/Base3', MsgSpec(['ci2_msgs/Base2'], ['data3'], [], 'ci2_msgs/Base2 data3\n'))
    msg_context.register('ci4_msgs/Base', MsgSpec(['int8'], ['data'], [], 'int8 data\n'))
    msg_context.register('ci4_msgs/Base4', MsgSpec(['ci2_msgs/Base2', 'ci3_msgs/Base3', 'ci4_msgs/Base'],
                                       ['data4a', 'data4b', 'data4c'],
                                       [], 'ci2_msgs/Base2 data4a\nci3_msgs/Base3 data4b\nci4_msgs/Base data4c\n'))

    msg_context.register('ci5_msgs/Base', MsgSpec(['time'], ['data'], [], 'time data\n'))

    assert ['import ci_msgs.msg'] == genpy.generator.compute_import('foo', 'ci_msgs/Base')
    assert ['import ci_msgs.msg'] == genpy.generator.compute_import('ci_msgs', 'ci_msgs/Base')
    assert ['import ci2_msgs.msg', 'import ci_msgs.msg'] == genpy.generator.compute_import('ci2_msgs', 'ci2_msgs/Base2')
    assert ['import ci2_msgs.msg', 'import ci_msgs.msg'] == genpy.generator.compute_import('foo', 'ci2_msgs/Base2')
    assert ['import ci3_msgs.msg', 'import ci2_msgs.msg', 'import ci_msgs.msg'] == genpy.generator.compute_import('ci3_msgs', 'ci3_msgs/Base3')

    assert set(['import ci4_msgs.msg', 'import ci3_msgs.msg', 'import ci2_msgs.msg', 'import ci_msgs.msg']) == set(genpy.generator.compute_import('foo', 'ci4_msgs/Base4'))
    assert set(['import ci4_msgs.msg', 'import ci3_msgs.msg', 'import ci2_msgs.msg', 'import ci_msgs.msg']) == set(genpy.generator.compute_import('ci4_msgs', 'ci4_msgs/Base4'))

    assert ['import ci4_msgs.msg'] == genpy.generator.compute_import('foo', 'ci4_msgs/Base')    
    assert ['import ci4_msgs.msg'] == genpy.generator.compute_import('ci4_msgs', 'ci4_msgs/Base')
    assert ['import ci4_msgs.msg'] == genpy.generator.compute_import('ci4_msgs', 'Base')

    assert ['import ci5_msgs.msg', 'import genpy'] == genpy.generator.compute_import('foo', 'ci5_msgs/Base')
        
def test_get_registered_ex():
    import genpy.generator
    s = MsgSpec(['string'], ['data'], [], 'string data\n')
    register('tgr_msgs/String', s)
    assert s == genpy.generator.get_registered_ex('tgr_msgs/String')
    try:
        genpy.generator.get_registered_ex('bad_msgs/String')
    except genpy.generator.MsgGenerationException: pass
            
def test_compute_constructor():
    import genpy.generator
    msg_context = MsgContext.create_default()
    msg_context.register('fake_msgs/String', MsgSpec(['string'], ['data'], [], 'string data\n'))
    msg_context.register('fake_msgs/ThreeNums', MsgSpec(['int32', 'int32', 'int32'], ['x', 'y', 'z'], [], 'int32 x\nint32 y\nint32 z\n'))

    # builtin specials
    assert 'genpy.Time()' == genpy.generator.compute_constructor('roslib', 'time')
    assert 'genpy.Duration()' == genpy.generator.compute_constructor('roslib', 'duration')
    assert 'std_msgs.msg._Header.Header()' == genpy.generator.compute_constructor('std_msgs', 'Header')

    assert 'genpy.Time()' == genpy.generator.compute_constructor('std_msgs', 'time')
    assert 'genpy.Duration()' == genpy.generator.compute_constructor('std_msgs', 'duration')

    # generic instances
    # - unregistered type
    assert None == genpy.generator.compute_constructor("unknown_msgs", "unknown_msgs/Foo")
    assert None == genpy.generator.compute_constructor("unknown_msgs", "Foo")
    # - wrong context
    assert None == genpy.generator.compute_constructor('std_msgs', 'ThreeNums')

    # - registered types
    assert 'fake_msgs.msg.String()' == genpy.generator.compute_constructor('std_msgs', 'fake_msgs/String')
    assert 'fake_msgs.msg.String()' == genpy.generator.compute_constructor('fake_msgs', 'fake_msgs/String')
    assert 'fake_msgs.msg.String()' == genpy.generator.compute_constructor('fake_msgs', 'String')
    assert 'fake_msgs.msg.ThreeNums()' == genpy.generator.compute_constructor('fake_msgs', 'fake_msgs/ThreeNums')
    assert 'fake_msgs.msg.ThreeNums()' == genpy.generator.compute_constructor('fake_msgs', 'fake_msgs/ThreeNums')
    assert 'fake_msgs.msg.ThreeNums()' == genpy.generator.compute_constructor('fake_msgs', 'ThreeNums')

def test_pack():
    import genpy.generator
    assert "buff.write(_struct_3lL3bB.pack(foo, bar))" == genpy.generator.pack('lllLbbbB', 'foo, bar')

def test_pack2():
    import genpy.generator
    assert 'buff.write(struct.pack(patt_name, foo, bar))' == genpy.generator.pack2('patt_name', 'foo, bar')

def test_unpack():
    import genpy.generator    
    assert "var_x = _struct_I3if2I.unpack(bname)" == genpy.generator.unpack('var_x', 'IiiifII', 'bname')

def test_unpack2():
    import genpy.generator    
    assert 'x = struct.unpack(patt, b)' == genpy.generator.unpack2('x', 'patt', 'b')

def test_generate_dynamic():
    import genpy
    import genpy.generator    
    msgs = genpy.generator.generate_dynamic("gd_msgs/EasyString", "string data\n")
    assert ['gd_msgs/EasyString'] == msgs.keys()
    m_cls = msgs['gd_msgs/EasyString']
    m_instance = m_cls()
    m_instance.data = 'foo'
    buff = cStringIO.StringIO()
    m_instance.serialize(buff)
    m_cls().deserialize(buff.getvalue())

    # 'probot_msgs' is a test for #1183, failure if the package no longer exists
    msgs = genpy.generator.generate_dynamic("gd_msgs/MoveArmState", """Header header
probot_msgs/ControllerStatus status

#Current arm configuration
probot_msgs/JointState[] configuration
#Goal arm configuration
probot_msgs/JointState[] goal

================================================================================
MSG: std_msgs/Header
#Standard metadata for higher-level flow data types
#sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.secs: seconds (stamp_secs) since epoch
# * stamp.nsecs: nanoseconds since stamp_secs
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: probot_msgs/ControllerStatus
# This message defines the expected format for Controller Statuss messages
# Embed this in the feedback state message of highlevel controllers
byte UNDEFINED=0
byte SUCCESS=1
byte ABORTED=2
byte PREEMPTED=3
byte ACTIVE=4

# Status of the controller = {UNDEFINED, SUCCESS, ABORTED, PREEMPTED, ACTIVE}
byte value

#Comment for debug
string comment
================================================================================
MSG: probot_msgs/JointState
string name
float64 position
float64 velocity
float64 applied_effort
float64 commanded_effort
byte is_calibrated

""")
    assert set(['gd_msgs/MoveArmState', 'probot_msgs/JointState', 'probot_msgs/ControllerStatus', 'std_msgs/Header']) ==  set(msgs.keys())
    m_instance1 = msgs['std_msgs/Header']() # make sure default constructor works
    m_instance2 = msgs['std_msgs/Header'](stamp=genpy.Time.from_sec(time.time()), frame_id='foo-%s'%time.time(), seq=12390)
    _test_ser_deser(m_instance2, m_instance1)

    m_instance1 = msgs['probot_msgs/ControllerStatus']()
    m_instance2 = msgs['probot_msgs/ControllerStatus'](value=4, comment=str(time.time()))
    d = {'UNDEFINED':0,'SUCCESS':1,'ABORTED':2,'PREEMPTED':3,'ACTIVE':4}
    for k, v in d.iteritems():
        assert v == getattr(m_instance1, k)
    _test_ser_deser(m_instance2, m_instance1)

    m_instance1 = msgs['probot_msgs/JointState']()
    m_instance2 = msgs['probot_msgs/JointState'](position=time.time(), velocity=time.time(), applied_effort=time.time(), commanded_effort=time.time(), is_calibrated=2)
    _test_ser_deser(m_instance2, m_instance1)

    m_instance1 = msgs['gd_msgs/MoveArmState']()
    js = msgs['probot_msgs/JointState']
    config = []
    goal = []
    # generate some data for config/goal
    for i in range(0, 10):
        config.append(js(position=time.time(), velocity=time.time(), applied_effort=time.time(), commanded_effort=time.time(), is_calibrated=2))
        goal.append(js(position=time.time(), velocity=time.time(), applied_effort=time.time(), commanded_effort=time.time(), is_calibrated=2))
    m_instance2 = msgs['gd_msgs/MoveArmState'](header=msgs['std_msgs/Header'](),
                                               status=msgs['probot_msgs/ControllerStatus'](),
                                               configuration=config, goal=goal)
    _test_ser_deser(m_instance2, m_instance1)

def _test_ser_deser(m_instance1, m_instance2):
    buff = cStringIO.StringIO()
    m_instance1.serialize(buff)
    m_instance2.deserialize(buff.getvalue())
    assert m_instance1 == m_instance2
        
def test_len_serializer_generator():
    import genpy.generator
    # generator tests are mainly tripwires/coverage tests
    # Test Serializers
    # string serializer simply initializes local var
    g = genpy.generator.len_serializer_generator('foo', True, True)
    assert 'length = len(foo)' == '\n'.join(g)
    # array len serializer writes var
    g = genpy.generator.len_serializer_generator('foo', False, True)        
    assert "length = len(foo)\nbuff.write(_struct_I.pack(length))" == '\n'.join(g)

    # Test Deserializers
    val = """start = end
end += 4
(length,) = _struct_I.unpack(str[start:end])"""
    # string serializer and array serializer are identical
    g = genpy.generator.len_serializer_generator('foo', True, False)
    assert val == '\n'.join(g)
    g = genpy.generator.len_serializer_generator('foo', False, False)        
    assert val == '\n'.join(g)

def test_string_serializer_generator():
    import genpy.generator
    # generator tests are mainly tripwires/coverage tests
    # Test Serializers
    g = genpy.generator.string_serializer_generator('foo', 'string', 'var_name', True)
    assert """length = len(var_name)
buff.write(struct.pack('<I%ss'%length, length, var_name.encode()))""" == '\n'.join(g)

    for t in ['uint8[]', 'byte[]', 'uint8[10]', 'byte[20]']:
        g = genpy.generator.string_serializer_generator('foo', 'uint8[]', 'b_name', True)
        assert """length = len(b_name)
# - if encoded as a list instead, serialize as bytes instead of string
if type(b_name) in [list, tuple]:
  buff.write(struct.pack('<I%sB'%length, length, *b_name))
else:
  buff.write(struct.pack('<I%ss'%length, length, b_name))""" == '\n'.join(g)

    # Test Deserializers
    val = """start = end
end += 4
(length,) = _struct_I.unpack(str[start:end])
start = end
end += length
var_name = str[start:end]"""
    # string serializer and array serializer are identical
    g = genpy.generator.string_serializer_generator('foo', 'string', 'var_name', False)
    assert val == '\n'.join(g)
