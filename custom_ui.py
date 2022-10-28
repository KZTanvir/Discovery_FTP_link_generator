import os
from time import sleep
def print_ui():
    print('''
            ==============================
            ****[DFLIX LINK GENERATOR]****
            ==============================
            1.RE-LOGIN
            2.GENERATE LINKS: SERIES
            3.GENERATE LINKS: MOVIES
            4.LOGOUT
            5.EXIT
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
            4. The user is personally responsible for using this script.
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

def items_list(items,search_type):
    for item in items:
        print(f'''
        {search_type} Item  : {item[0]['count']}
        {search_type} Name  : {item[1]['item_name']}
        {search_type} Info  : {item[1]['item_info']}
        ''')
        #the end of the item list
    return 0