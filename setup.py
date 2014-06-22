from setuptools import setup

setup(
    name='zeek',
    author='Kristian Perkins',
    author_email='krockode@gmail.com',
    version='0.1',
    url='http://github.com/krockode/zeek',
    py_modules=['zeek'],
    description='ZooKeeper CLI',
    install_requires=[
        'Click',
        'Kazoo',
    ],
    entry_points='''
       [console_scripts]
       zeek=zeek:main
    ''',
    classifiers=(
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
    ),
)
