import json 
from datetime import datetime
import requests
from os.path import exists
import os
import ast

def init():
    ipsDict = {}
    jsonFilePath = 'ips.json'
    target = 'https://check.torproject.org/torbulkexitlist'
    ips = requests.get(target, allow_redirects=False)
    ips = str(ips.content.decode("utf-8"))
    ips = ips.split("\n")

    for ip in ips:
        dict = {"ip": ip, "addedDate":str(datetime.now())}
        ipsDict[ip] = dict

    ips = json.dumps(ipsDict, indent=4, sort_keys=True)
    dateNow = datetime.now()
    dateNow = dateNow.strftime("%Y-%M-%d-%H%M%S")
    if exists(jsonFilePath):
        os.rename(jsonFilePath, jsonFilePath+str(dateNow))

    open(jsonFilePath , 'wb').write(bytes(ips,"utf-8"))

target = 'https://check.torproject.org/torbulkexitlist'
jsonFilePath = 'ips.json'
ips = requests.get(target, allow_redirects=False)
ips = str(ips.content.decode("utf-8"))
ips = ips.split("\n")

if not exists(jsonFilePath) or os.stat(jsonFilePath).st_size == 0:
    init()
currIps = {}
with open(jsonFilePath) as fips:
    currIps = fips.read()
    currIps = ast.literal_eval(currIps)

currIpsList = list(currIps.keys())

for ip in ips:
    if not ip in currIpsList:
        currIps[ip] = {"ip":ip, "addedDate":str(datetime.now())}

for ip in currIpsList:
    if not ip in ips:
        currIps[ip] = {"ip":ip, "addedDate":currIps[ip]["addedDate"] , "lastSeen": str(datetime.now())}

currIps = json.dumps(currIps, indent=4, sort_keys=True)
open(jsonFilePath , 'wb').write(bytes(currIps,"utf-8"))