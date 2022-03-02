from pathlib import Path
from readline import append_history_file

import click
from ape import accounts, project
from ape.cli import NetworkBoundCommand, network_option
from eth_utils import to_bytes
from trie import smt


@click.group(short_help="Deploy the project")
def cli():
    pass


@cli.command()
def assets():
    pass  # Upload all assets and generated JSON files from `scripts/data` here


@cli.command(cls=NetworkBoundCommand)
@network_option()
@click.argument("artist")  # `AddressType`
def nft(network, artist):
    a = accounts.load(artist)
    piece = artist.deploy(project.ApePiece)


@cli.command(cls=NetworkBoundCommand)
@network_option()
def auction(network):
    pass  # `BuyApe.vy` deploy process to `network` here
