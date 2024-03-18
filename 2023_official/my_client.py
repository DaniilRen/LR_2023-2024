import requests

def get_coords():
	return requests.get(f'http://127.0.0.1:4001/').json()

print(get_coords())