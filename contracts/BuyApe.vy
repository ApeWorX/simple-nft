interface ApePiece:
    def artist() -> address: view
    def mint(to: address) -> bool: nonpayable


ape_piece: public(address)

PRICE: constant(uint256) = 25 * 10 ** 15  # minting price of 0.025 ETH (can pay more tho)


@external
def __init__(ape_piece: address):
    self.ape_piece = ape_piece


@payable
@external
def buy():
    # Buy an NFT from this contract. TokenId is whatever comes next.
    assert block.basefee < 150 * 10 ** 9  # 150 gwei, just some silly ape protection
    assert msg.value >= PRICE

    ape_piece: address = self.ape_piece
    artist: address = ApePiece(ape_piece).artist()
    send(artist, msg.value)  # Artist gets 100% of the proceeds of minting

    assert ApePiece(ape_piece).mint(msg.sender)
