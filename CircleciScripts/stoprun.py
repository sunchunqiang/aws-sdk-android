from utils import *
import sys
import os
import boto3
import datetime
import time
import demjson
from utils import runcommand
from collections import namedtuple

configurefile = sys.argv[1]
lastcommit = sys.argv[2]
tag = lastcommit[:10]

with open(configurefile, 'r') as jsonfile:
    jsonstring = jsonfile.read()
configure =  demjson.decode(jsonstring)

 
project_arn = configure['project_arn']
dummy_apk_arn = configure['dummy_apk_arn']
devicepool_arn = configure['devicepool_arn']
testspec_arn = configure['testspec_arn']
testmodulelist = configure['testmodulelist']


# session = boto3.session.Session(profile_name='default')
client = boto3.client('devicefarm', region_name='us-west-2')
 
#clean up old runs
response = client.list_runs(arn = project_arn)
while True: 
    now  = datetime.datetime.now()
    for run in response['runs']:
        status = run['status']
        if status != "COMPLETED":
            response = client.stop_run( arn = run['arn'] )

    if 'nextToken' in response:
        nextToken = response['nextToken']
        response = client.list_runs(arn = project_arn, nextToken = nextToken)
    else:
        break;
