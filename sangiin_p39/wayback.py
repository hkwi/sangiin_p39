import re
import time
import datetime
import requests
import selenium.webdriver

def run():
	dr = selenium.webdriver.PhantomJS()
	
	urls = set()
	
	dr.get("http://www.sangiin.go.jp/japanese/joho1/kousei/giin/current/giinmei.htm")
	time.sleep(2)
	urls.add(dr.current_url)
	
	cur = []
	for a in dr.find_elements_by_xpath(".//a"):
		href = a.get_attribute("href")
		if href and "current" in href:
			cur += [href]
	for url in cur:
		dr.get(url)
		time.sleep(2)
		urls.add(dr.current_url)
	
	for url in urls:
		cdx = requests.get("http://web.archive.org/cdx/search/cdx",
			params=dict(url=url, output="json"))
		rows = cdx.json()
		rows = [dict(zip(rows[0], r)) for r in rows[1:]]
		if rows:
			tms = max([r["timestamp"] for r in rows])
			m = re.match("(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})", tms)
			tm = datetime.datetime(*tuple(map(int, m.groups())))
			if tm + datetime.timedelta(days=30) > datetime.datetime.now():
				continue
		
		dr.get("https://web.archive.org/save/%s" % url)
		time.sleep(2)

if __name__=="__main__":
	run()
