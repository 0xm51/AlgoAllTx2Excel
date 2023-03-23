# AlgoAllTx2Excel  
Author : 4OTXZM7NFVZHZUXDI2CSOUMTAUDZPI4Y5BBAMZ44DTXYIG4SMHJZUTASKI  
Algo explorer api :   https://algoexplorer.io/api-dev/indexer-v2  
Algo explorer :       https://algoexplorer.io/  

## Purpose  
Call Algoexplorer API to export all account Tx to an excel sheet. Account pub addr passed to 1st arg   
And filter these fields only => date UTC, txid, sender, amount, receiver   
Written during MyAlgo hack context for tracking the hacker's accounts  

Examples here attached for 3 suspicious accounts:

 - Main addr which seems to be a final destination for many hacked accounts => `6PO62A5VTCIQJWFGEV7RNAGXE5AVCIFI5VYOO4MX6OFEQHB6P2XCXW3SBY`  
 - Addr used as a "transit" addr => `4UE7AHNYEYD5Z2VJUYTU5JIXHLFJIVBXF3RXZRJSMN4ASAJEJOOBYOK4AE`  
 - Last addr before transfering to binance 5 => `VX6JI2PB67HIRCVAERVCEKYD2Q3UGUGWTPWXWEYIDZMEAB4Q4VNHRHVKYY`  

## Requirements
Tested with:
 - python 3.10.10
 - pandas 1.5.3

## Usage
Pass Algo account pub address to 1st argument, excel sheet will be created in current directory
```
python3 algoalltx2excel.py VX6JI2PB67HIRCVAERVCEKYD2Q3UGUGWTPWXWEYIDZMEAB4Q4VNHRHVKYY
```


![algo_to_binance5](https://user-images.githubusercontent.com/127057042/227370452-b7d72f16-4149-4d3b-a9b1-80d763665dbf.png)
