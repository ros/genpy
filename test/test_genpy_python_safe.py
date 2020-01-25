import traceback
import unittest


class MessageTest(unittest.TestCase):

    def test_python_safe_message(self):
        # simple test for make_python_safe
        try:
            # this import will fail, if the data field "from" is not properly properly renames, since "from" is a reserved keyword in Python
            from genpy.msg import TestPythonSafe  # noqa: F401
        except Exception:
            # assert False, "should have raised"
            self.fail("failed to import message type 'TestPythonSafe':\n%s" % (traceback.format_exc()))

    def test_python_safe_message_with_subfields(self):
        # regression test for https://github.com/ros/genpy/issues/68
        try:
            # this import will fail, if the make_python_safe function is not properly used on all subfields of the message
            from genpy.msg import TestPythonSafeSubfields  # noqa: F401
        except Exception:
            self.fail("failed to import message type 'TestPythonSafeSubfields':\n%s" % (traceback.format_exc()))
