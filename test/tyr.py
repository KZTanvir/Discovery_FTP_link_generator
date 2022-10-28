if dir['data-href'].startswith('/') and dir['data-href'].endswith('/'):
            real_url = cds2_url + dir['data-href']
            print(real_url)
        elif re.search('expires',dir['data-href']) :
            real_url_file = cds2_url + dir['data-href']
            print(real_url_file)