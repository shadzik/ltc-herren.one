from icalendar import Calendar, Event, vDatetime
import requests
from datetime import datetime
import os

url = "https://ltc-herren.one/nextcloud/remote.php/dav/public-calendars/xpzTca5bCNFftAqE/?export"
c = Calendar.from_ical(requests.get(url).text)

print('''
    <div class="container">
    <h3>Auf einen Blick</h3>
    <div class="row row-cols-1 row-cols-md-3 g-4">
''')

events = c.walk("VEVENT")
events = sorted(events, key=lambda c: c.get("dtstart").dt, reverse=False)

for event in events:
  s = event.decoded("dtstart")
  start = datetime.strftime(s, "%d.%m.%Y %H:%M")
  calname = "ltc-herren1" + datetime.strftime(s, "%Y%m%d") + ".ics"
  print(f'''
  <div class="col">
    <div class="card text-dark bg-light mb-3">
    <div class="card-header">{start}</div>
      <div class="card-body">
        <h5 class="card-title">{event.get("summary")}</h5>
        <p class="card-text">{event.get("description")}</p>
        <a href="{calname}" class="btn btn-primary">Event importieren</a>
      </div>
      <div class="card-footer">
        <small class="text-muted">Adresse: {event.get("location")}</small>
      </div>
    </div>
    </div>
  ''')
  cal = Calendar()
  cal.add('prodid', '-//My calendar product//mxm.dk//')
  cal.add('version', '2.0')
  cal.add_component(event)
  cwd = os.getcwd()
  f = open(os.path.join(cwd, calname), 'wb')
  f.write(cal.to_ical())
  f.close()

print(f'''
    </div>

    <div class="row">
      <div class="col text-center">
        <a href="{url}" class="btn btn-primary">Alle Events importieren</a>
      </div>
    </div>

    <div class="mb-4"></div>
    </div> <!-- container -->
''')
