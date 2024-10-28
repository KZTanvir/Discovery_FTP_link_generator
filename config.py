#the config lies here

#the url of the dflix site is here
primary_url  = 'https://dflix.discoveryftp.net'
login_url    = primary_url + '/login/auth'
index_url    = primary_url + '/m'
profile_url  = primary_url + '/profile'
logout_url   = primary_url + '/login/destroy'
search_url   = primary_url + '/search'
cds2_url     = 'http://cds2.discoveryftp.net'
cds1_url     = 'http://cds1.discoveryftp.net'
#the login data is here
login_data = {
    'username': 'your username',#CHNAGE THIS WITH YOUR USERNAME
    'password': 'your password',#CHNAGE THIS WITH YOUR PASSWORD
    'remember': 'on',#DO NOT CHANGE THIS
    'loginsubmit': ''#DO NOT CHANGE THIS
}

#WARNING: DO NOT CHANGE THIS CONFIGURATION
#DO NOT TOUCH THIS CONFIGURATION

#the index headers is here
dflix_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }

#the search data is here
search_data = {
    'term' : '',
    'types' : ''
}

#the link extractor is here
preview_payload = {
    'dir' : '',
    'generateplaylist' : 'Playlist'
}


#end of config