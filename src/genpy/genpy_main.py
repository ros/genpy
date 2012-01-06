from __future__ import print_function

from optparse import OptionParser

import os
import sys
import traceback
import genmsg
import genmsg.command_line

from genmsg import MsgGenerationException
from . generate_initpy import write_modules

def usage(progname):
    print("%(progname)s file(s)"%vars())

def genmain(argv, progname, gen):
    parser = OptionParser("%s file"%(progname))
    parser.add_option('--initpy', dest='initpy', action='store_true',
                      default=False)
    parser.add_option('-p', dest='package')
    parser.add_option('-s', dest='srcdir')
    parser.add_option('-o', dest='outdir')
    parser.add_option('-I', dest='includepath', action='append')
    options, args = parser.parse_args(argv)
    try:
        if options.initpy:
            if options.outdir:
                retcode = write_modules(options.outdir)
            else:
                parser.error("Missing args")
        else:
            if len(args) < 2:
                parser.error("please specify args")
            if not os.path.exists(options.outdir):
                # This script can be run multiple times in parallel. We
                # don't mind if the makedirs call fails because somebody
                # else snuck in and created the directory before us.
                try:
                    os.makedirs(options.outdir)
                except OSError as e:
                    if not os.path.exists(options.outdir):
                        raise
            search_path = genmsg.command_line.includepath_to_dict(options.includepath)
            retcode = gen.generate_messages(options.package, args[1:], options.outdir, search_path)
    except genmsg.InvalidMsgSpec as e:
        print("ERROR: ", e, file=sys.stderr)
        retcode = 1
    except MsgGenerationException as e:
        print("ERROR: ", e, file=sys.stderr)
        retcode = 2
    except Exception as e:
        traceback.print_exc()
        print("ERROR: ",e)
        retcode = 3
    sys.exit(retcode or 0)
