#!/bin/bash
PATH=/home/users/ltcherren/node_modules/puppeteer/.local-chromium/linux-848005/chrome-linux:$PATH

cat header.html table.html footer.html > index.html

source /home/users/ltcherren/venv/bin/activate
# python3 ltc-calendar.py > kalender-content.html
python3 ltc-events.py
python3 ltc-profiles.py

cat header.html kalender-content.html footer.html > kalender.html
cat header.html kontakt-content.html footer.html > kontakt.html
cat header.html player-content.html footer.html > team.html
#cat header.html 2019.html footer.html > table-2019.html
#cat header.html 2020.html footer.html > table-2020.html
