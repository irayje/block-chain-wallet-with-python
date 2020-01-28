#!/usr/bin/env python
# coding: utf-8

# In[2]:


import subprocess
import json
import os
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from eth_account import Account
from bit import *

from pathlib import Path
from getpass import getpass


# In[3]:


load_dotenv()
from constants import *
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
mnemonic = os.getenv('MNEMONIC')


# In[6]:


def derive_wallets(mnenomicvariable, coinname, num):
    x = './wallet/derive -g --mnemonic="' + mnenomicvariable + '" --format=json --coin=' + coinname + ' --numderive='+ str(num) + ' --cols=path,index,address,privkey,pubkey'
    p = subprocess.Popen(x, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    accounts = json.loads(output)
    return accounts


# In[7]:


derive_wallets(mnemonic, 'btc-test', 4)[3]['privkey']


# In[7]:


coins = {'btc': derive_wallets(mnemonic, 'btc', 4),
        'btc-test': derive_wallets(mnemonic, 'btc-test', 4),
        'eth': derive_wallets(mnemonic, 'eth', 4)}


# In[8]:


print(json.dumps(coins, indent=2))


# In[9]:


coins['btc'][0]['privkey']


# In[10]:


def priv_key_to_account(coin, priv_key):
    if coin == 'eth':
        return Account.privateKeyToAccount(priv_key)
    elif coin == 'btc-test': # or 'btc':
        return PrivateKeyTestnet(priv_key)
#    For ETH, return Account.privateKeyToAccount(priv_key)
#    For BTCTEST, return PrivateKeyTestnet(priv_key)


# In[11]:


priv_key_to_account('eth', coins['eth'][0]['privkey'] )


# In[12]:


priv_key_to_account('btc-test', coins['btc-test'][0]['privkey'])


# In[13]:


def create_tx(coin, account, recipient, amount):
    if coin == 'eth':
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    elif coin == 'btc-test': #or 'btc':
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, 'btc')])


# In[14]:


def send_tx(coin, account, recipient, amount):
    tx = create_tx(coin, account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    if coin == 'eth':
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    elif coin == 'btc-test': # or 'btc':
        return NetworkAPI.broadcast_tx_testnet(signed_tx)


# In[16]:


create_tx('eth', priv_key_to_account('eth', coins['eth'][0]['privkey']), '0x22C5b0FDeC24947524dd951ACF42564249A3409b', 0)


# In[17]:


send_tx('eth', priv_key_to_account('eth', coins['eth'][0]['privkey']), '0x22C5b0FDeC24947524dd951ACF42564249A3409b', 0)


# In[ ]:





# In[ ]:





# In[ ]:




