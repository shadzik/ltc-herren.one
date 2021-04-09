cat header.html table.html footer.html > index.html

source /home/users/ltcherren/venv/bin/activate
python3 ltc-calendar.py > kalender-content.html

cat header.html kalender-content.html footer.html > kalender.html
cat header.html kontakt-content.html footer.html > kontakt.html
cat header.html 2019.html footer.html > table-2019.html
cat header.html 2020.html footer.html > table-2020.html
