import os
import re
import pickle
import subprocess
from bs4 import BeautifulSoup
from config import *

class DflixSessionManager:
    def __init__(self, session, username='', password=''):
        self.session = session
        self.username = username
        self.password = password
        self.cookie_file = 'User Info/cookies.bin'

    def _cookie_exists(self):
        return os.path.exists(self.cookie_file)

    def _save_cookies(self):
        with open(self.cookie_file, 'wb') as file:
            pickle.dump(self.session.cookies, file)

    def _load_cookies(self):
        with open(self.cookie_file, 'rb') as file:
            cookies = pickle.load(file)
            self.session.cookies.update(cookies)

    def idm_downloader(self, url):
        """Downloads files using Internet Download Manager (IDM) if installed."""
        idm_paths = {
            'x64': r"C:\Program Files (x86)\Internet Download Manager",
            'x32': r"C:\Program Files\Internet Download Manager"
        }

        idm_installed = next((path for path in idm_paths.values() if os.path.exists(path)), None)
        if idm_installed:
            # Adjust URL for IDM compatibility
            url = url.replace("md5=", "md5^=").replace("&expires=", "^&expires^=")
            cmd = f"IDMan.exe /n /a /d {url}"
            subprocess.run(["cmd.exe", "/c", cmd], creationflags=subprocess.CREATE_NO_WINDOW, cwd=idm_installed)
        else:
            print("Please install Internet Download Manager")

    def login(self):
        """Logs in the user by either loading cookies or using credentials."""
        if self._cookie_exists():
            self._load_cookies()
            return self.session, 1

        if self.username and self.password:
            login_data['username'] = self.username
            login_data['password'] = self.password
            self.session.post(login_url, data=login_data).text
            self._save_cookies()
            return self.session, 0

        return self.session, -1

    def relogin(self):
        """Logs out and logs back in."""
        self.logout()
        return self.login()

    def logout(self):
        """Logs the user out and deletes cookies."""
        self.session.get(url=logout_url, headers=dflix_headers)
        if self._cookie_exists():
            os.remove(self.cookie_file)
        return 0

    def get_profile_info(self):
        """Fetches and returns profile information."""
        try:
            profile_page = self.session.get(url=profile_url, headers=dflix_headers)
            profile_soup = BeautifulSoup(profile_page.text, "html.parser")
            profile_info = profile_soup.find('div', class_='col-lg-8')
            return profile_info.find_all('p', class_='text-white mb-0')[1:]
        except Exception as e:
            print(f"Error fetching profile info: {e}")
            return -1

    def search(self, search_term, search_type):
        """Searches for a term on either 'movies' or 'series' URLs."""
        search_urls = {
            'series': cds2_url,
            'movies': cds1_url
        }

        if search_type not in search_urls:
            print(f"Invalid search type: {search_type}")
            return []

        search_data['term'] = search_term
        search_data['types'] = search_type

        try:
            search_list = self.session.post(url=search_urls[search_type], headers=dflix_headers, data=search_data)
            search_items = BeautifulSoup(search_list.text, "html.parser").find_all('div', class_='moviesearchiteam ps-1 mb-1')
            item_list = [
                {
                    'count': count,
                    'item_name': item.find('div', class_='searchtitle').text,
                    'item_info': item.find('div', class_='searchdetails').text.replace('<br>', ''),
                    'item_url': item.find('a')['href'],
                    'type': search_type
                }
                for count, item in enumerate(search_items)
            ]
            return item_list
        except Exception as e:
            print(f"Error searching: {e}")
            return []

    def link_crawler(self, select_url, crawl_type):
        """Crawls through the links on a page."""
        target_url = cds2_url if crawl_type == "series" else cds1_url

        try:
            crawler_soup = BeautifulSoup(self.session.get(url=select_url, headers=dflix_headers).text, 'html.parser')
            crawler_data = crawler_soup.find_all('td', attrs={'data-href': True})
            crawler = []

            for contents in crawler_data:
                href = contents['data-href']
                if href.startswith('/') and href.endswith('/'):
                    crawler += self.link_crawler(target_url + href, crawl_type)
                elif 'expires' in href:
                    crawler.append(target_url + href)
            return crawler

        except Exception as e:
            print(f"Error during crawling: {e}")
            return []


import requests

# Assuming your session object and credentials
session = requests.Session()
username = '01759800150'  # Replace with your username
password = 'TanvirTanvirTanvir'  # Replace with your password

# Create an instance of DflixSessionManager
dflix_manager = DflixSessionManager(session, username, password)

# Login and check status
session, status = dflix_manager.login()

if status == 0:
    print("Logged in successfully.")
elif status == 1:
    print("Logged in using saved cookies.")
else:
    print("Login failed.")
# Fetch and print user profile information
profile_info = dflix_manager.get_profile_info()
if profile_info != -1:
    print("User Profile Details:")
    for detail in profile_info:
        print(detail.text.strip())  # Printing the text content of each profile detail
else:
    print("Failed to retrieve profile information.")
