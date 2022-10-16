import requests,pickle,os,re
from bs4 import BeautifulSoup
import config
from subprocess import call
from time import sleep

def clear():
    _ = call('clear' if os.name =='posix' else 'cls')
    return

def login(session):
    if os.path.exists('cookies.bin'):
        with open('cookies.bin', 'rb') as file:
            cookies = pickle.load(file)
            session.cookies.update(cookies)
    else:
        config.login_data['username'] = input("Enter your username: ")
        config.login_data['password'] = input("Enter your password: ")
        
        session.post(config.login_url, data = config.login_data)
        with open('cookies.bin', 'wb') as file:
            pickle.dump(session.cookies, file)
        print('You are logged in.')
    try:
        profile_page = session.get(config.profile_url, headers = config.dflix_headers)
        profile_soup = BeautifulSoup(profile_page.text, "html.parser")
        profile_info =  profile_soup.find('div', class_='col-lg-8')
        profile_info.find_all('p', class_='text-muted mb-0')
    except:
        clear()
        print_ui()
        print('Login failed. Please try again.')
        session = relogin(session)
    return session

def relogin(session):
    logout(session)
    session = login(session)
    return session

def logout(session):
    session.get(config.logout_url, headers = config.dflix_headers)
    if os.path.exists('cookies.bin'):
        os.remove('cookies.bin')
    print("You are logged out.")
    return 0

def get_profile_info(session):
    profile_page = session.get(config.profile_url, headers = config.dflix_headers)
    profile_soup = BeautifulSoup(profile_page.text, "html.parser")
    profile_info =  profile_soup.find('div', class_='col-lg-8')
    user_data = profile_info.find_all('p', class_='text-muted mb-0')
    print(f'''
        ==================================
        ********[User information]********
        ==================================
        User Name  : {user_data[0].text}
        User Email : {user_data[1].text}
        User Phone : {user_data[2].text}
    ''')
    return 0
def search(session,search_type,search_term):
    #search data lies here
    config.search_data['term'] = search_term
    config.search_data['types'] = search_type
    # this is the searching part by getting the search data
    search_list = session.post(config.search_url, headers = config.dflix_headers, data = config.search_data)
    #this works as  getting the items list from the search
    search_item = BeautifulSoup(search_list.text, "html.parser").find_all('div', class_='moviesearchiteam ps-1 mb-1')
    item_list = []
    count = 0
    for item in search_item:
        item_url = item.find('a')['href']
        item_name = item.find('div', class_='searchtitle').text
        item_info = item.find('div', class_='searchdetails').text.replace('<br>','')
        item_list.append([
            {'count': count},
                {
                'item_name' : item_name,
                'item_info' : item_info,
                'item_url'  : item_url
                }])
        count += 1
    return item_list

def items_list(items):
    for item in items:
        print(f'''
        Serch Item  : {item[0]['count']}
        Serch Name  : {item[1]['item_name']}
        Serch Info  : {item[1]['item_info']}
        Serch Url   : {item[1]['item_url']}
        ''')
        sleep(0.5)
        #the end of the item list
    return 0

def download_list(session,item): #this is for tv series download
    downloader_url = item[1]['item_url'] + '/'
    config.preview_payload['dir'] = downloader_url.replace(config.cds2_url,'') + '/'
    get_playlist = session.post(downloader_url, headers = config.dflix_headers, data = config.preview_payload)
    print(get_playlist.text)
    if os.path.exists('links.txt'):
        os.remove('links.txt')

    for line in get_playlist.text.split('\n'):
        if re.search('http', line.strip()):
            with open('links.txt','a') as file:
                file.write(line + '\n')
                file.close()
    return 0


def pmain():
    session = requests.Session()
    login(session)
    get_profile_info(session)
    search_type = 'series'
    search_term = input("Enter the search term: ")
    items = search(session,search_type,search_term)
    items_list(items)
    item_number = int(input("Enter the item number: "))
    download_list(session,items[item_number])
    #logout(session)
    return 0

def print_ui():
    print('''
        ==============================
        ****[DFLIX LINK GENERATOR]****
        ==============================
        1.RE-LOGIN
        2.SEARCH SERIES
        3.SEARCH MOVIES(WORK IN PROGRESS)
        4.GENERATE LINKS
        5.LOGOUT
        6.EXIT
        ''')
    return
def user_warning():
    print('''
        ==============================
        ********[User Agrement]*******
        ==============================
        1. This script is for educational purpose only.
        2. This script is not for commercial use.
        3. This script is not for any illegal use.
        4. This script is for personal use only.
        ''')
    if os.path.exists('user_agreement.tanvir'):
        with open('user_agreement.tanvir','r') as file:
            if file.read() == 'Yes':
                return 0
            else:
                print('You have to agree with the user agreement.')
                sleep(1)
                print('Please read the user agreement carefully.')
                print('Program exited.')
                os.remove('user_agreement.tanvir')
                exit()
    else:
        with open('user_agreement.tanvir','w') as file:
            if input("Do you agree with the above terms and conditions? (y/n): ").lower() == 'y':
                file.write('Yes')
                file.close()
            else:
                file.write('No')
                file.close()
                print('You have to agree with the user agreement.')
                sleep(1)
                print('Please read the user agreement carefully.')
                sleep(1)
                print('Program exited.')
                sleep(1)
                print('You are not allowed to use this script.')
                exit()
    return