from readline import append_history_file
import click
from ape.cli import network_option, NetworkBoundCommand
from ape import project
from ape import accounts
from trie import smt
from pathlib import Path

@click.group(short_help="Deploy the project")
def cli():
    pass


@cli.command()
def assets():
    ... # Upload all assets and generated JSON files from `scripts/data` here


@cli.command(cls=NetworkBoundCommand)
@network_option()
@click.argument("artist", ...)  # `AddressType`
def nft(network, artist):
    a = accounts.load(artist)
    piece = artist.deploy(project.ApePiece)


@cli.command(cls=NetworkBoundCommand)
@network_option()
def auction(network):
    ... # `BuyApe.vy` deploy process to `network` here


@cli.command()
def merkle_root(filename):
    TRUE_NODE = b"\x00" * 31 + b"\x01"
    FALSE_NODE = b"\x00" * 32
    addresses = Path(filename).read_text().split("\n")
    tree = smt.SparseMerkleTree(20, FALSE_NODE)
    for address in addresses:
        tree.set(to_bytes(hexstr=address), TRUE_NODE)
    return tree
    # calculate merkle root with input file here