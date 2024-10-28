import requests

# The login URL
url = 'https://dflix.discoveryftp.net/login/auth'

# Payload containing form data
login_data = {
    'username': '01759800150',#CHNAGE THIS WITH YOUR USERNAME
    'password': 'TanvirTanvirTanvir',#CHNAGE THIS WITH YOUR PASSWORD
    'remember': 'on',#DO NOT CHANGE THIS
    'loginsubmit': ''#DO NOT CHANGE THIS
}

dflix_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }


# Send a POST request
session = requests.Session()
response = session.post(url, data=login_data, headers=dflix_headers)
response2 = session.get("https://dflix.discoveryftp.net/m", headers=dflix_headers)
# Print the response
print(response.status_code)
print(response.text)  # This will show the HTML of the page, or you can process it further

print()