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
lastcommit = sys.argv[2]
tag = lastcommit[:10] 

with open(configurefile, 'r') as jsonfile:
    jsonstring = jsonfile.read()
configure =  demjson.decode(jsonstring)

project_arn =  configure['project_arn']
project_runlink = configure['project_runlink']

 
# session = boto3.session.Session(profile_name='default')
client = boto3.client('devicefarm', region_name='us-west-2')
 

module_result = namedtuple('module_result', 'name, result, total, passed, failed, warned, skipped, errored,  totalminutes')
response = client.list_runs(arn = project_arn)
resultlist = []
totals = 0 
passeds = 0
while True: 
    now  = datetime.datetime.now()
    for run in response['runs']:

        status = run['status']
        if status != 'COMPLETED' :
            continue
        testname =  run['name']
        if not testname.endswith(tag):
            continue
        totals += 1
        if run['result'] == "PASSED":
            passeds += 1
        # testname = testname[:-len(tailtag)]
        # if testname.endswith("-test"):
        #     testname = testname[:-5]
        result = module_result(
        name = testname ,       
        result = run['result'] ,
        total = int(run['counters']['total']) - 2 ,
        passed = int(run['counters']['passed']) - 2 ,
        failed = run['counters']['failed'] ,
        warned = run['counters']['warned'] ,
        skipped = run['counters']['skipped'] ,    
        errored = run['counters']['errored'] ,  
        totalminutes = run['deviceMinutes']['total']
        )

        # print(result)
        resultlist.append(result)
        # if  name.endswith(tag):
        #     print(run)
    if 'nextToken' in response:
        nextToken = response['nextToken']
        response = client.list_runs(arn = project_arn, nextToken = nextToken)
    else:
        break;

htmloutput = "<b>Totals: {0}</b> <br>".format(totals)
htmloutput += "<b>Passed: {0}</b>  <br>".format(passeds)
htmloutput += "<b>Last commit: {0}</b>  <br>".format(lastcommit)
htmloutput += '<a href="{0}">Detail for more information. </a> <br>'.format(project_runlink)
htmloutput += "<br> <br>"
htmloutput +=  """<table> 
              <tr align="left"  bgcolor="#A9A9A9">
                <th width="300">Test name</th>
                <th width="80">Result</th>
                <th width="50">Total</th>
                <th width="50">Passed</th>
                <th width="50">Failed</th>
                <th width="50">Warned</th>
                <th width="50">Skipped</th>
                <th width="50">Errored</th>
                <th width="100">Total miniutes</th>
              </tr>
              """



for result in resultlist:
    print(result)
    if result.result == 'PASSED':
        bgcolor = "#00FF00"
    else:
        bgcolor = "#FF0000"
    htmloutput +=  \
            """<tr bgcolor="{8}">
                <td>{0}</td>
                <td>{1}</td>
                <td>{2}</td>
                <td>{3}</td>
                <td>{4}</td>
                <td>{5}</td>
                <td>{6}</th>
                <td>{7}</th>
                <td>{8}</th>
              </tr>
            """.format(result.name, result.result, result.total, result.passed, result.failed, result.warned, result.skipped, result.errored,result.totalminutes, bgcolor)
htmloutput += "</table>"
title = "Anroid SDK Integration test result Passed:{0} Failed:{1}".format(passeds, totals - passeds)
send_email(title, htmloutput , contentformat = ContentFormat.Html, fromaddress = configure['email_from'], toaddresses = configure['email_to'] )

