# AlgoAllTx2Excel  
Author : 4OTXZM7NFVZHZUXDI2CSOUMTAUDZPI4Y5BBAMZ44DTXYIG4SMHJZUTASKI  
Algo explorer api :   https://algoexplorer.io/api-dev/indexer-v2  
Algo explorer :       https://algoexplorer.io/  

## Purpose  
Call Algoexplorer API to export all account Tx to an excel sheet. Account pub addr passed to 1st arg   
And filter these fields only => date UTC, txid, sender, amount, receiver   
Written during MyAlgo hack context for tracking the hacker's accounts  

Examples here attached for suspicious accounts:

 - Main addr which seems to be a final destination for many hacked accounts `6PO62A5VTCIQJWFGEV7RNAGXE5AVCIFI5VYOO4MX6OFEQHB6P2XCXW3SBY`
 - Addr used as a "transit" addr `4UE7AHNYEYD5Z2VJUYTU5JIXHLFJIVBXF3RXZRJSMN4ASAJEJOOBYOK4AE`
 - Last addr before transfering to Binance `VX6JI2PB67HIRCVAERVCEKYD2Q3UGUGWTPWXWEYIDZMEAB4Q4VNHRHVKYY`
 - New malicious addr on 31 march 2023 but seems not related to addr above `MVEKYHFLJ63UKDYGNKCJD7WO5KFJZFVFMJPSDAWLDIDP4LUP575YDOW6GI`
 - Addr which gathered stolen algo before transfering to Binance on 21 april 2023 `KMQG24BRP4ZZWPGDJRDJPC3NQR5MFY5M24WSZGT2EXRYTEFE4YM2YFTV5E` (https://algoexplorer.io/tx/7GKZ2UHOTRF6GPWGZ5E7MBTDMONGMHN4SDCQ36C5Y3MSEPLO53HA)
 - April 28-29 : `KMQG..TV5E` continues to withdraw but using Gate.io instead. Over 6M algo transfered to this CEX from `BS2URPR7D3OSD4SMIK5QCJGP6CJCHCPQYC2V3D5QPERCOGTYZKDJP2NQ6I` 
## Requirements
Tested with:
 - python 3.10.10
 - pandas 1.5.3

## Usage
Pass Algo account pub address to 1st argument, excel sheet will be created in current directory
```
python3 algoalltx2excel.py VX6JI2PB67HIRCVAERVCEKYD2Q3UGUGWTPWXWEYIDZMEAB4Q4VNHRHVKYY
```


![algo_to_binance5](https://user-images.githubusercontent.com/127057042/227374662-e83c5bc0-9746-4389-ae3a-dd889c4d0994.png)
