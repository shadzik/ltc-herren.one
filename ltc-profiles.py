from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
import os
import uuid
from pathlib import Path
home = str(Path.home())

url = "https://tvbb.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/teamPortrait?team=2775110&championship=TVBB+Sommer+2022&group=1733747"

profile_ids = ["18603557", "18551271", "17702734", "17702749", "18996974", "17952135", "18752536", "18003347", "18152123", "18252420"]

xpath = "//*[@id='content-row2']/table[3]"
before_xpath = "//*[@id='content-row2']/table[3]/tbody/tr["
id_xpath = "]/td[3]"
lk_xpath = "]/td[2]"
name_xpath = "]/td[4]"
single_xpath = "]/td[8]"
double_xpath = "]/td[9]"
overall_xpath = "]/td[10]"

options = Options()
options.headless = True
#driver = webdriver.Firefox(options=options, executable_path=home+'/bin/geckodriver')
#second_driver = webdriver.Firefox(options=options, executable_path=home+'/bin/geckodriver')
driver = webdriver.Chrome(options=options, executable_path=home+'/bin/chromedriver')
second_driver = webdriver.Chrome(options=options, executable_path=home+'/bin/chromedriver')
driver.get(url)

rows = len(driver.find_elements_by_xpath(xpath + "/tbody/tr"))

class Player:
  def __init__(self, id: str, name: str, lk: str, single: str, double: str, overall: str):
    self.id = id
    self.name = name
    self.lk = lk
    self.single = single
    self.double = double
    self.overall = overall


def write_html(players):
  cwd = os.getcwd()
  f = open(os.path.join(cwd, "player-content.html"), 'w')
  html_start = '''
    <div class="container">
    <h3>Team</h3>
    <div class="row row-cols-md-3">
  '''
  f.write(html_start)

  for player in players:
    player_html = f'''
      <div class="card" style="border-radius: 15px;">
        <div class="card-body p-4">
          <div class="d-flex text-black">
            <div class="flex-grow-1 ms-3">
              <h5 class="mb-1">{player.name}</h5>
              <p class="mb-2 pb-1" style="color: #2b2a2a;">{player.lk}</p>
              <div class="d-flex justify-content-start rounded-3 p-2 mb-2"
                style="background-color: #efefef;">
                <div>
                  <p class="small text-muted mb-1">Einzel</p>
                  <p class="mb-0">{player.single}</p>
                </div>
                <div class="px-3">
                  <p class="small text-muted mb-1">Doppel</p>
                  <p class="mb-0">{player.double}</p>
                </div>
                <div>
                  <p class="small text-muted mb-1">Gesamt</p>
                  <p class="mb-0">{player.overall}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    '''
    f.write(player_html)

  end_html = f'''
    </div>
      <div class="mb-4"></div>
      </div> <!-- container -->
  '''
  f.write(end_html)
  f.close()

players = []
for t_row in range(2, (rows + 1)):
  final_id_xpath = before_xpath + str(t_row) + id_xpath
  profile_id = driver.find_element_by_xpath(final_id_xpath).text.strip()
  if profile_id in profile_ids:
    final_lk_xpath = before_xpath + str(t_row) + lk_xpath
    final_name_xpath = before_xpath + str(t_row) + name_xpath
    final_single_xpath = before_xpath + str(t_row) + single_xpath
    final_double_xpath = before_xpath + str(t_row) + double_xpath
    final_overall_xpath = before_xpath + str(t_row) + overall_xpath

    profile_lk = driver.find_element_by_xpath(final_lk_xpath).text
    profile_name = driver.find_element_by_xpath(final_name_xpath).text
    profile_single = driver.find_element_by_xpath(final_single_xpath).text
    profile_double = driver.find_element_by_xpath(final_double_xpath).text
    profile_overall = driver.find_element_by_xpath(final_overall_xpath).text

    player = Player(id=profile_id, name=profile_name, lk=profile_lk, single=profile_single, double=profile_double, overall=profile_overall)
    players.append(player)

driver.quit()
write_html(players)
