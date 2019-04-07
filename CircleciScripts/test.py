
import os

print(r"https://circleci.com/gh/{0}/{1}/{2}".format(os.environ.get('CIRCLE_PROJECT_USERNAME'), os.environ.get('CIRCLE_PROJECT_REPONAME'), os.environ.get('CIRCLE_BUILD_NUM')))