Zeek: Zookeeper CLI for caged animals!
======================================

.. image:: https://badge.fury.io/py/zeek.png
    :target: http://badge.fury.io/py/zeek

.. image:: https://pypip.in/d/zeek/badge.png
    :target: https://crate.io/packages/zeek/

.. image:: https://badge.waffle.io/krockode/zeek.png?label=ready&title=Ready 
    :target: https://waffle.io/krockode/zeek
    :alt: 'Stories in Ready'

The Z and K are for `Zookeeper <http://zookeeper.apache.org>`_, the E's are
just for fun.

Break free from the menagerie of configuration.  Zeek is a ZooKeeper command
line application that makes it easy to see what is in all those cages.  This
CLI works best in ZSH.

Turn On - (Installation)
------------------------

To install zeek:

    $ pip install zeek


Tune In - (Configuration)
-------------------------

Zeek connects to localhost:2181 by default.  To change this you can either set
the environment variable ZEEK_HOSTS or add the option `-H`/`--hosts` to the
zeek command.  The value should be a comma separated list of zookeeper servers
to connect to e.g. host1:2181,host2:2181


Drop Out - (Usage)
------------------

The goal of zeek is to provide reasonable facimilies of the unix `find` and
`grep` commands for the Zookeeper structure, so no new learning is required.
Both find and grep return matches in the form of `<node> - <value>` where
`node` is the full path of the node and `value` is the stringified value of
that node.

``ls``
    List nodes underneath the node you specified.

Example::

    $ zeek ls /animals
    /animals/ -
    /animals/mammals -
    /animals/reptiles -
    

``find``
    Example of find which will perform a recursive find from the root.

::

    $ zeek find /
    / -
    /animals -
    /animals/mammals -
    /animals/mammals/foxes - ok
    /animals/reptiles -
    /animals/reptiles/snakes - rad
    /animals/reptiles/crocodilia -
    /animals/reptiles/crocodilia/alligators - hungry
    /animals/reptiles/crocodilia/crocodiles - hungry

Zeek find is like `find / -name ...` and searches for zookeeper nodes that
match your search::

    $ zeek find '*crocodile*'
    /animals/reptiles/crocodilia/crocodiles - hungry


``grep``
    Zeek Grep searches zookeeper node values.

::

    $ zeek grep hungry
    /animals/reptiles/crocodilia/alligators - hungry
    /animals/reptiles/crocodilia/crocodiles - hungry

