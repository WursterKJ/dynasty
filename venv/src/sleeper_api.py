import requests
url = "https://api.sleeper.app/v1/user/KyleWurster"
pull = requests.get(url).json()
print(pull)


