import pytest


@pytest.fixture
def BASE_URI():
    return "https://test.com"


@pytest.fixture
def owner(accounts):
    return accounts[0]


@pytest.fixture
def artist(accounts):
    return accounts[1]


@pytest.fixture
def buyers(accounts):
    return accounts[2:]


@pytest.fixture
def nft(project, owner, artist, BASE_URI):
    return owner.deploy(project.ApePiece, artist, BASE_URI)


@pytest.fixture
def auction(project, nft, owner):
    # NOTE: Transfer control of nft minting to the auction contract
    auction = owner.deploy(project.BuyApe, nft)
    nft.setMinter(auction, sender=owner)
    return auction
