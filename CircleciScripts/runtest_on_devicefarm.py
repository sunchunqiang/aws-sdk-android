from utils import *
import sys
import os
import boto3
import datetime
import time
import demjson
from utils import runcommand

base=sys.argv[1]
configurefile = sys.argv[2]
lastcommit = sys.argv[3]
tag = lastcommit[:10]

with open(configurefile, 'r') as jsonfile:
    jsonstring = jsonfile.read()
configure =  demjson.decode(jsonstring)

keepoldrundays = configure['keepoldrundays']
project_arn = configure['project_arn']
dummy_apk_arn = configure['dummy_apk_arn']
devicepool_arn = configure['devicepool_arn']
testspec_arn = configure['testspec_arn']
testmodulelist = configure['testmodulelist']


# session = boto3.session.Session(profile_name='default')
client = boto3.client('devicefarm', region_name='us-west-2')
 
# clean up old uploads
response = client.list_uploads(arn = project_arn, type = 'INSTRUMENTATION_TEST_PACKAGE')
while True:
	
	now  = datetime.datetime.now()
	for upload in response['uploads']:

		createdtdays= (now - upload['created'].replace(tzinfo=None)).days
		status = upload['status']
		name = upload['name']
		if (createdtdays >= keepoldrundays or status != 'SUCCEEDED') and name.startswith("aws-android-sdk-") :
			print("delete old upload:", name)
			arn = upload['arn']
			client.delete_upload(arn = arn)
	if 'nextToken' in response:
		nextToken = response['nextToken']
		response = client.list_uploads(arn = project_arn, type = 'INSTRUMENTATION_TEST_PACKAGE', nextToken = nextToken)
	else:
		break;
#clean up old runs
response = client.list_runs(arn = project_arn)
while True:	
	now  = datetime.datetime.now()
	for run in response['runs']:
		name = run['name']
		createdtdays = (now - run['created'].replace(tzinfo=None)).days
		status = run['status']
		print(status, createdtdays, run['created'], name)
		if  createdtdays >= keepoldrundays  and status != "PENDING" and status != 'RUNNING':
			print("delete old run:", name)
			arn = run['arn']
			client.delete_run(arn = arn)
	if 'nextToken' in response:
		nextToken = response['nextToken']
		response = client.list_runs(arn = project_arn, nextToken = nextToken)
	else:
		break;


for module in testmodulelist:
	name = module[16:]
	if name.endswith('-test'):
		name = name[:-5]	
	print("#################### {0} ####################".format(name))
	command = "bash gradlew :{0}:assembleAndroidTest".format(module)
	rn = runcommand(command)
	if rn != 0 :
		print("failed to build test module:", module)
		continue;
	apkfile = os.path.join(base, module, "build/outputs/apk/androidTest/debug/{0}-debug-androidTest.apk".format(module))
	if not os.path.isfile(apkfile) :
		print("cannot find test module apk:", apkfile)
		print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		continue
	response = client.create_upload(
	    projectArn = project_arn,
	    name='{0}-debug-androidTest-{1}.apk'.format(module, tag),
	    type='INSTRUMENTATION_TEST_PACKAGE'
	)
	uploadarn =  response['upload']['arn']
	status = response['upload']['status']
	if status != 'INITIALIZED':
		print("Failed to create upload")
		print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		continue

	uploadurl = response['upload']['url']
	# apkfile = "/Users/sdechunq/Documents/github/private/aws-sdk-android-personal/aws-android-sdk-sns-test/build/outputs/apk/androidTest/debug/aws-android-sdk-sns-test-debug-androidTest.apk"
	uploadcommand = 'curl -T "{0}"  "{1}"'.format(apkfile, uploadurl)  
	rn = runcommand(uploadcommand)
	if rn != 0 :
		print("Failed to run curl upload:", module)
		print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		continue

	while  status != 'SUCCEEDED' and status != 'FAILED' :	
		print("upload status:", status)
		time.sleep(5)
		response = client.get_upload(arn = uploadarn)
		status = response['upload']['status']
	if status == 'FAILED':
		print("Failed to upload test apk for ", module)
		print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		continue;

	response = client.schedule_run(
	    projectArn = project_arn,
	    appArn = dummy_apk_arn,
	    devicePoolArn= devicepool_arn,
	    name='{0}-{1}'.format(name, tag),
	    test={
	        'type': 'INSTRUMENTATION',
	        'testPackageArn': uploadarn,
	        # 'testSpecArn': testspec_arn
	    }
	)
	print(response['run']['status'], response['run']['result'])
print("done")




