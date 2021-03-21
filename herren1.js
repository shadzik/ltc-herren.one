const { doesNotMatch } = require('assert');
const puppeteer = require('puppeteer')

async function scrapeTable(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url);

  const el = await page.$x('//*[@id="content-row2"]/h1');
  const title = await page.evaluate(el => el.textContent, el[0]);
  console.log("<div class='container'>");
  console.log("<h3>"+title+"</h3>");
  console.log('<div class="mb-4"></div>');

  const xpaths = ['//*[@id="content-row2"]/table[1]', '//*[@id="content-row2"]/table[2]'];
  for (let xpath of xpaths) {
	  const table = await page.$x(xpath);
    const changeClass = await page.evaluate(() => {
      const anchors = Array.from(document.querySelectorAll('table'));
      anchors.map(table => table.setAttribute('class', "table"));
      const tables = anchors.map(table => table.getAttribute('class'));
	    return tables;
    })
	  const data = await page.evaluate(() => {
	    const anchors = Array.from(document.querySelectorAll('table tbody tr td a'));
	    anchors.map(td => {
        var href = td.getAttribute('href');
        if (!href.includes('tvbb.liga.nu')) {
          td.setAttribute('href', "https://tvbb.liga.nu" + td.getAttribute('href'));
        }
      });
	    const links = anchors.map(td => td.getAttribute('href'));
	    return links;
	  })
	  const result = await page.evaluate(el => el.outerHTML, table[0]);
	  console.log(result);
    console.log('<div class="mb-4"></div>');
  }

  browser.close();
  var d = new Date();
  var currentDate = d.getDate() + "."
                + (d.getMonth()+1)  + "." 
                + d.getFullYear();  

  var currentTime = d.toLocaleTimeString('de-DE', { hour12: false })

  console.log("<div>Scraped: " + currentDate + " " + currentTime + "</div>");
  console.log("</div>");
}


// 2021
scrapeTable('https://tvbb.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/groupPage?championship=TVBB+Sommer+2021&group=1635442');
// 2020
// scrapeTable('https://tvbb.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/groupPage?championship=TVBB+Sommer+2020&group=1539516');
// 2019
// scrapeTable('https://tvbb.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/groupPage?championship=TVBB+Sommer+2019&group=1428138');