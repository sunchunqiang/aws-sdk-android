from utils import *
import sys
import os
import boto3
import datetime
import time
from collections import namedtuple
from send_email import *
import demjson

configurefile = sys.argv[1]
name = sys.argv[2]
 

with open(configurefile, 'r') as jsonfile:
    jsonstring = jsonfile.read()
configure =  demjson.decode(jsonstring)

project_arn =  configure['project_arn']
project_runlink = configure['project_runlink']

 
# session = boto3.session.Session(profile_name='default')
client = boto3.client('devicefarm', region_name='us-west-2')
 
 

module_result = namedtuple('module_result', 'name, result, total, passed, failed, warned, skipped, totalminutes')
response = client.list_runs(arn = project_arn)
resultlist = []
totals = 0 
passeds = 0
while True: 
    now  = datetime.datetime.now()
    for run in response['runs']:
        if name ==  run['name']:
            print(run)
            exit(0)
    if 'nextToken' in response:
        nextToken = response['nextToken']
        response = client.list_runs(arn = project_arn, nextToken = nextToken)
    else:
        break;
print("the run is not present")
