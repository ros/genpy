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

"""
ROS message source code generation for Python.

Converts ROS .srv files into Python source code implementations.
"""

import os
import sys
import traceback

import genmsg.msg_loader
import genmsg.gentools

import genpy
import genpy.generator

REQUEST ='Request'
RESPONSE='Response'

def srv_generator(msg_context, spec, search_path):
    name = spec.short_name
    req, resp = ["%s%s"%(name, suff) for suff in [REQUEST, RESPONSE]]

    fulltype = '%s/%s'%(package, name)

    genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    md5 = genmsg.compute_md5(msg_context, spec)

    yield "class %s(object):"%name
    yield "  _type          = '%s'"%fulltype
    yield "  _md5sum = '%s'"%md5
    yield "  _request_class  = %s"%req
    yield "  _response_class = %s"%resp

class SrvGenerator(genpy.generator.Generator):
    def __init__(self):
        super(SrvGenerator, self) \
            .__init__('gensrv_py', 'services')

    def generate(self, msg_context, package, f, outdir, search_path):
        verbose = True
        f = os.path.abspath(f)
        infile_name = os.path.basename(f)
        try:
            # you can't just check first... race condition
            os.makedirs(outdir)
        except OSError, e:
            if e.errno != 17: # file exists
                raise

        assert infile_name.endswith(genmsg.EXT_SRV)
        short_name = infile_name[:-len(genmsg.EXT_SRV)]
        # generate message files for request/response
        short_name = 'TODO'
        full_type = "%s/%s"%(package, short_name)
        spec = genmsg.msg_loader.load_srv_from_file(msg_context, f, full_type)
        
        outfile = genpy.generator.compute_outfile_name(outdir, infile_name, genmsg.EXT_SRV)
        with open(outfile, 'w') as f:
            for mspec in (spec.request, spec.response):
                for l in genpy.generator.msg_generator(msg_context, mspec, search_path):
                    f.write(l+'\n')

            # generate service file
            for l in srv_generator(msg_context, spec, search_path):
                f.write(l+'\n')
        return outfile
    
if __name__ == "__main__":
    import trace
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=0)
    tracer.run("genpy.generator.genmain(sys.argv, SrvGenerator())")
