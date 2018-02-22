import time
from selenium import webdriver
from BeautifulSoup import BeautifulSoup

url = "https://domaintyper.com/top-websites"

def lookupPrimary(url, driver, crawled_urls):
	driver.get(url)
	html = driver.page_source.encode("utf-8")
	soup = BeautifulSoup(html)
	urls = soup.findAll("a")
	urls_list = list()
	for a in urls:
		if "top-websites" in a.get("href"):
			if (a.get("href")) and (a.get("href") not in urls_list):
				urls_list.append("https://domaintyper.com" + a.get("href"))
	for b in urls_list:
		lookupSecondary(b, driver, crawled_urls)
	
def lookupCheck(url, driver, crawled_urls):
	driver.get(url)
	html = driver.page_source.encode("utf-8")
	soup = BeautifulSoup(html)
	columns = list()
	rows = list()
	columns = soup.findAll('div', attrs={"class" : "pagingDivDisabled"})
	rows = soup.findAll('div', attrs={"class" : "pagingDiv"})
	urlTable = soup.findAll('a', attrs={"title" : re.compile('^(Whois Record)')})
	print '*********************'
	print rows
	if any(rows) and "Next" in rows[-1]:
		crawl_urls(urlTable, crawled_urls)
		nextPageURL = soup.findAll('a', attrs={"class" : "pagingLink"})
		nextPageURL = "https://domaintyper.com" + nextPageURL[-1].get("href")
		print nextPageURL
		lookupCheck(nextPageURL, driver, crawled_urls)
	
def crawl_urls(urlTable, crawled_urls):
	for a1 in urlTable:
		for a2 in a1.contents:
			if a2 not in crawled_urls:
				crawled_urls.append(a2)
		
if __name__ == "__main__":
	driver = webdriver.Firefox()
	crawled_urls = list()
	lookupPrimary(url, driver, crawled_urls)
	driver.quit()