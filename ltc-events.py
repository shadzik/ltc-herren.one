from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
import os
import uuid
from pathlib import Path
home = str(Path.home())

url = "https://tvbb.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/groupPage?championship=TVBB+Sommer+2021&group=1635442"

xpath = "//*[@id='content-row2']/table[2]"
before_xpath = "//*[@id='content-row2']/table[2]/tbody/tr["
datetime_xpath = "]/td[2]"
host_xpath = "]/td[4]"
guest_xpath = "]/td[5]"

club = "Lichtenberger Tennisclub"

cal = Calendar()
cal.add('prodid', '-//LTC Herren 1 Kalender//ltc-scraper.py by Bartosz Swiatek//')
cal.add('version', '2.0')
calendarname = "ltc-herren1-full.ics"

options = Options()
options.headless = True
# driver = webdriver.Firefox(options=options, executable_path=home+'/bin/geckodriver')
# second_driver = webdriver.Firefox(options=options, executable_path=home+'/bin/geckodriver')
driver = webdriver.Chrome(options=options, executable_path=home+'/bin/chromedriver')
second_driver = webdriver.Chrome(options=options, executable_path=home+'/bin/chromedriver')
driver.get(url)

rows = len(driver.find_elements_by_xpath(xpath + "/tbody/tr"))
is_host = False
tmp_datetime = ""

def write_calendar(summary: str, start: datetime, end: datetime, description: str, location: str):
    calname = "ltc-herren1-" + datetime.strftime(start, "%Y%m%d") + ".ics"
    t_cal = Calendar()
    t_cal.add('prodid', '-//LTC Herren 1 Kalender//ltc-scraper.py by Bartosz Swiatek//')
    t_cal.add('version', '2.0')
    t_cal.add('method', 'request')
    event = Event()
    event.add('uid', uuid.uuid4().hex)
    event.add('summary', summary)
    event.add('dtstart', start)
    event.add('dtend', end)
    event.add('description', description)
    event.add('last-modified', datetime.now())
    event.add('dtstamp', datetime.now())
    event.add('location', location)
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('TRIGGER;RELATED=START', '-P1D')
    alarm.add('description', 'Erinnerung zum Punktspiel')
    event.add_component(alarm)
    t_cal.add_component(event)
    cal.add_component(event)
    cwd = os.getcwd()
    f = open(os.path.join(cwd, calname), 'wb')
    f.write(t_cal.to_ical())
    f.close()
    del alarm
    del event
    del t_cal

def write_html(calendar: Calendar):
    cwd = os.getcwd()
    f = open(os.path.join(cwd, "kalender-content.html"), 'w')
    html_start = '''
        <div class="container">
        <h3>Kalender Events</h3>
        <div class="row row-cols-1 row-cols-md-3 g-4">
    '''
    f.write(html_start)
    events = calendar.walk("VEVENT")
    events = sorted(events, key=lambda c: c.get("dtstart").dt, reverse=False)

    for event in events:
      s = event.decoded("dtstart")
      start = datetime.strftime(s, "%d.%m.%Y %H:%M")
      calname = "ltc-herren1-" + datetime.strftime(s, "%Y%m%d") + ".ics"
      html_event = f'''
      <div class="col">
        <div class="card text-dark bg-light mb-3">
        <div class="card-header">{start}</div>
          <div class="card-body">
            <h5 class="card-title">{event.get("summary")}</h5>
            <p class="card-text">{event.get("description")}</p>
            <a href="{calname}" class="btn btn-primary">Event importieren</a>
          </div>
          <div class="card-footer">
            <small class="text-muted"><b>Infos zum Gegner:</b><br/><br/>{event.get("location")}</small>
          </div>
        </div>
        </div>
      '''
      f.write(html_event)

    end_html = f'''
        </div>

        <div class="row">
          <div class="col text-center">
            <a href="{calendarname}" class="btn btn-primary">Alle Events importieren</a>
          </div>
        </div>

        <div class="mb-4"></div>
        </div> <!-- container -->
    '''
    f.write(end_html)
    f.close()

def find_location(club: str) -> str:
  xpath = "//*[@id='content-row2']/table[1]/tbody"
  club_xpath = f"//*[ text() = '{club}' ]"
  address_xpath = "//*[@id='content-row2']/table[1]/tbody/tr[1]/td[2]"
  elem = driver.find_element_by_xpath(xpath)
  club_url = elem.find_element_by_xpath(club_xpath).get_attribute('href')
  second_driver.get(club_url)
  address = second_driver.find_element_by_xpath(address_xpath).text
  return address


for t_row in range(2, (rows + 1)):
  is_host = False
  found_event = False
  final_datetime_xpath = before_xpath + str(t_row) + datetime_xpath
  final_host_xpath = before_xpath + str(t_row) + host_xpath
  final_guest_xpath = before_xpath + str(t_row) + guest_xpath
  datestr = driver.find_element_by_xpath(final_datetime_xpath).text
  hostclub = driver.find_element_by_xpath(final_host_xpath).text
  guestclub = driver.find_element_by_xpath(final_guest_xpath).text
  oponent = guestclub
  if not datestr.isspace():
    tmp_datetime = datestr
  if club in hostclub:
    found_event = True
    is_host = True
  if club in guestclub:
    found_event = True
    oponent = hostclub
  if found_event:
    if datestr.isspace():
      datestr = tmp_datetime
    location = find_location(oponent)
    date = datetime.strptime(datestr, "%d.%m.%Y %H:%M")
    meetingDate = date - timedelta(minutes=30)
    end = date + timedelta(hours=8)
    meetingTimeStr = datetime.strftime(meetingDate, "%H:%M")
    summary = ("Heimspiel " if is_host else "Auswärtsspiel ") + "gegen " + oponent
    description = "Bitte einen Tag vor dem Spiel gut ausruhen und viel Schlaf bekommen. Treffen ist um " + meetingTimeStr + (" auf unserer Anlage." if is_host else " beim " + oponent)
    write_calendar(summary=summary, start=date, end=end, description=description, location=location)
  
cwd = os.getcwd()
f = open(os.path.join(cwd, calendarname), 'wb')
f.write(cal.to_ical())
f.close()
write_html(cal)

driver.quit()
