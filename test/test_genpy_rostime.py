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

import unittest
import warnings


class RostimeTest(unittest.TestCase):

    def test_TVal(self, TVal=None, test_neg=True):
        import genpy.rostime
        if TVal is None:
            # cannot set as default arg because --cov option reloads the module and causes
            # spurious failure
            TVal = genpy.rostime.TVal
        # test constructor
        # - test zero
        v = TVal()
        self.assert_(repr(v))
        self.assert_(str(v))
        self.assertEqual(0, v.secs)
        self.assertEqual(0, v.nsecs)
        self.assertFalse(v) # test __zero__
        self.assert_(v.is_zero())
        self.assertEqual('0', str(v))
        self.assertEqual(0, v.to_nsec())
        self.assertEqual(0, v.to_sec())

        self.assertEqual(v, v)
        self.assertEqual(v, TVal())
        self.assertEqual(v, TVal(0))
        self.assertEqual(v, TVal(0, 0))
        self.assertEqual(v.__hash__(), TVal(0, 0).__hash__())

        self.assert_(v != TVal(0,1))
        self.assert_(v >= TVal())
        self.assert_(v <= TVal())
        self.assert_(v < TVal(0,1))
        self.assert_(TVal(0,1) > v)
        v.set(0, 0)
        self.assertEqual(0, v.secs)
        self.assertEqual(0, v.nsecs)
        v.set(1, 0)
        self.assertEqual(1, v.secs)
        self.assertEqual(0, v.nsecs)
        v.set(0, 1)
        self.assertEqual(0, v.secs)
        self.assertEqual(1, v.nsecs)
        # - set does _not_ canonicalize
        v.set(0, 1000000000)
        self.assertEqual(0, v.secs)
        self.assertEqual(1000000000, v.nsecs)
        v.canon()
        self.assertEqual(1, v.secs)
        self.assertEqual(0, v.nsecs)

        # - test seconds
        v = TVal(1)
        self.assertEqual(1, v.secs)
        self.assertEqual(0, v.nsecs)
        self.assert_(v) # test __zero__
        self.assertFalse(v.is_zero())
        self.assertEqual('1000000000', str(v))
        self.assertEqual(1000000000, v.to_nsec())
        self.assertEqual(v, v)
        self.assertEqual(v, TVal(1))
        self.assertEqual(v, TVal(1, 0))
        self.assertEqual(v, TVal(0,1000000000))
        self.assertEqual(v.__hash__(), TVal(0,1000000000).__hash__())
        self.assertNotEquals(v, TVal(0, 0))
        self.assertNotEquals(v.__hash__(), TVal(0, 0).__hash__())
        self.assertEqual(NotImplemented, v.__ge__(0))
        class Foo(object): pass
        self.assertEqual(NotImplemented, v.__gt__(Foo()))
        self.assertEqual(NotImplemented, v.__ge__(Foo()))
        self.assertEqual(NotImplemented, v.__le__(Foo()))
        self.assertEqual(NotImplemented, v.__lt__(Foo()))
        self.assertFalse(v.__eq__(Foo()))
        self.assert_(v.__ne__(Foo()))
        self.assert_(v >= TVal())
        self.assert_(v <= TVal(1))
        self.assert_(v <= TVal(1,0))
        self.assert_(v <= TVal(2,0))
        self.assert_(v < TVal(2))
        self.assert_(v < TVal(1,1))
        self.assert_(TVal(1,1) > v)
        self.assert_(TVal(2) > v)
        # - test ns
        v = TVal(0, 1)
        self.assertEqual(0, v.secs)
        self.assertEqual(1, v.nsecs)
        self.assert_(v) # test __zero__
        self.assertFalse(v.is_zero())
        self.assertEqual('1', str(v))
        self.assertEqual(1, v.to_nsec())
        self.assertEqual(v, v)
        self.assertEqual(v, TVal(0,1))
        self.assertNotEquals(v, TVal(0, 0))
        self.assert_(v >= TVal())
        self.assert_(v <= TVal(1))
        self.assert_(v <= TVal(0,1))
        self.assert_(v <= TVal(2,0))
        self.assert_(v < TVal(0,2))
        self.assert_(v < TVal(1))
        self.assert_(TVal(1) > v)
        self.assert_(TVal(0,2) > v)
        # - test canon
        v = TVal(1, 1000000000)
        self.assertEqual(2, v.secs)
        self.assertEqual(0, v.nsecs)
        self.assertEqual(2, v.to_sec())
        self.assertEqual(2000000000, v.to_nsec())

        v = TVal(1, 1000000001)
        self.assertEqual(2, v.secs)
        self.assertEqual(1, v.nsecs)
        self.assertEqual(2.000000001, v.to_sec())
        self.assertEqual(2000000001, v.to_nsec())

        v = TVal(1, -1000000000)
        self.assertEqual(0, v.secs)
        self.assertEqual(0, v.nsecs)
        v = TVal(1, -999999999)
        self.assertEqual(0, v.secs)
        self.assertEqual(1, v.nsecs)
        self.assertEqual(0.000000001, v.to_sec())
        self.assertEqual(1, v.to_nsec())

        if test_neg:
            v = TVal(-1, -1000000000)
            self.assertEqual(-2, v.secs)
            self.assertEqual(0, v.nsecs)
            self.assertEqual(-2, v.to_sec())
            self.assertEqual(-2000000000, v.to_nsec())

            v = TVal(-2, 1000000000)
            self.assertEqual(-1, v.secs)
            self.assertEqual(0, v.nsecs)
            self.assertEqual(-1, v.to_sec())
            self.assertEqual(-1000000000, v.to_nsec())


        # test some more hashes
        self.assertEqual(TVal(1).__hash__(), TVal(1).__hash__())
        self.assertEqual(TVal(1,1).__hash__(), TVal(1,1).__hash__())
        self.assertNotEquals(TVal(1).__hash__(), TVal(2).__hash__())
        self.assertNotEquals(TVal(1,1).__hash__(), TVal(1,2).__hash__())
        self.assertNotEquals(TVal(1,1).__hash__(), TVal(2,1).__hash__())

    def test_Time(self):
        from genpy.rostime import Time, Duration
        self.test_TVal(TVal=Time, test_neg=False)

        # #1600 Duration > Time should fail
        failed = False
        try:
          v = Duration.from_sec(0.1) > Time.from_sec(0.5)
          failed = True
        except: pass
        self.assertFalse(failed, "should have failed to compare")
        try:
          v = Time.from_sec(0.4) > Duration.from_sec(0.1)
          failed = True
        except: pass
        self.assertFalse(failed, "should have failed to compare")

        # TODO: sub

        # neg time fails
        try:
            Time(-1)
            failed = True
        except: pass
        self.assertFalse(failed, "negative time not allowed")
        try:
            Time(1, -1000000001)
            failed = True
        except: pass
        self.assertFalse(failed, "negative time not allowed")

        # test Time.now() is within 10 seconds of actual time (really generous)
        import time
        t = time.time()
        v = Time.from_sec(t)
        self.assertEqual(v.to_sec(), t)
        # test from_sec()
        self.assertEqual(Time.from_sec(0), Time())
        self.assertEqual(Time.from_sec(1.), Time(1))
        self.assertEqual(Time.from_sec(v.to_sec()), v)
        self.assertEqual(v.from_sec(v.to_sec()), v)
        # test to_time()
        self.assertEqual(v.to_sec(), v.to_time())

        # test addition
        # - time + time fails
        try:
            v = Time(1,0) + Time(1, 0)
            failed = True
        except: pass
        self.assertFalse(failed, "Time + Time must fail")

        # - time + duration
        v = Time(1,0) + Duration(1, 0)
        self.assertEqual(Time(2, 0), v)
        v = Duration(1, 0) + Time(1,0)
        self.assertEqual(Time(2, 0), v)
        v = Time(1,1) + Duration(1, 1)
        self.assertEqual(Time(2, 2), v)
        v = Duration(1, 1) + Time(1,1)
        self.assertEqual(Time(2, 2), v)

        v = Time(1) + Duration(0, 1000000000)
        self.assertEqual(Time(2), v)
        v = Duration(1) + Time(0, 1000000000)
        self.assertEqual(Time(2), v)

        v = Time(100, 100) + Duration(300)
        self.assertEqual(Time(400, 100), v)
        v = Duration(300) + Time(100, 100)
        self.assertEqual(Time(400, 100), v)

        v = Time(100, 100) + Duration(300, 300)
        self.assertEqual(Time(400, 400), v)
        v = Duration(300, 300) + Time(100, 100)
        self.assertEqual(Time(400, 400), v)

        v = Time(100, 100) + Duration(300, -101)
        self.assertEqual(Time(399, 999999999), v)
        v =  Duration(300, -101) + Time(100, 100)
        self.assertEqual(Time(399, 999999999), v)

        # test subtraction
        try:
            v = Time(1,0) - 1
            failed = True
        except: pass
        self.assertFalse(failed, "Time - non Duration must fail")
        class Foob(object): pass
        try:
            v = Time(1,0) - Foob()
            failed = True
        except: pass
        self.assertFalse(failed, "Time - non TVal must fail")

        # - Time - Duration
        v = Time(1,0) - Duration(1, 0)
        self.assertEqual(Time(), v)

        v = Time(1,1) - Duration(-1, -1)
        self.assertEqual(Time(2, 2), v)
        v = Time(1) - Duration(0, 1000000000)
        self.assertEqual(Time(), v)
        v = Time(2) - Duration(0, 1000000000)
        self.assertEqual(Time(1), v)
        v = Time(400, 100) - Duration(300)
        self.assertEqual(Time(100, 100), v)
        v = Time(100, 100) - Duration(0, 101)
        self.assertEqual(Time(99, 999999999), v)

        # - Time - Time = Duration
        v = Time(100, 100) - Time(100, 100)
        self.assertEqual(Duration(), v)
        v = Time(100, 100) - Time(100)
        self.assertEqual(Duration(0,100), v)
        v = Time(100) - Time(200)
        self.assertEqual(Duration(-100), v)

        # Time (float secs) vs. Time(int, int)
        self.assertEqual(Time.from_sec(0.5), Time(0.5))
        t = Time(0.5)
        self.assert_(type(t.secs) == int)
        self.assertEqual(0, t.secs)
        self.assertEqual(500000000, t.nsecs)

        try:
            Time(0.5, 0.5)
            self.fail("should have thrown value error")
        except ValueError: pass

    def test_Duration(self):
        from genpy.rostime import Time, Duration

        self.test_TVal(TVal=Duration, test_neg=True)

        # test from_sec
        v = Duration(1000)
        self.assertEqual(v, Duration.from_sec(v.to_sec()))
        self.assertEqual(v, v.from_sec(v.to_sec()))
        v = Duration(0,1000)
        self.assertEqual(v, Duration.from_sec(v.to_sec()))
        self.assertEqual(v, v.from_sec(v.to_sec()))

        # test neg
        v = -Duration(1, -1)
        self.assertEqual(-1, v.secs)
        self.assertEqual(1, v.nsecs)
        v = -Duration(-1, -1)
        self.assertEqual(1, v.secs)
        self.assertEqual(1, v.nsecs)
        v = -Duration(-1, 1)
        self.assertEqual(0, v.secs)
        self.assertEqual(999999999, v.nsecs)

        # test addition
        self.assertEqual(Duration(1,0) + Time(1, 0), Time(2, 0))
        failed = False
        try:
            v = Duration(1,0) + 1
            failed = True
        except: pass
        self.assertFalse(failed, "Duration + int must fail")

        v = Duration(1,0) + Duration(1, 0)
        self.assertEqual(2, v.secs)
        self.assertEqual(0, v.nsecs)
        self.assertEqual(Duration(2, 0), v)
        v = Duration(-1,-1) + Duration(1, 1)
        self.assertEqual(0, v.secs)
        self.assertEqual(0, v.nsecs)
        self.assertEqual(Duration(), v)
        v = Duration(1) + Duration(0, 1000000000)
        self.assertEqual(2, v.secs)
        self.assertEqual(0, v.nsecs)
        self.assertEqual(Duration(2), v)
        v = Duration(100, 100) + Duration(300)
        self.assertEqual(Duration(400, 100), v)
        v = Duration(100, 100) + Duration(300, 300)
        self.assertEqual(Duration(400, 400), v)
        v = Duration(100, 100) + Duration(300, -101)
        self.assertEqual(Duration(399, 999999999), v)

        # test subtraction
        try:
            v = Duration(1,0) - 1
            failed = True
        except: pass
        self.assertFalse(failed, "Duration - non duration must fail")
        try:
            v = Duration(1, 0) - Time(1,0)
            failed = True
        except: pass
        self.assertFalse(failed, "Duration - Time must fail")

        v = Duration(1,0) - Duration(1, 0)
        self.assertEqual(Duration(), v)
        v = Duration(-1,-1) - Duration(1, 1)
        self.assertEqual(Duration(-3, 999999998), v)
        v = Duration(1) - Duration(0, 1000000000)
        self.assertEqual(Duration(), v)
        v = Duration(2) - Duration(0, 1000000000)
        self.assertEqual(Duration(1), v)
        v = Duration(100, 100) - Duration(300)
        self.assertEqual(Duration(-200, 100), v)
        v = Duration(100, 100) - Duration(300, 101)
        self.assertEqual(Duration(-201, 999999999), v)

        # test abs
        self.assertEqual(abs(Duration()), Duration())
        self.assertEqual(abs(Duration(1)), Duration(1))
        self.assertEqual(abs(Duration(-1)), Duration(1))
        self.assertEqual(abs(Duration(0,-1)), Duration(0,1))
        self.assertEqual(abs(Duration(-1,-1)), Duration(1,1))
        self.assertEqual(abs(Duration(0,1)), Duration(0,1))

        # Duration (float secs) vs. Duration(int, int)
        self.assertEqual(Duration.from_sec(0.5), Duration(0.5))
        t = Duration(0.5)
        self.assert_(type(t.secs) == int)
        self.assertEqual(0, t.secs)
        self.assertEqual(500000000, t.nsecs)

        try:
            Duration(0.5, 0.5)
            self.fail("should have thrown value error")
        except ValueError: pass

        # Test mul
        self.assertEqual(Duration(4), Duration(2) * 2)
        self.assertEqual(Duration(4), Duration(2) * 2.)
        self.assertEqual(Duration(4), 2 * Duration(2))
        self.assertEqual(Duration(4), 2. * Duration(2))
        self.assertEqual(Duration(10), Duration(4) * 2.5)
        self.assertEqual(Duration(4, 8), Duration(2, 4) * 2)
        v = Duration(4, 8) - (Duration(2, 4) * 2.)
        self.assert_(abs(v.to_nsec()) < 100)
        v = Duration(5, 10) - (Duration(2, 4) * 2.5)
        self.assert_(abs(v.to_nsec()) < 100)

        # Test div
        self.assertEqual(Duration(4), Duration(8) / 2)
        self.assertEqual(Duration(4), Duration(8) / 2.)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.assertEqual(Duration(4), Duration(8) // 2)
            self.assertEqual(Duration(4), Duration(8) // 2.)
            self.assertEqual(Duration(4), Duration(9) // 2)
            self.assertEqual(Duration(4), Duration(9) // 2.)
            self.assertEqual(len(w), 0)
        self.assertEqual(Duration(4, 2), Duration(8, 4) / 2)
        v = Duration(4, 2) - (Duration(8, 4) / 2.)
        self.assert_(abs(v.to_nsec()) < 100)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.assertEqual(Duration(4, 0), Duration(8, 4) // 2)
            self.assertEqual(Duration(4, 0), Duration(9, 5) // 2)
            v = Duration(4, 2) - (Duration(9, 5) // 2.)
            self.assertTrue(abs(v.to_nsec()) < 100)
            self.assertEqual(len(w), 0)
