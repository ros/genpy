from __future__ import print_function

import os

from . base import MsgGenerationException

## :param type_name str: Name of message type sans package,
## e.g. 'String'
## :returns str: name of python module for auto-generated code
def _module_name(type_name):
    return "_"+type_name
    
def write_modules(package, files, srcdir, outdir):
    mfiles = map(lambda s: os.path.basename(os.path.splitext(s)[0]),
                 files)
    good_types = set([f[1:-3] for f in os.listdir(outdir)
                     if f.endswith('.py') and f != '__init__.py'])
    types = set(map(lambda s: os.path.basename(os.path.splitext(s)[0]),
                    files))
    generated_modules = [_module_name(f) for f in good_types.intersection(types)]
    write_module(outdir, package, generated_modules, srcdir)
    return 0

def write_module(basedir, package, generated_modules, srcdir):
    """
    Create a module file to mark directory for python

    :param base_dir: path to package, ``str``
    :param package: name of package to write module for, ``str``
    :param generated_modules: list of generated message modules,
      i.e. the names of the .py files that were generated for each
      .msg file. ``[str]``
    """
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    elif not os.path.isdir(basedir):
        raise MsgGenerationException("file preventing the creating of module directory: %s"%dir)
    p = os.path.join(basedir, '__init__.py')
    with open(p, 'w') as f:
        for mod in generated_modules:
            f.write('from %s import *\n'%mod)

    parent_init = os.path.dirname(basedir)
    p = os.path.join(parent_init, '__init__.py')
    if not os.path.exists(p):
        #touch __init__.py in the parent package
        with open(p, 'w') as f:
            print("import pkgutil, os.path", file=f)
            print("__path__ = pkgutil.extend_path(__path__, __name__)", file=f)
            if srcdir is not None:
                staticinit = '%s/%s/__init__.py' % (srcdir, package)
                print("if os.path.isfile('%s'): execfile('%s')" % (staticinit, staticinit), file=f)
