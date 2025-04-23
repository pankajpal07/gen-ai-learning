import requests
import os

def search_internet(query: str):
    print('SEARCHING: ', query)
    response = requests.get(f"https://api.search.brave.com/res/v1/web/search?q={query}&count=10", headers={ 'X-Subscription-Token': os.getenv('BRAVE_API_KEY') })
    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None