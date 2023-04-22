# Call Algoexplorer API to export all account Tx to an excel sheet. Account pub addr passed to 1st arg.
# And filter these fields only => date UTC, txid, sender, amount, receiver. 
# Written during MyAlgo hack context for tracking the hacker's accounts.
# algo explorer api :   https://algoexplorer.io/api-dev/indexer-v2
# algo explorer :       https://algoexplorer.io/
# Author : 4OTXZM7NFVZHZUXDI2CSOUMTAUDZPI4Y5BBAMZ44DTXYIG4SMHJZUTASKI

import os, sys
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json
from datetime import datetime
import pandas as pd


algoindexer_api_url = "https://algoindexer.algoexplorerapi.io/v2"
outfile_path = os.path.dirname(__file__)

# FUNC getAllTxFromAddr : get all tx from addr and return a json dict list of tx
def getAllTxFromAddr(addr):
    print(f' -- Get all tx for account {addr}...')
    page_to_fetch = ''
    tx_json = { 'next-token' : ''}
    all_tx_json = { 'transactions' : []}
    # loop for managing multiple page responses (if dict key next-token exists)
    while "next-token" in tx_json:
        try:
            response = urlopen(algoindexer_api_url + '/accounts/' + addr + '/transactions' + page_to_fetch )
        except HTTPError as e:
            print(' -- HTTP Error: ', e)
            sys.exit(2)
        except URLError as e:
            print(' -- URL Error: ', e)
            sys.exit(3)
        else:
            tx_json = json.loads(response.read())
            all_tx_json['transactions'].append(tx_json['transactions'])
            if "next-token" in tx_json:
                page_to_fetch = '?next=' + tx_json['next-token']
    return all_tx_json


# FUNC filterAndSortAllTx : filter and sort specific keys of the tx dict list and construct a new dict list
def filterAndSortAllTx(all_tx_dict_list):
    print(' -- Filter and sort all tx...')
    all_tx_dict_list_filtered = []
    for i in range(len(all_tx_dict_list['transactions'])):
    # iterate Tx dict list and go further if not empty only
        if all_tx_dict_list['transactions'][i]:
            for tx in all_tx_dict_list['transactions'][i]:
                # get keys->values for id, round-time and sender
                tx_dict_filtered = {key: tx[key] for key in tx.keys() & {'id', 'round-time', 'sender'}}
                if 'payment-transaction' in tx:
                    # if payment key exists get key->values for payment-transaction and extract the value as a dict by filtering this 3 keys->values amount, close-amount and receiver, or add '0' value
                    pay_tx_dict = {key: tx[key] for key in tx.keys() & {'payment-transaction'}}
                    pay_tx_dict_filtered = {key: pay_tx_dict['payment-transaction'][key] for key in pay_tx_dict['payment-transaction'].keys() & {'amount', 'close-amount', 'receiver'}}
                    tx_dict_filtered.update(pay_tx_dict_filtered)
                elif 'asset-transfer-transaction' in tx:
                    # if asset-transfer-transaction key exists get key->values for asset-transfer-transaction and extract the value as a dict by filtering this 3 keys->values amount, close-amount and receiver, or add '0' value
                    pay_tx_dict = {key: tx[key] for key in tx.keys() & {'asset-transfer-transaction'}}
                    pay_tx_dict_filtered = {key: pay_tx_dict['asset-transfer-transaction'][key] for key in pay_tx_dict['asset-transfer-transaction'].keys() & {'amount', 'close-amount', 'receiver'}}
                    tx_dict_filtered.update(pay_tx_dict_filtered)
                else:
                    tx_dict_filtered.update({"amount" : 0 , "close-amount" : 0, "receiver" : 0})
                # append to the new filtered tx dict list
                all_tx_dict_list_filtered.append(dict(sorted(tx_dict_filtered.items())))
    return all_tx_dict_list_filtered


# FUNC createTxJsonFile : write tx json data on disk 
def createTxJsonFile(json_data, addr, out_path):
    print(' -- JSON file creation...')
    file_prefix = os.path.join(out_path,'all_tx_')
    with open(file_prefix + str(addr[:4]) + '-' + str(addr[-4:]) + '.json', 'w') as outfile:
        json.dump(json_data, outfile)


# FUNC createTxExcelFile : pandas format, sort, convert and write excel
def createTxExcelFile(json_data, addr, out_path):
    # panda format, sort, convert,...
    print(' -- Panda formating...')
    df = pd.DataFrame.from_dict(json_data)
    # merge ammunt and close-amount
    df['amount'] = df.pop('amount') + df.pop('close-amount')
    df['amount'] = df['amount'].div(1000000).round(0)
    df = df.reindex(columns=['round-time', 'id', 'sender', 'amount', 'receiver'])
    df = df.rename(columns={'round-time': 'date UTC', 'id': 'txid'})
    df.sort_values(by=['date UTC'])
    df['date UTC'] = [datetime.utcfromtimestamp(x) for x in df['date UTC']]
    # write file
    print(' -- Excel file creation...')
    file_prefix = os.path.join(out_path,'all_tx_')
    df.to_excel(file_prefix + str(addr[:4]) + '-' + str(addr[-4:]) + '.xlsx', index = False)


# FUNC usage
def usage():
    print(f"""
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % Pass Algo account pub address to 1st argument, excel sheet will be created in current directory %
 % (requires pandas)
 %
 %    python3 {os.path.basename(__file__)} VX6JI2PB67H...
 %
 %       excel sheet -> all_tx_XXXX-YYYY.xlsx
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """)


# MAIN
if __name__ == '__main__':
    print('\n')
    # check argv
    if len(sys.argv) == 2 and sys.argv[1].isalnum and sys.argv[1].isupper and len(sys.argv[1]) == 58:
        # 1st arg to Algo account addr
        algo_account = str(sys.argv[1])
        tx_json = getAllTxFromAddr(algo_account)
        tx_json_filtered = filterAndSortAllTx(tx_json)
        createTxExcelFile(tx_json_filtered, algo_account, outfile_path)
        # Optional: also create a json file
        #createTxJsonFile(tx_json_filtered, algo_account, outfile_path)
        sys.exit(0)
    else:
        usage()
        sys.exit(1)



    
