import os
from subprocess import call
import tempfile
import click
from kazoo.client import KazooClient

zk = None


def init(hosts):
    global zk
    zk = KazooClient(hosts=hosts)
    zk.start(timeout=5)


def main():
    global zk
    cli(auto_envvar_prefix='ZEEK')
    if zk is not None and zk.connected:
        zk.close()


@click.group()
@click.option('--hosts',
              '-H',
              default='localhost:2181',
              help="ZooKeeper connection string",
              show_default=True)
def cli(hosts):
    """View your ZooKeeper data from the command line"""
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


@cli.command()
@click.argument('path')
@click.option('--recursive',
              '-r',
              is_flag=True,
              help="create parent nodes if they don't exist")
def touch(path, recursive):
    """ Create the specified node.

    Arguments:
        PATH    the node to edit."""
    create_node(path, recursive)


@cli.command()
@click.argument('path')
@click.argument('value')
@click.option('--create',
              '-c',
              is_flag=True,
              help="create parent nodes if they don't exist")
def set(path, value, create):
    """ Set a specified node

    Arguments:
        PATH    the node to edit.
        VALUE   the value of the node"""
    create_node(path, create)
    node = zk.set(path, value.encode('utf-16be'))
    click.echo(node[0])


@cli.command()
@click.argument('path')
def vi(path):
    """ Edit a specified node

    Arguments:
        PATH    the node to edit."""
    editor = os.environ.get('EDITOR', 'vim')
    create_node(path)
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tmp:
        if zk.exists(path):
            node = zk.get(path)
            tmp.write(node[0])
        tmp.flush()
        call([editor, tmp.name])
        zk.set(path, open(tmp.name).read().strip())


@cli.command()
@click.argument('path')
def rm(path):
    """ Edit a specified node

    Arguments:
        PATH    the node to edit."""
    if zk.exists(path):
        zk.delete(path)
    else:
        click.echo('%s does not exist' % path)


def children(path):
    """Generator that yields the children of the specified path"""
    global zk
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


def parents(path, ascending=False):
    """Generator that yields the full path of all parents"""
    if path == '/':
        yield path
        return
    parts = path.split('/')
    indexes = range(len(parts) - 1)
    if not ascending:
        indexes.reverse()
    for i in indexes:
        yield '/' + '/'.join(parts[1:i+1])


def echo(path):
    """Echos a ZooKeeper node path and value"""
    click.echo('%s - %s' % (path, zk.get(path)[0]))


def create_node(path, recursive=False):
    if recursive:
        for parent in parents(path, ascending=True):
            if not zk.exists(parent):
                zk.create(parent)
    if zk.exists(path):
        click.echo('%s already exists' % path)
    else:
        zk.create(path)
