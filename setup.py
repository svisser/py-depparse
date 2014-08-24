import os
import setuptools

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')) as readme:
    long_description = readme.read()

setuptools.setup(
    name='depparse',
    version='0.1.0',
    packages=setuptools.find_packages(),
    author='Leif Johnson',
    author_email='leif@leifjohnson.net',
    description='dependency parsers for natural language text',
    long_description=long_description,
    license='MIT',
    url='http://github.com/lmjohns3/py-depparse/',
    keywords=('parsing '
              'dependency-parsing '
              'nlp '
              'nlproc '
              ),
    scripts=['scripts/py-depparse'],
    install_requires=['climate'],
    ext_modules=[setuptools.Extension('depparse._sparse', sources=['src/sparse.c'])],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        ],
    )
