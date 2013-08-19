"""
    This script allows to build python-independent executable
    on win32 platform to use on systems with no Python interpreter
    installed.

    To build EXE file make sure to install py2exe library and issue
    the following command:
    
        python setup.py py2exe

    This command will create the following directories:
    
        build   contains build related files, temporary
        
        dist    contains files that can be moved to another system
                with no Python interpreter installed.

    WARNING. Please make sure you do not violate any licence agreements
             when building and redistributing win32 binaries.
    
"""

from distutils.core import setup
import py2exe

setup(console=['main.py'])

