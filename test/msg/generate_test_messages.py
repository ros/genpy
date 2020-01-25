import os
import sys

pkg_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(pkg_path, 'src'))

from genpy.generator import MsgGenerator  # noqa
from genpy.genpy_main import genmain  # noqa


def generate_test_messages(msg_files):
    test_msg_path = os.path.join(pkg_path, 'test/msg')
    msg_files = []
    for filename in os.listdir(test_msg_path):
        if filename.endswith('.msg'):
            msg_files.append(filename)

    src_msg_path = os.path.join(pkg_path, 'src/genpy/msg')
    if not os.path.exists(src_msg_path):
        os.makedirs(src_msg_path)

    with open(os.path.join(src_msg_path, '__init__.py'), 'w') as h:
        for msg_file in msg_files:
            h.write('from ._%s import *\n' % msg_file[:-4])

    for msg_file in msg_files:
        argv = [
            'genmsg_py.py',
            '-p', 'genpy',
            '-Igenpy:%s/test/msg' % pkg_path,
            '-o', '%s/src/genpy/msg' % pkg_path,
            '%s/test/msg/%s' % (pkg_path, msg_file),
        ]
        try:
            genmain(argv, 'genmsg_py.py', MsgGenerator())
        except SystemExit as e:
            if e.code:
                raise


if __name__ == '__main__':
    generate_test_messages(sys.argv[1:])
