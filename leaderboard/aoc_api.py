import aocd
import requests

# Get user token
user = aocd.get.default_user()
token = user.token

def get(url):
    return requests.get(url, cookies={'session': token})
