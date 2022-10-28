import os,requests,sys
sys.path.insert(1,os.getcwd())
from config import *
from lib import *


with requests.Session() as session:
    login_data['username'] = '01759800150'
    login_data['password'] = 'Tanvir123'
    session.post(login_url, data = login_data, headers = dflix_headers)
    login(session)
    item_lists = search(session = session,search_type = 'series',search_term = 'see')
    #items_list(item_lists,search_type= 'Series')
    select_url = item_lists[0][1]['item_url'] + '/'
    #print(select_url)
    crawled_links = link_crawler(session = session, select_url = select_url)
    for links in crawled_links:
        print(links)