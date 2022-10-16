#the config lies here

#the url of the dflix site is here
primary_url  = 'http://dflix.discoveryftp.net'
login_url    = primary_url + '/login/auth'
index_url    = primary_url + '/m'
profile_url  = primary_url + '/profile'
logout_url   = primary_url + '/login/destroy'
search_url   = primary_url + '/search'
cds2_url     = 'http://cds2.discoveryftp.net'
#the login data is here
login_data = {
    'username': 'HERE IS THE USERNAME',#CHNAGE THIS WITH YOUR USERNAME
    'password': 'HERE IS THE PASSWORD',#CHNAGE THIS WITH YOUR PASSWORD
    'remember': 'on',#DO NOT CHANGE THIS
    'loginsubmit': 'submit'#DO NOT CHANGE THIS
}

#WARNING: DO NOT CHANGE THIS CONFIGURATION
#DO NOT TOUCH THIS CONFIGURATION

#the index headers is here
dflix_headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
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