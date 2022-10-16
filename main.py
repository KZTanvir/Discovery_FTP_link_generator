from lib import *
from time import sleep
def main():
    with requests.Session() as session:
        print_ui()
        user_warning()
        session = login(session)
        sleep(2)
        clear()
    while True:
        get_profile_info(session)
        print_ui()
        choice = int(input("Enter your choice: "))
        if choice == 1:
            session = requests.Session()
            relogin(session)
        elif choice == 2:
            search_type = 'series'
            search_term = input("Enter any word to search: ")
            items = search(session,search_type,search_term)
            items_list(items)
            item_number = int(input("Enter the item number: "))
            download_list(session,items[item_number])
        elif choice == 3:
            search_type = 'movies'
            search_term = input("Enter any word to search: ")
            items = search(session,search_type,search_term)
            items_list(items)
            print('Search completed! Enter choice 4 to download!')
        elif choice == 4:
            try:
                item_number = int(input("Enter the item number: "))
                download_list(session,items[item_number])
                print('Download completed!Links generated in links.txt')
                clear()
            except:
                clear()
                print('Please select a item first.')
                print('Reason: logged out or no search results\n')
        elif choice == 5:
            logout(session)
            break
        elif choice == 6:
            print('The program exited successfully!')
            exit()
        else:
            print("Invalid choice")
            break
        #clear()
    return 0
main()