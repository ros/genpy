#!/usr/bin/env python
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
#
# Revision $Id: genmsg_py.py 9002 2010-04-09 01:08:47Z kwc $

"""
ROS message source code generation for Python

Converts ROS .msg files in a package into Python source code implementations.
"""
import os
import sys

import genmsg
import genmsg.msg_loader

import genpy
import genpy.generator

class GenmsgPackage(genpy.generator.Generator):
    """
    GenmsgPackage generates Python message code for all messages in a
    package. See genutil.Generator. In order to generator code for a
    single .msg file, see msg_generator.
    """
    def __init__(self):
        super(GenmsgPackage, self).__init__(
            'genmsg_py', 'messages')

    def generate(self, msg_context, package, f, outdir, search_path):
        """
        Generate python message code for a single .msg file
        :param f: path to .msg file, ``str``
        :param outdir: output directory for generated code, ``str``
        :returns: filename of generated Python code, ``str``
        """
        # TODO: it would be better of generator did not do type name calculation
        verbose = True
        assert f.endswith(genmsg.EXT_MSG), f

        f = os.path.abspath(f)
        infile_name = os.path.basename(f)
        outfile_name = genpy.generator.compute_outfile_name(outdir, infile_name, genmsg.EXT_MSG)

        short_name = infile_name[:-len(genmsg.EXT_MSG)]
        full_name = '%s/%s'%(package, short_name)
        spec = genmsg.msg_loader.load_msg_from_file(msg_context, f, full_name)
        gen = genpy.generator.msg_generator(msg_context, spec, search_path)
        self.write_gen(outfile_name, gen, verbose)
        msg_context.register(full_name, spec)
        return outfile_name

if __name__ == "__main__":
    genpy.generator.genmain(sys.argv, GenmsgPackage())
    
