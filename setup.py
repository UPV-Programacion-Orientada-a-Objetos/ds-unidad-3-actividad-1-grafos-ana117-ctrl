from setuptools import setup, Extension
from Cython.Build import cythonize
import sys

# Configuración de flags según el sistema operativo
extra_compile_args = []
extra_link_args = []

if sys.platform == 'win32':
    extra_compile_args = ['/std:c++17', '/O2']
else:
    extra_compile_args = ['-std=c++17', '-O3']

extensions = [
    Extension(
        "grafo_wrapper",
        sources=["grafo_wrapper.pyx", "GrafoDisperso.cpp"],  # Incluir el .cpp
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        include_dirs=["."],  # Incluir directorio actual para los headers
    )
]

setup(
    name="NeuroNet",
    version="1.0",
    description="Sistema híbrido C++/Python para análisis de grafos masivos",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    zip_safe=False,
)