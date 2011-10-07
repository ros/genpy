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

import genmsg.gentools
import genmsg.srvs

import genpy
import genpy.generator

REQUEST ='Request'
RESPONSE='Response'

def srv_generator(package, name, spec, includepath):
    req, resp = ["%s%s"%(name, suff) for suff in [REQUEST, RESPONSE]]

    fulltype = '%s/%s'%(package, name)

    gendeps_dict = genmsg.gentools.get_dependencies(spec, package, includepath)
    md5 = genmsg.gentools.compute_md5(gendeps_dict, includepath)

    yield "class %s(object):"%name
    yield "  _type          = '%s'"%fulltype
    yield "  _md5sum = '%s'"%md5
    yield "  _request_class  = %s"%req
    yield "  _response_class = %s"%resp

class SrvGenerator(genpy.generator.Generator):
    def __init__(self):
        super(SrvGenerator, self) \
            .__init__('gensrv_py', 'services', genmsg.EXT_SRV, 
                      'srv')

    def generate(self, package, f, outdir, incpath):
        verbose = True
        f = os.path.abspath(f)
        infile_name = os.path.basename(f)
        try:
            # you can't just check first... race condition
            os.makedirs(outdir)
        except OSError, e:
            if e.errno != 17: # file exists
                raise

        prefix = infile_name[:-len(genmsg.srvs.EXT)]
        # generate message files for request/response        
        name, spec = genmsg.srvs.load_from_file(f, package)
        base_name = genmsg.resource_name_base(name)
        
        outfile = self.outfile_name(outdir, f)
        f = open(outfile, 'w')
        try:
            for mspec, suffix in ((spec.request, REQUEST), (spec.response, RESPONSE)):
                for l in genpy.generator.msg_generator(package, base_name+suffix, mspec, incpath):
                    f.write(l+'\n')

            # generate service file
            for l in srv_generator(package, base_name, spec, incpath):
                f.write(l+'\n')
        finally:
            f.close()
        return outfile
    
if __name__ == "__main__":
    import trace
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=0)
    tracer.run("genpy.generator.genmain(sys.argv, SrvGenerator())")
