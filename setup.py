from setuptools import setup, find_packages

setup(
    name='tkpf',
    description=' A GUI library for python/tkinter with two-way data binding',
    author='Márton Marczell',
    url="https://github.com/marczellm/tkpf",
    version='0.0.1',
    packages=find_packages(),
    long_description="""\
tkpf is a library for building Tkinter GUIs in a paradigm influenced by WPF (Windows Presentation Foundation) and Angular.

Main features are:

 * Declarative view hierarchy and layout in XML
 * One-way and two-way data binding
 * Componentization support
    """,
    keywords="tkinter",
    license="LGPLv3",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
