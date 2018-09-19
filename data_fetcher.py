import requests

def fetch_data():
    r = requests.get("https://jsonplaceholder.typicode.com/users")
    print(r.status_code)
    return r.json()
