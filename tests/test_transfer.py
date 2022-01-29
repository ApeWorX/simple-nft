import ape


def test_mint(nft, owner):
    assert nft.balanceOf(owner) == 0
    nft.mint(owner, sender=owner)
    assert nft.balanceOf(owner) == 1
    assert nft.ownerOf(0) == owner


def test_transfer(nft, owner, buyers):
    friend = buyers[0]
    nft.mint(owner, sender=owner)
    assert nft.balanceOf(owner) == 1
    assert nft.ownerOf(0) == owner

    nft.transferFrom(owner, friend, 0, sender=owner)
    assert nft.balanceOf(owner) == 0
    assert nft.balanceOf(friend) == 1
    assert nft.ownerOf(0) == friend


def test_buyers_cant_mint(nft, buyers):
    friend = buyers[0]
    with ape.reverts():
        nft.mint(friend, sender=friend)
