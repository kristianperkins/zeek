from os import path

import click
from kazoo.client import KazooClient

zk = None


def init(hosts):
    global zk
    zk = KazooClient(hosts=hosts)
    zk.start()


def main():
    global zk
    cli(auto_envvar_prefix='ZEEK')
    if zk is not None and zk.connected:
        zk.close()


@click.group()
@click.option('--hosts',
              default='localhost:2181',
              help="ZooKeeper connection string",
              show_default=True)
def cli(hosts):
    """View your ZooKeeper configuration from the command line"""
    init(hosts)


@cli.command()
@click.argument('path')
def ls(path):
    """ List the contents of a specified path.

    Arguments:
        PATH    the path to list the contents of."""
    echo(path)
    for p in children(path):
        echo(p)


@cli.command()
@click.argument('path')
def find(path):
    """ Find all children of a specified path.

    Arguments:
        PATH    the path to search for children."""
    echo(path)
    for p in walk(path):
        echo(p)


def children(path):
    """Generator that yields the children of the specified path"""
    for c in zk.get_children(path):
        if path == '/':
            yield '/%s' % c
        else:
            yield '%s/%s' % (path, c)


def walk(path):
    """Generator that yields the children of the given path recursively"""
    for c in children(path):
        yield c
        for x in walk(c):
            yield x


def echo(path):
    """Echos a ZooKeeper node path and value"""
    click.echo('%s - %s' % (path, zk.get(path)[0]))
