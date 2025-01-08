wstETH = '0x13e5FB0B6534BB22cBC59Fae339dbBE0Dc906871'
bondETH = '0x1aC493C87a483518642f320Ba5b342c7b78154ED'
levETH = '0x975f67319f9DA83B403309108d4a8f84031538A6'


tokenAbi = [
    {
        "constant": True,
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
