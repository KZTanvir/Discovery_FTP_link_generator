from lib import *
from time import sleep
from custom_ui import *
import requests
def main():
    with requests.Session() as session:
        print_ui()
        user_warning()
        session = login(session)
        sleep(1)
        clear()
    while True:
        get_profile_info(session)
        print_ui()
        try:
            choice = int(input("Enter your choice: "))
        except:
            print("INVALID CHOICE!")
            sleep(1)
            clear()
            print("Returning to the main menu!")
            sleep(1)
            clear()
            continue
        if choice == 1:#re-login
            relogin(session)
        elif choice == 2:#generate links: series
            search_type = 'series'
            search_term = input("Enter any word to search: ")
            items = search(session,search_type,search_term)
            items_list(items = items, search_type = search_type)
            selection = int(input('Enter the item count to generate links:'))
            print('\n\n')
            crawled_links = link_crawler(session = session, select_url = items[selection][1]['item_url'] + '/')
            item_name = items[selection][1]['item_name']
            for links in crawled_links:
                with open(f'''GeneratedLinks/{item_name}_links.txt''','a+') as file:
                    file.write(links + '\n')
                    file.close()
            print(f'Links generated for {item_name}')
            print('Saved to GeneratedLinks folder.')
            sleep(1)
            clear()
        elif choice == 3:#generate links: movies
            search_type = 'movies'
            search_term = input("Enter any word to search: ")
            items = search(session,search_type,search_term)
            items_list(items,search_type)
            selection = int(input('Enter the item count to generate links:'))
            print('\n\n')
            movie_player = session.get(url = primary_url + items[selection][1]['item_url'], headers = dflix_headers)
            movie_player_soup = BeautifulSoup(movie_player.text, "html.parser")
            item_name = items[selection][1]['item_name']
            with open(f'''GeneratedLinks/{item_name}_links.txt''','a+') as file:
                file.write(movie_player_soup.find('source')['src'] + '\n')
                file.close()
            print(f'Links generated for {item_name}')
            print('Saved to GeneratedLinks folder.')
            sleep(1)
            clear()
        elif choice == 4:
            logout(session)
            continue
        elif choice == 5:
            clear()
            print("Exiting...")
            sleep(1)
            print('The program exited successfully!')
            break
    return 0
if __name__ == '__main__':
    main()