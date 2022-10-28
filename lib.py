import pickle,os,re
from bs4 import BeautifulSoup
from config import *
from subprocess import call
from custom_ui import print_ui

def clear():
    _ = call('clear' if os.name =='posix' else 'cls')
    return

def login(session):
    if os.path.exists('User Info/cookies.bin'):
        with open('User Info/cookies.bin', 'rb') as file:
            cookies = pickle.load(file)
            session.cookies.update(cookies)
    else:
        login_data['username'] = input("Enter your username: ")
        login_data['password'] = input("Enter your password: ")
        
        session.post(login_url, data = login_data)
        with open('User Info/cookies.bin', 'wb') as file:
            pickle.dump(session.cookies, file)
        print('You are logged in.')
    try:
        profile_page = session.get(url = profile_url, headers = dflix_headers)
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
    session.get(url = logout_url, headers = dflix_headers)
    if os.path.exists('User Info/cookies.bin'):
        os.remove('User Info/cookies.bin')
    print("You are logged out.")
    return 0

def get_profile_info(session):
    try:
        profile_page = session.get(url = profile_url, headers = dflix_headers)
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
    except:
        print('Profile info not found.')
    return 0
def search(session,search_type,search_term):
    #search data lies here
    search_data['term'] = search_term
    search_data['types'] = search_type
    # this is the searching part by getting the search data
    search_list = session.post(url = search_url, headers = dflix_headers, data = search_data)
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

def link_crawler(session,select_url):
    crawler = []
    crawler_soup = BeautifulSoup(session.get(url = select_url,headers = dflix_headers).text, 'html.parser')
    crawler_data = crawler_soup.find_all('td', attrs= {'data-href':True})
    for contents in crawler_data:
        if contents['data-href'].startswith('/') and contents['data-href'].endswith('/'):
            crawler = crawler + link_crawler(session, cds2_url + contents['data-href'])
        elif re.search('expires',contents['data-href']):
            ## THIS IS FOR SAVING LINKS IN A TEXT FILE
            #with open('test.txt','a+') as file:
                #file.write(cds2_url + contents['data-href'] + '\n')
                #file.close()
            ## THIS BLOCK ENDS HERE
            crawler.append(cds2_url + contents['data-href'])
    return crawler