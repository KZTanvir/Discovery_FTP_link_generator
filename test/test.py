import os, sys
import requests
sys.path.insert(1, os.getcwd()) 
from config import *
from lib import *

with requests.Session() as session:
    login_data['username'] = '01759800150'
    login_data['password'] = 'Tanvir1234#'
    session.post(login_url, data = login_data, headers = dflix_headers)
    login(session)
    item_lists = search(session,'series','hero academia')
    #items_list(item_lists,'SERIES')

    #initialization of variable supports
    item = item_lists[3]
    #FROM DEF DOWNLOAD LINK SERIES
    downloader_url = item[1]['item_url'] + '/'
    print(downloader_url)
    config.preview_payload['dir'] = downloader_url.replace(config.cds2_url,'') + '/'
    get_playlist = session.get(downloader_url, headers = config.dflix_headers)
    
    analyzer = BeautifulSoup(get_playlist.text, "html.parser")
    #print(analyzer.find('input')['value'])
    wrapper = analyzer.find_all('td', attrs = {'data-href': True})
    for item in wrapper:
        if item['data-href'].startswith('/') and item['data-href'].endswith('/'):
            direct = session.get(config.cds2_url+item['data-href'], headers = config.dflix_headers)
            wrapper_again = BeautifulSoup(direct.text, 'html.parser').find_all('td', attrs = {'data-href': True})
            for item_again in wrapper_again:
                if item_again['data-href'].startswith('/') and item['data-href'].endswith('/'):
                    print(item_again['data-href'])
                elif re.search('expires',item_again['data-href']):
                    print('this is the link')
                    print(item_again['data-href'])
        elif re.search('expires',item['data-href']):
            print('this is the link')
            print(item['data-href'])
    #MAIN FUNCTION PART ENDS HERE
    
    

