import click
from ape.cli import network_option


@click.group(short_help="Deploy the project")
def cli():
    pass


@cli.command()
def assets():
    ... # Upload all assets and generated JSON files from `scripts/data` here


@cli.command()
@network_option()
@click.argument("artist", ...)  # `AddressType`
def nft(network, artist):
    ... # `ApePiece.vy` deploy process to `network` here


@cli.command()
@network_option()
def auction(network):
    ... # `BuyApe.vy` deploy process to `network` here