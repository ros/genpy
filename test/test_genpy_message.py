# Software License Agreement (BSD License)
#
# Copyright (c) 2009, Willow Garage, Inc.
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

import os
import sys
import time
import unittest
import traceback
import yaml

import genpy.message
import genpy
from genpy import Time, Duration

# Not much to test, just tripwires

class MessageTest(unittest.TestCase):
    
    def xtest_check_types_Header(self):
        # #2128: test that check_types works with a Header
        # #message. This is a weird case because Header has an aliased
        # #type and is the only ROS type for which that is true
        from test_roslib_comm.msg import HeaderTest
        x = HeaderTest()
        x._check_types()
        
    def test_Message_check_types(self):
        # test on a generated message
        # - use UInt16MultiArray because it has an embedded MultiArrayLayout
        from std_msgs.msg import String, UInt16MultiArray, MultiArrayLayout, MultiArrayDimension
        from genpy import SerializationError
        # not checking overflow in this test
        correct = [String(), String('foo'), String(''), String(data='data'),
                   UInt16MultiArray(),
                   UInt16MultiArray(MultiArrayLayout(), []), 
                   UInt16MultiArray(MultiArrayLayout(data_offset=1), [1, 2, 3]),         
                   UInt16MultiArray(layout=MultiArrayLayout(data_offset=1)),
                   UInt16MultiArray(layout=MultiArrayLayout(dim=[])),                   
                   UInt16MultiArray(layout=MultiArrayLayout(dim=[MultiArrayDimension()])),                   
                   UInt16MultiArray(data=[1, 2, 3]),
                   ]
        for t in correct:
            t._check_types()
        for t in correct:
            try:
                t._check_types(exc=Exception())
                self.fail("should have raised wrapped exc")
            except SerializationError:
                pass

        wrong = [String(1), String(data=1),
                 UInt16MultiArray(1, []),                 
                 UInt16MultiArray(MultiArrayLayout(), 1),
                 UInt16MultiArray(String(), []),
                 UInt16MultiArray(layout=MultiArrayLayout(dim=[1])),  
                 UInt16MultiArray(layout=MultiArrayLayout(data_offset='')),  
                 ]
        for t in wrong:
            try:
                t._check_types()
                self.fail("should have raised")
            except SerializationError:
                pass

    def test_check_types_valid(self):
        '''Test directly a bunch of valid combinations to check_types.

        check_type will throw an exception when it fails
        '''
        genpy.message.check_type('test', 'uint8[]', 'byteDataIsAStringInPy')
        genpy.message.check_type('test', 'char[]', 'byteDataIsAStringInPy')
        genpy.message.check_type('test', 'uint8[]', [3,4,5])
        genpy.message.check_type('test', 'uint8[]', (3,4,5))
        genpy.message.check_type('test', 'char[]', [3,4,5])
        genpy.message.check_type('test', 'int32[]', [3,4,5])
        genpy.message.check_type('test', 'int32', -5)
        genpy.message.check_type('test', 'int64', -5)
        genpy.message.check_type('test', 'int16', -5)
        genpy.message.check_type('test', 'int8', -5)
        genpy.message.check_type('test', 'uint32', 5)
        genpy.message.check_type('test', 'uint64', 5)
        genpy.message.check_type('test', 'uint16', 5)
        genpy.message.check_type('test', 'uint8', 5)
        genpy.message.check_type('test', 'bool', True)
        genpy.message.check_type('test', 'bool', False)
        genpy.message.check_type('test', 'bool', 0)
        genpy.message.check_type('test', 'bool', 1)
        genpy.message.check_type('test', 'string', 'IAmAString')
        genpy.message.check_type('test', 'time', Time())
        genpy.message.check_type('test', 'duration', Duration(5))

    def test_check_types_invalid(self):
        from genpy import SerializationError
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'int32[]', 'someString')
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'uint32[]', [3, -2, 4])
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'uint8', -2)
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'uint16', -2)
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'uint32', -2)
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'uint64', -2)
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'bool', -2)
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'bool', 2)
        self.assertRaises(SerializationError, genpy.message.check_type,
                          'test', 'string', u'UnicodeString')
        
    def test_Message(self):
        import cStringIO
        from genpy import Message, SerializationError
        self.assert_(isinstance(Message(), Message))
        m = Message()
        b = cStringIO.StringIO()
        m.serialize(b)
        m.deserialize('')

        # test args/keywords constructor
        try:
            Message(1, 2, 3, one=1, two=2, three=3)
            self.fail("Message should not allow *args and **kwds")
        except TypeError: pass
        try:
            Message()._get_types()
            self.fail("_get_types() should not be callable on abstract Message instance")
        except: pass

        # test Empty message
        class M1(Message):
            __slots__ = []
            _slot_types=[]
            def __init__(self, *args, **kwds):
                super(M1, self).__init__(*args, **kwds)
            def _get_types(self): return []
            
        # - test __str__ on empty
        self.assertEquals('', str(M1()))
        # - should not fail on default constructor
        M1()._check_types()
        # - must fail if provided an exception
        try:
            M1()._check_types(Exception("test"))
            self.fail("_check_types must fail if explicitly provided an exception")
        except SerializationError: pass

        # Test simple message with two fields
        class M2(Message):
            __slots__ = ['a', 'b']
            _slot_types=['int32', 'int32']
            def _get_types(self): return ['int32', 'int32']
            def __init__(self, *args, **kwds):
                super(M2, self).__init__(*args, **kwds)
        self.assertEquals('a: 1\nb: 2', str(M2(1, 2)))
        # - test check types with two int type
        M2(1, 2)._check_types()
        M2(a=1, b=2)._check_types()
        invalid = [M2(a=1), M2('1', '2'), M2(1, '2'), M2(1., 2.), M2(None, 2)]
        for m in invalid:
            try:
                m._check_types()
                self.fail("check_types for %s should have failed"%m)
            except SerializationError: pass
        
        
        valid = [
            ((), {}, M1),
            ((), {}, M2),
            ((1, 2), {}, M2),
            ((), {'a': 1, 'b': 2}, M2),
            ((), {'a': 1}, M2),((), {'b': 2}, M2),
            ]
        invalid = [
            ((1,), {}, M1),
            ((), {'one': 1}, M1),
            ((1), {}, M2),((1, 2, 3), {}, M2),
            ((), {'c': 1}, M2),((), {'a': 1, 'b': 2, 'c': 1}, M2),
            ]
        for args, kwds, cls in valid:
            cls(*args, **kwds)
        val = time.time()
        val2 = time.time()
        self.assertEquals(val, M2(val, 2).a)
        self.assertEquals(val, M2(1, val).b)
        self.assertEquals(val, M2(a=val).a)
        self.assertEquals(None, M2(a=val).b)
        self.assertEquals(None, M2(b=val).a)
        self.assertEquals(val, M2(b=val).b)
        self.assertEquals(val, M2(a=val, b=val2).a)
        self.assertEquals(val2, M2(a=val, b=val2).b)
        for args, kwds, cls in invalid:
            try:
                cls(*args, **kwds)
                self.fail("Message should have failed for cls[%s] *args[%s] and **kwds[%s]"%(cls, args, kwds))
            except: pass
        
    def test_strify_message(self):
        # this is a bit overtuned, but it will catch regressions
        from genpy.message import Message, strify_message
        class M1(Message):
            __slots__ = []
            _slot_types = []
            def __init__(self): pass
        self.assertEquals('', strify_message(M1()))
        class M2(Message):
            __slots__ = ['str', 'int', 'float', 'bool', 'list']
            _slot_types = ['string', 'int32', 'float32', 'bool', 'int32[]']            
            def __init__(self, str_, int_, float_, bool_, list_):
                self.str = str_
                self.int = int_       
                self.float = float_
                self.bool = bool_
                self.list = list_
                
        self.assertEquals("""str: string
int: 123456789101112
float: 5678.0
bool: True
list: [1, 2, 3]""", strify_message(M2('string', 123456789101112, 5678., True, [1,2,3])))
        
        self.assertEquals("""str: ''
int: -1
float: 0.0
bool: False
list: []""", strify_message(M2('', -1, 0., False, [])))

        class M3(Message):
            __slots__ = ['m2']
            _slot_types=['M1']
            def __init__(self, m2):
                self.m2 = m2
        self.assertEquals("""m2: 
  str: string
  int: -1
  float: 0.0
  bool: False
  list: []""", strify_message(M3(M2('string', -1, 0., False, []))))

        # test array of Messages field
        class M4(Message):
            __slots__ = ['m2s']
            _slot_types=['M2[]']
            def __init__(self, m2s):
                self.m2s = m2s
                
        self.assertEquals("""m2s: 
  - 
    str: string
    int: 1234
    float: 5678.0
    bool: True
    list: [1, 2, 3]
  - 
    str: string
    int: -1
    float: 0.0
    bool: False
    list: []""", strify_message(M4([
                        M2('string', 1234, 5678., True, [1,2,3]),
                        M2('string', -1, 0., False, []),
                        ])))
        # test Time and Duration
        from genpy import Time, Duration
        class M5(Message):
            __slots__ = ['t', 'd']
            _slot_types=['time', 'duration']
            def __init__(self, t, d):
                self.t = t
                self.d = d        
        self.assertEquals("""t: 
  secs: 987
  nsecs: 654
d: 
  secs: 123
  nsecs: 456""", strify_message(M5(Time(987, 654), Duration(123, 456))))
        
        # test final clause of strify -- str anything that isn't recognized
        self.assertEquals("set([1])", strify_message(set([1])))

    def test_strify_yaml(self):
        def roundtrip(m):
            yaml_text = strify_message(m)
            print yaml_text
            loaded = yaml.load(yaml_text) 
            print "loaded", loaded
            new_inst = m.__class__()
            if loaded is not None:
                fill_message_args(new_inst, [loaded])
            else:
                fill_message_args(new_inst, [])                
            return new_inst

        # test YAML roundtrip. strify_message doesn't promise this
        # yet, but want to use it in this way in some demo toolchains
        from genpy.message import Message, strify_message, fill_message_args
        class M1(Message):
            __slots__ = []
            _slot_types=[]
            def __init__(self): pass
        self.assertEquals(M1(), roundtrip(M1()))
        
        class M2(Message):
            __slots__ = ['str', 'int', 'float', 'bool', 'list']
            _slot_types = ['string', 'int32', 'float32', 'bool', 'int32[]'] 
            def __init__(self, str_=None, int_=None, float_=None, bool_=None, list_=None):
                self.str = str_
                self.int = int_       
                self.float = float_
                self.bool = bool_
                self.list = list_
                
        val = M2('string', 123456789101112, 5678., True, [1,2,3])
        self.assertEquals(val, roundtrip(val))
        # test with empty string and empty list
        val = M2('', -1, 0., False, [])
        self.assertEquals(val, roundtrip(val))
        
        class M3(Message):
            __slots__ = ['m2']
            _slot_types=['test_roslib/M2']
            def __init__(self, m2=None):
                self.m2 = m2 or M2()
                
        val = M3(M2('string', -1, 0., False, []))
        self.assertEquals(val, roundtrip(val))

        # test array of Messages field. We can't use M4 or M5 because fill_message_args has to instantiate the embedded type
        if 0:
            from test_roslib_comm.msg import ArrayOfMsgs
            from std_msgs.msg import String, Time, MultiArrayLayout, MultiArrayDimension
            dims1 = [MultiArrayDimension(*args) for args in [('', 0, 0), ('x', 1, 2), ('y of z', 3, 4)]]
            dims2 = [MultiArrayDimension('hello world', 91280, 1983274)]
            times = [Time(genpy.Time(*args)) for args in [(0,), (12345, 6789), (1, 1)]]
            val = ArrayOfMsgs([String(''), String('foo'), String('bar of soap')],
                              times,
                              [MultiArrayLayout(dims1, 0), MultiArrayLayout(dims2, 12354)],
                              )
            self.assertEquals(val, roundtrip(val))
        

    def test_check_type(self):
        # check_type() currently does not do harder checks like
        # type-checking class types.  as soon as it does, it will need
        # test to validate this.
        from genpy.message import check_type, SerializationError
        from genpy import Time, Duration
        valids = [
            ('byte', 1), ('byte', -1),
            ('string', ''), ('string', 'a string of text'),
            ('int32[]', []),
            ('int32[]', [1, 2, 3, 4]),
            ('time', Time()), ('time', Time.from_sec(1.0)),
            ('time', Time(10000)), ('time', Time(1000, -100)),
            ('duration', Duration()),('duration', Duration()), 
            ('duration', Duration(100)), ('duration', Duration(-100, -100)),
                  ]

        for t, v in valids:
            try:
                check_type('n', t, v)
            except Exception, e:
                traceback.print_exc()
                raise Exception("failure type[%s] value[%s]: %s"%(t, v, str(e)))

        invalids = [
            ('byte', 129), ('byte', -129), ('byte', 'byte'), ('byte', 1.0),
            ('string', 1),
            ('uint32', -1),
            ('int8', 112312), ('int8', -112312),
            ('uint8', -1), ('uint8', 112312),
            ('int32', '1'), ('int32', 1.),
            ('int32[]', 1), ('int32[]', [1., 2.]), ('int32[]', [1, 2.]), 
            ('duration', 1), ('time', 1),            
            ]
        for t, v in invalids:
            try:
                check_type('n', t, v)
                self.fail("check_type[%s, %s] should have failed"%(t, v))
            except SerializationError: pass
    
