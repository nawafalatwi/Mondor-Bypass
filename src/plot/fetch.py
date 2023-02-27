from bs4 import BeautifulSoup
import requests

URL = "http://tainangtrevietnam.vn/Page/VoteResult.aspx"

payload = {
	'txtCap': 'ABC',
	'holdCAP': 'ABC',
	'btnShow.x': '10',
	'btnShow.y': '17',
	'__VIEWSTATE': '/wEPDwULLTE1MjAwNzgxNTcPZBYCAgEPZBYCAgEPFgIeBFRleHQFQELDrG5oIGNo4buNbiAyMCBnxrDGoW5nIG3hurd0IHRy4bq7IFZp4buHdCBOYW0gdGnDqnUgYmnhu4N1IDIwMjJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQdidG5TaG93vvs98RoK0P1h+lowgg/w0jMPOKs='
}

def fetch_rankings() -> dict[str, int]:
	response = requests.post(URL, data = payload)
	soup = BeautifulSoup(response.text, features = 'html.parser')

	result = {}

	for name, vote in zip(soup.findAll('td', {'class': 'td1'}),
						  soup.findAll('td', {'class': 'td3'})):
		result[name.text] = int(vote.text.strip().split()[0])
	return result

previous_ranking = None
def fetch_rankings_delta() -> list[tuple[str, int]] | None:
	global previous_ranking
	ranking = fetch_rankings()
	if previous_ranking is None:
		previous_ranking = ranking
		return None

	result = []
	for name, pvalue in previous_ranking.items():
		result.append((name, ranking[name] - pvalue))
	
	result = sorted(result, key = lambda x: x[0])
	previous_ranking = ranking
	return result
