import ape


def test_buy(nft, auction, artist, buyers):
    a = buyers[0]
    assert nft.totalSupply() == 0

    before = artist.balance
    auction.buy(sender=a, value="0.025 ether")
    assert nft.totalSupply() == 1
    assert nft.ownerOf(0) == a
    assert artist.balance == before + ape.convert("0.025 ether", int)
