
if [ -z "$1" ]
then
    read -p "new sdk version:" sdkversion

else
	sdkversion="$1"
fi

echo "start rlease android sdk $sdkversion ..."
read -p "continuekey? [yes/no]:" continuekey
echo &continuekey

if [ "$continuekey" != "yes" ] && [ "$continuekey" != "y" ]
then
	echo "stop releasing android sdk"
	exit 1
fi

git checkout bump_sdk_version
git pull --rebase
echo "sdkversion" >> version
git add version
git commit -m "bump android sdk version $sdkversion"
git push
 

