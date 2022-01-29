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
