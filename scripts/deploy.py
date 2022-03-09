from pathlib import Path
from readline import append_history_file

import click
from ape import accounts, project, logger
from ape.cli import NetworkBoundCommand, network_option, account_option


@click.group(short_help="Deploy the project")
def cli():
    pass


@cli.command(cls=NetworkBoundCommand)
@network_option()
@account_option()
@click.argument("artist")  # `AddressType`
def nft(network, account, artist):
    """Deploy the apepiece NFT contract"""
    piece = account.deploy(project.ApePiece,artist,"")
    click.echo(f"NFT deployed to {piece.address}")


@cli.command(cls=NetworkBoundCommand)
@network_option()
@account_option()
@click.argument("nft")
def auction(network,account,nft):
    """`BuyApe.vy` deploy process to `network` here"""
    nft = project.ApePiece.at(nft) #todo: get from dependencies
    if nft.owner() != account:
        logger.error("account is not owner of NFT")
    auction = account.deploy(project.BuyApe,nft)
    nft.setMinter(auction,sender=account)
    click.echo(f"Auction deployed to {auction.address}")

@cli.command(cls=NetworkBoundCommand)
@network_option()
@account_option()
@click.argument("nft")
def merkle(network,account):
    """deploy merkle drop"""
    nft = project.ApePiece.at(nft) #todo: get from dependencies
    if nft.owner() != account:
        logger.error("account is not owner of NFT")
    merkle = account.deploy(project.MerkleDrop,nft,root_hash)
    nft.setMinter(merkle,sender=account)
    click.echo(f"MerkleDrop deployed to {merkle.address}")