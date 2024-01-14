#Name: Adam Sherer
#Date: 12/5/2022
#Description: Multi-threaded web crawler for intro to operating systems

#You also have to run the following commands to install a couple of libraries that we will need for the web crawler

#pip install bs4
#pip install requests

#These are all the libraries we will need to load
import multiprocessing
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests
import time

x = time.time()

class MultiThreadedCrawler:

	def __init__(self, seed_url):
		self.seed_url = seed_url
		self.root_url = '{}://{}'.format(urlparse(self.seed_url).scheme,
										urlparse(self.seed_url).netloc)
		self.pool = ThreadPoolExecutor(max_workers=10)
		self.scraped_pages = set([])
		self.crawl_queue = Queue()
		self.crawl_queue.put(self.seed_url)

	def parse_links(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		Anchor_Tags = soup.find_all('a', href=True)
		for link in Anchor_Tags:
			url = link['href']
			if url.startswith('/') or url.startswith(self.root_url):
				url = urljoin(self.root_url, url)
				if url not in self.scraped_pages:
					self.crawl_queue.put(url)

	def post_scrape_callback(self, res):
		result = res.result()
		if result and result.status_code == 200:
			self.parse_links(result.text)

	def scrape_page(self, url):
		try:
			res = requests.get(url, timeout=(3, 30))
			return res
		except requests.RequestException:
			return

	def run_web_crawler(self):
		while True:
			try:
				print("\n Name of the current executing process: ",
					multiprocessing.current_process().name, '\n')
				target_url = self.crawl_queue.get(timeout=60)
				if target_url not in self.scraped_pages:
					print("Scraping URL: {}".format(target_url))
					self.current_scraping_url = "{}".format(target_url)
					self.scraped_pages.add(target_url)
					job = self.pool.submit(self.scrape_page, target_url)
					job.add_done_callback(self.post_scrape_callback)

			except Empty:
				return
			except Exception as e:
				print(e)
				continue

	def info(self):
		print('\n Seed URL is: ', self.seed_url, '\n')
		print('Scraped pages are: ', self.scraped_pages, '\n')


if __name__ == '__main__':
	cc = MultiThreadedCrawler("https://crawler-test.com/")
	cc.run_web_crawler()
	cc.info()

y = time.time()
t = y-x
print("Time is: " + str(t))