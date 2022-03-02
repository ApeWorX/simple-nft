interface ApePiece:
    def mint(to: address) -> bool: nonpayable


ape_piece: public(address)
root_hash: public(bytes32)
claimed: public(HashMap[address,bool])

@external
def __init__(ape_piece: address, root_hash: bytes32):
    self.ape_piece = ape_piece
    self.root_hash = root_hash

@internal
@view
def _calc_root(
    leaf: bytes32,
    proof: bytes32[160]
) -> bytes32:
    node: bytes32 = leaf
    for sibling in proof:
        if convert(node, uint256) <= convert(sibling, uint256):
            node = keccak256(concat(node, sibling))
        else:
            node = keccak256(concat(sibling, node))
    return node

@external
def claim(proof: bytes32[160]):
    assert not self.claimed[msg.sender]
    self.claimed[msg.sender] = True
    assert self._calc_root(convert(msg.sender,bytes32),proof) == self.root_hash
    ApePiece(self.ape_piece).mint(msg.sender)