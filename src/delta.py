from bs4 import BeautifulSoup
import requests

import time
from threading import Event, Thread

class RepeatedTimer:
	"""Repeat `function` every `interval` seconds."""

	def __init__(self, interval, function, *args, **kwargs):
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.start = time.time()
		self.event = Event()
		self.thread = Thread(target=self._target)
		self.thread.daemon = True
		self.thread.start()

	def _target(self):
		while not self.event.wait(self._time):
			self.function(*self.args, **self.kwargs)

	@property
	def _time(self):
		return self.interval - ((time.time() - self.start) % self.interval)

	def stop(self):
		self.event.set()
		self.thread.join()

URL = "http://tainangtrevietnam.vn/Page/VoteResult.aspx"

payload = {
	'txtCap': 'ABC',
	'holdCAP': 'ABC',
	'btnShow.x': '10',
	'btnShow.y': '17',
	'__VIEWSTATE': '/wEPDwULLTE1MjAwNzgxNTcPZBYCAgEPZBYCAgEPFgIeBFRleHQFQELDrG5oIGNo4buNbiAyMCBnxrDGoW5nIG3hurd0IHRy4bq7IFZp4buHdCBOYW0gdGnDqnUgYmnhu4N1IDIwMjJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQdidG5TaG93vvs98RoK0P1h+lowgg/w0jMPOKs='
}

def get_ranking():
	resp = requests.post(URL, data = payload)
	soup = BeautifulSoup(resp.text, features = 'html.parser')

	names, votes = [], []

	for name in soup.findAll('td', {'class': 'td1'}):
		names.append(name.text)

	for vote in soup.findAll('td', {'class': 'td3'}):
		votes.append(int(vote.text.strip().split()[0]))

	ranking = {}
	for name, vote in zip(names, votes):
		ranking[name] = vote
	return ranking

ranking = get_ranking()

def new_ranking():
	global ranking
	new_ranking = get_ranking()
	delta_ranking = {}
	for name, _ in new_ranking.items():
		delta_ranking[name] = new_ranking[name] - ranking[name]
	delta_ranking = dict(sorted(delta_ranking.items(), key=lambda x:x[1], reverse=True))
	ranking = new_ranking
	print("Delta:")
	for name, vote in delta_ranking.items():
		print(name + ": " + str(vote))
	print()

timer = RepeatedTimer(10, new_ranking)

while (True):
	command = input()
	if command == "stop":
		exit(0)
