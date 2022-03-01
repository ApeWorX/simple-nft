
import click
from ape import convert
from ape.types import AddressType
from trie import smt
from pathlib import Path
from eth_utils import to_bytes, to_hex
import json

ADDRESS_DBFILE = Path.cwd()/"scripts/db.json"
TRUE_NODE = b"\x00" * 31 + b"\x01"
FALSE_NODE = b"\x00" * 32
KEY_SIZE = 20

def get_tree() -> smt.SparseMerkleTree:
    if ADDRESS_DBFILE.exists():
        click.echo("Tree DB loading...")
        db = json.loads(ADDRESS_DBFILE.read_text())
        return smt.SparseMerkleTree.from_db(
            db={to_bytes(hexstr=k):to_bytes(hexstr=v) for k,v in db["db"].items()},
            root_hash=to_bytes(hexstr=db["root_hash"]),
            key_size=KEY_SIZE,
            default=FALSE_NODE
        )
    else:
        return smt.SparseMerkleTree(key_size=KEY_SIZE, default=FALSE_NODE)

def save_tree(tree):
    click.echo("Saving Tree DB...")
    db = {'db':{to_hex(k):to_hex(v) for k,v in tree.db.items()},'root_hash':to_hex(tree.root_hash)}
    ADDRESS_DBFILE.write_text(json.dumps(db))

@click.group(short_help="Working with merkledb")
def cli():
    """
    CLI for working with merkle database. Assumes merkledb file will be created in scripts/db.json
    """
    pass

@cli.command()
def purge():
    """purge merkle db"""
    ADDRESS_DBFILE.unlink()

@cli.command()
@click.argument("addresses",nargs=-1)
def add(addresses):
    """add one or more addresses to the merkle db"""
    tree = get_tree()
    for address in addresses:
        tree.set(to_bytes(hexstr=address), TRUE_NODE)
    save_tree(tree)

@cli.command()
@click.argument("addresses",nargs=-1)
def remove(addresses):
    """remove one or more addresses from the merkle db"""
    tree = get_tree()
    for address in addresses:
        tree.set(to_bytes(hexstr=address), FALSE_NODE)
    save_tree(tree)

#import is a protected keyword - using a different function name
@cli.command(name="import")
@click.argument("filename", type=click.Path(exists=True))
def import_from_file(filename):
    """import a list of addresses from a file"""
    tree = get_tree()
    addresses = Path(filename).read_text().split("\n")
    for address in addresses:
        tree.set(to_bytes(hexstr=address), TRUE_NODE)
    save_tree(tree)

@cli.command()
@click.argument("address")
def check(address):
    """check if address is in the merkle db"""
    tree = get_tree()
    if tree.get(to_bytes(hexstr=convert(address,AddressType))) == TRUE_NODE:
        click.echo(f"Address {address} exists in tree")
    else:
        click.echo(f"Address {address} DOES NOT exist in tree")

@cli.command()
@click.argument("address")
def get_proof(address):
    """Get merkle proof for an address from the merkle db tree"""
    tree = get_tree()
    if tree.get(to_bytes(hexstr=convert(address,AddressType))) == FALSE_NODE:
        click.echo(f"Address {address} DOES NOT exist in tree")
        return
    branch = tree.branch(to_bytes(hexstr=convert(address,AddressType)))
    click.echo("\n".join(map(to_hex,branch)))
    
