from web3 import *
import time,os,sys

from abi import *

from dotenv import load_dotenv

load_dotenv()

connect = Web3(Web3.HTTPProvider('https://base-sepolia.infura.io/v3/723972c109514a08b4afb742fd1447c9'))


def verifyHash(hash,topic,transaction):
        invalidhash = 0
        while True:
            try:
                receipt = connect.eth.get_transaction_receipt(hash)
                logs = receipt.get('logs',[])
                topics = ['0x'+log['topics'][0].hex() for log in logs]
                if topic in topics :
                    print(f'{transaction} Is Successfull')
                    break 
                else:
                    print(f'{transaction} Failed')
                    break 
            except Exception as e:
                if invalidhash == 20:
                    break
                print(f'{transaction} Not Yet Mined')
                time.sleep(3)

def checkAllowance(tokenContract,account,plaza_contract):
    allowance =  tokenContract.functions.allowance(account.address,plaza_contract).call()
    return allowance

def approval(tokenContract,account,plaza_contract,priv):
    approveTopic = '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'
    unlimited = 2**256 - 1
    approve = tokenContract.functions.approve(
        plaza_contract,
        unlimited
    ).build_transaction({
        'from':account.address,
        'gas':70000,
        'maxPriorityFeePerGas':connect.to_wei('0.0008','gwei'),
        'maxFeePerGas': connect.to_wei('0.2','gwei'),
        'nonce':connect.eth.get_transaction_count(account.address),
        'chainId':84532
    })
    signTrx = connect.eth.account.sign_transaction(approve,priv)
    send = connect.eth.send_raw_transaction(signTrx.raw_transaction)
    verifyHash(send.hex(),approveTopic,'ApproveTransaction')



def swap(account,plaza_contract,task,priv):
    swapTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
    transaction = {
    'from':account.address,
    'to':plaza_contract,
    # 'value': connect.to_wei('0.1','ether'),
    'gas':170000,
    'data':task,
    'maxPriorityFeePerGas':connect.to_wei('0.0008','gwei'),
    'maxFeePerGas': connect.to_wei('2','gwei'),
    'nonce':connect.eth.get_transaction_count(account.address),
    'chainId':84532
    }
    signTrx = connect.eth.account.sign_transaction(transaction,priv)
    send = connect.eth.send_raw_transaction(signTrx.raw_transaction)
    verifyHash(send.hex(),swapTopic,'swapTransactions')

def dailyTask(account,plaza_contract,priv):
    tasks = [
        '0x6e530e97000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000038d7ea4c680000000000000000000000000000000000000000000000000000076ddd2c76a7f7c',
        '0x6e530e97000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000038d7ea4c68000000000000000000000000000000000000000000000000000000d8e65fd8da138',
        '0xf0fae20f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000016345785d8a0000000000000000000000000000000000000000000000000000000a8334f31f5a36',
        '0xf0fae20f000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000038d7ea4c680000000000000000000000000000000000000000000000000000000e8326d403456'
        ]

    for task in tasks:
        swap(account,plaza_contract,task,priv)
        time.sleep(4)



def start(account,priv):
    tokens = [wstETH,bondETH,levETH]
    plaza_contract = '0x47129e886b44B5b8815e6471FCD7b31515d83242'
    for token in tokens:
        tokenContract = connect.eth.contract(address=token,abi=tokenAbi)
        allowance = checkAllowance(tokenContract,account,plaza_contract)
        if allowance <= 0:
            approval(tokenContract,account,plaza_contract,priv)

    dailyTask(account,plaza_contract,priv)
    print('Daily Swap Completed')    



raw_key = os.getenv("MY_KEYS", "")
key_list = raw_key.strip("[]").replace(" ", "").split(",")
while True:
    for key in key_list:
        account = Account.from_key(key)
        start(account,key)
        time.sleep(5)
    print('Swaping Next In The Next 24hrs')
    time.sleep(24*60*60)