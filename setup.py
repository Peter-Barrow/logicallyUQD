import os
from numpy import get_include
from Cython.Build import cythonize
from ctypes.util import find_library
from setuptools import setup, Extension


def check_library_installed(library_name):
    # Remove 'lib' prefix and '.so' suffix if present
    clean_name = library_name
    if library_name.startswith('lib'):
        clean_name = library_name[3:]
    if clean_name.endswith('.so'):
        clean_name = clean_name[:-3]

    return find_library(clean_name) is not None


cython_dir = os.path.join('./src/logicallyUQD/')

extensions = []

libusb = 'usb'
if check_library_installed('lib' + libusb) is False:
    if check_library_installed('lib' + libusb + '-1.0') is True:
        libusb += '-1.0'
    else:
        raise ValueError('Could not find libusb')

logically_UQD = Extension(
    'logicallyUQD._lib',
    sources=[
        os.path.join(cython_dir, '_lib.py'),
        os.path.join(cython_dir, 'bindings_uqd_logic.cpp'),
    ],
    include_dirs=[
        get_include(),
        cython_dir,
        './opt/CTimeTag/Include',
    ],
    define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
    libraries=[libusb, 'timetag64'],
    library_dirs=['.', './opt/CTimeTag/Linux'],
    extra_compile_args=[],
    optional=os.environ.get('CIBUILDWHEEL', '0') != '1',
)

extensions.append(logically_UQD)

ext_modules = cythonize(
    extensions,
    include_path=[cython_dir],
    compiler_directives={'language_level': '3'},
    annotate=True,
)

setup(ext_modules=ext_modules)
