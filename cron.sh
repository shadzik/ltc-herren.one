#!/bin/bash
PATH=/home/users/ltcherren/.nvm/versions/node/v15.4.0/bin:/home/users/ltcherren/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/X11R6/bin:/usr/local/bin:/home/users/ltcherren/bin
export PATH

cd /home/users/ltcherren/ltc-herren.one

node herren1.js > table.html.tmp
MD5=$(md5sum table.html.tmp |awk '{print $1}')
MD5O=$(md5sum table.html |awk '{print $1}')

if [ $MD5 = $MD5O ]; then
  exit 0
fi

DATE=$(date)
echo "${DATE}: Updating..."
echo "${DATE}: Moving new table"
mv table.html.tmp table.html
echo "${DATE}: Creating site"
./makeSite.sh
