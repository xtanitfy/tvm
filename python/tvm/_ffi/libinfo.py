"""Library information."""
from __future__ import absolute_import
import sys
import os
import platform


def find_lib_path(name=None):
    """Find dynamic library files.

    Parameters
    ----------
    name : list of str
        List of names to be found.

    Returns
    -------
    lib_path : list(string)
        List of all found path to the libraries
    """
    use_runtime = os.environ.get("TVM_USE_RUNTIME_LIB", False)
    curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    root_path = os.path.join(curr_path, '../')
    api_path = os.path.join(curr_path, '../../../lib/')
    cmake_build_path = os.path.join(curr_path, '../../../build/Release/')
    dll_path = [curr_path, root_path, api_path, cmake_build_path]
    if os.name == 'nt':
        vs_configuration = 'Release'
        if platform.architecture()[0] == '64bit':
            dll_path.append(os.path.join(curr_path, '../../../build', vs_configuration))
            dll_path.append(os.path.join(curr_path, '../../../windows/x64', vs_configuration))
        else:
            dll_path.append(os.path.join(curr_path, '../../../build', vs_configuration))
            dll_path.append(os.path.join(curr_path, '../../../windows', vs_configuration))
    elif os.name == "posix" and os.environ.get('LD_LIBRARY_PATH', None):
        dll_path.extend([p.strip() for p in os.environ['LD_LIBRARY_PATH'].split(":")])
    dll_path = [os.path.abspath(x) for x in dll_path]
    if name is not None:
        lib_dll_path = [os.path.join(p, name) for p in dll_path]
        runtime_dll_path = []
    else:
        if os.name == 'nt':
            lib_dll_path = [os.path.join(p, 'libtvm.dll') for p in dll_path]
            runtime_dll_path = [os.path.join(p, 'libtvm_runtime.dll') for p in dll_path]
        else:
            lib_dll_path = [os.path.join(p, 'libtvm.so') for p in dll_path]
            runtime_dll_path = [os.path.join(p, 'libtvm_runtime.so') for p in dll_path]

    if not use_runtime:
        # try to find lib_dll_path
        lib_found = [p for p in lib_dll_path if os.path.exists(p) and os.path.isfile(p)]
    if use_runtime or not lib_found:
        # try to find runtime_dll_path
        use_runtime = True
        lib_found = [p for p in runtime_dll_path if os.path.exists(p) and os.path.isfile(p)]

    if not lib_found:
        raise RuntimeError('Cannot find the files.\n' +
                           'List of candidates:\n' +
                           str('\n'.join(lib_dll_path + runtime_dll_path)))

    if use_runtime:
        sys.stderr.write("Loading runtime library %s... exec only\n" % lib_found[0])
        sys.stderr.flush()
    return lib_found


# current version
__version__ = "0.1.0"
