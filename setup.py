from setuptools import setup

setup(
    name = "qdatastream",
    version = "0.1",
    py_modules = ["qdatastream"],
    zip_safe = True,

    # metadata for upload to PyPI
    author = "Qize Huang",
    author_email = "hgoldfish@gmail.com",
    description = "pure python implementation for Qt's QDataStream",
    license = "LGPL",
    keywords = "qt qdatastream",
    url = "http://github/hgoldfish/qdatastream",

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
