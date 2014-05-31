from setuptools import setup

setup(
    name='Zeek',
    version='0.1',
    py_modules=['zeek'],
    install_requires=[
        'Click',
        'Kazoo',
    ],
    entry_points='''
       [console_scripts]
       zeek=zeek:main
    '''
)
