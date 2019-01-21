from functions import getmodules
from functions import replacefiles
from functions import runcommand
import sys
import os

root = sys.argv[1]
projects = list(filter(lambda x: os.path.isdir(os.path.join(root, x)), os.listdir(root)))

exitcode = 0 ; 
for project in projects:
	projectfolder = os.path.join(root, project) 
	gradlewpath = os.path.join(projectfolder, "gradlew")
	if os.path.isfile(gradlewpath):
		rn = runcommand(command = "bash '{0}'  assemble".format(gradlewpath), workingdirectory = projectfolder)
		if rn != 0 :
			exitcode = 1
	else:
		print(gradlewpath, "is not present")
exit(exitcode)
