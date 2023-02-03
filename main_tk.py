from tkinter import *
from tkinter import messagebox
import os
from lib import *
from time import sleep
import requests

with requests.Session() as session:
    session_main = session
    #this is the main session
logged_in = False
main_frame = None
frame_about = None
#for user login logout button and status
auth_state = True
#from user option
frame_option = None
#get the search result
search_result_frame = None
search_result_items = []
current_item = 0
#ui item show
item_show_list = []

def authentication(status):
    #status can be used as internal variable to check... this is just temporary
    global main_frame
    root = main_frame
    if status:
        auth = Toplevel(root)
        #auth.attributes("-topmost", True)
        auth.title("Login")
        auth.geometry("400x400")
        #auth.iconbitmap("tkinter test/img/ico.ico")
        auth.resizable(False,False)
        auth.config(bg="white")
        #new frame
        auth_frame = LabelFrame(auth, text="Login", width=400, height=400, bg="white", border=1, labelanchor=N)
        auth_frame.pack(fill="both", expand="yes", padx=10, pady=10)
        #variables
        username = StringVar()
        password = StringVar()

        user_name_entry = Entry(auth_frame, textvariable=username, width=20)
        user_name_label = Label(auth_frame, justify=LEFT, text="User Name : ", bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0)
        password_entry = Entry(auth_frame, textvariable=password, width=20, show="*")
        password_label = Label(auth_frame, justify=LEFT, text="Password : ", bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0)
        
        user_name_label.grid(row=0, column=0, pady=10, sticky=W, padx=20)
        user_name_entry.grid(row=0, column=1, pady=10, sticky=W, padx=10)
        password_label.grid(row=1, column=0, pady=10, sticky=W, padx=20)
        password_entry.grid(row=1, column=1, pady=10, sticky=W, padx=10)
        
        #has to confirm password and save as cookies
        #submit button
        submit_frame = LabelFrame(auth_frame, bg="white", border=0, width=400)
        submit_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=N, padx=120)
        submit_btn = Button(
            submit_frame, 
            text="SUBMIT", 
            width=20, height=2, bg="white", fg="black", 
            font=("Arial", 10, "bold"), relief=RAISED, border=0,
            command=lambda: submit_btn_cm(username.get(), password.get(), auth))
        submit_btn.pack()
    else:
        logout_conf = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if logout_conf:
            logout(session_main)
            messagebox.showinfo("Logout", "You have been logged out.")
            global auth_state,frame_option,logged_in
            frame_about.destroy()
            auth_state = True
            logged_in = False
            #os.remove("cookies.txt")
            frame_option.destroy()
            user_profile()
            user_options()

def user_confirmation(title :str, message :str, button :list, reply :StringVar):
    #this is a custom messagebox
    #it returns the button name
    #button is a list of button names
    #button = ["Yes","No","Save as text"]
    confirm = Toplevel()
    confirm.title(title)
    confirm.geometry("400x400")
    confirm.resizable(False,False)
    confirm.config(bg="white")
    #new frame
    confirm_frame = LabelFrame(confirm, text=title, width=400, height=400, bg="white", border=1, labelanchor=N)
    confirm_frame.pack(fill="both", expand="yes", padx=10, pady=10)
    #variables
    message_label = Label(confirm_frame, justify=LEFT, text=message, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0)
    message_label.pack(pady=10, padx=10)
    #submit button
    submit_frame = LabelFrame(confirm_frame, bg="white", border=0, width=400)
    submit_frame.pack(pady=10, padx=10)
    submit_btn = []
    for options in button:
        submit_btn.append(Button(
            submit_frame, 
            text=options, 
            width=20, height=2, bg="white", fg="black", 
            font=("Arial", 10, "bold"), relief=RAISED, border=0,
            command=lambda i=options: [reply.set(i),confirm.destroy()]))
        submit_btn[-1].pack(pady=10, padx=10)
    confirm.wait_window() #this is to make sure that the after window close the value of object is set.
    #this is made specially dry method -Tanvir Zaman

def link_crawler_get(item_name,item_url,type):
    global session_main
    #setting the url
    if type=="series":
        item_url+="/" #this is to make sure that the url is correct
    if type=="movies":
        movie_player = session_main.get(url = primary_url + item_url, headers = dflix_headers)
        movie_player_soup = BeautifulSoup(movie_player.text, "html.parser")
        item_url = movie_player_soup.find_all('td')[2].find('a')['href'] + "/"
    #getting the links as list
    result = link_crawler(session = session_main, select_url = item_url)
    
    #idmtabber = Toplevel()
    #idmtabber.title("Open In IDM")
    #idmtabber.geometry("400x400")

    #using info messagebox for now
    #user_reply = messagebox.askquestion(title="Open In IDM", message="Do you want to open this in IDM?",button=["Yes","No","Save as text"])
    user_reply = StringVar()
    user_confirmation(title="Open In IDM", message="Do you want to open this in IDM?",button=["Yes","No","Save as text"], reply=user_reply)
    if user_reply.get() == "Yes":
        for i in result:
            #open in idm or xdm
            reply = os.system("idman /n /d " + i)
            print(reply)
    elif user_reply.get() == "No":
        pass
    elif user_reply.get() == "Save as text":
        if os.path.exists(f'''Generated Links/{item_name}_{type}.txt'''):
            confirm = messagebox.askyesno("File Exists!", f'''The file already exists in "Generated Links" as {item_name}_{type}.txt\n do you want to overwrite it?''')
            if confirm:
                os.remove(f'''Generated Links/{item_name}_{type}.txt''')
                with open(f'''Generated Links/{item_name}_{type}.txt''', "a+") as links:
                    for link in result:
                        links.write(link + "\n")
                messagebox.showinfo("File Saved!", f'''The file has been saved in "Generated Links" as {item_name}_{type}.txt''')
            else:
                pass
        else:
            with open(f'''Generated Links/{item_name}_{type}.txt''', "a+") as links:
                for link in result:
                    links.write(link + "\n")
            messagebox.showinfo("File Saved!", f'''The file has been saved in "Generated Links" as {item_name}_{type}.txt''')
    else:
        pass

def submit_btn_cm(username, password,auth):
    global session_main,frame_about,auth_state,frame_option,logged_in
    if username != "" or password != "":
        session_main,status = login(session_main, username, password)
        if status==-1:
            messagebox.showinfo("Login", "Please Enter correct Username/Password.")
        elif status==0:
            messagebox.showinfo("Login", "Successfully Logged In.")
            frame_about.destroy()
            auth_state = False
            logged_in = True
            frame_option.destroy()
            user_profile()
            user_options()
            auth.destroy()
        '''
        elif status==1:
            auth.destroy()
            messagebox.showinfo("Already Logged In", "You are already logged in.")
        '''
    else:
        messagebox.showinfo("Login", "Please fill all the fields.")

def user_agreement(frame,status :str):
    if status=="begin":
        if os.path.exists("user_agreement.txt"):
            with open("user_agreement.txt", "r") as f:
                if f.read() == "yes":
                    f.close()
                    return
                else:
                    f.close()
                    os.remove("user_agreement.txt")
                    frame.destroy()
                    user_agreement_window(frame)
        else:
            user_agreement_window(frame)
    elif status=="yes":
        with open("user_agreement.txt", "w") as f:
            f.write("yes")
            f.close()
            frame.destroy()
    elif status=="no":
        frame.destroy()
        messagebox.showinfo("User Agreement", "You have to agree to the user agreement to use this software.")
        exit()

def user_agreement_window(root):
    agreement = Toplevel(root)
    agreement.title("User Agreement")
    agreement.geometry("400x400")
    #agreement.iconbitmap("tkinter test/img/ico.ico")
    agreement.resizable(False,False)
    agreement.config(bg="white")
    #new frame
    agreement_frame = LabelFrame(agreement, width=400, height=400, bg="white", border=0)
    agreement_frame.pack(fill="both", expand="yes", padx=10, pady=10)

    #the agreement
    rule_1 = Label(agreement_frame, text="1. The user is personally responsible to use this program.", bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, justify=LEFT)
    rule_1.grid(row=0, column=0, columnspan=2, sticky=W)
    rule_2 = Label(agreement_frame, text="2. This software has been created for learning purpose only.", bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0)
    rule_2.grid(row=1, column=0, columnspan=2, sticky=W)
    rule_3 = Label(agreement_frame, text="3. None of the files from the links are not stored by \n    the developer. This software just collects\n    the links from the server.", bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, justify=LEFT)
    rule_3.grid(row=2, column=0, columnspan=2,pady=5, sticky=W)
    rule_4 = Label(agreement_frame, text="4. This software is just a byproduct, learning tkinter for python.\n    Not for illigal use.", bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, justify=LEFT)
    rule_4.grid(row=3, column=0, columnspan=2, sticky=W)
    rule_5 = Label(agreement_frame, text="5.This script is not for commercial use.", bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0)
    rule_5.grid(row=4, column=0, columnspan=2, sticky=W)

    #create a yes no with user agreement question
    question = Label(agreement_frame, text="Do you agree to the user agreement?", bg="white", fg="black", font=("Arial", 14, "bold"), relief=RAISED, border=0)
    question.grid(row=6, column=0, columnspan=2,pady=10, sticky=W)
    #yes no buttons
    yes_no_frame = LabelFrame(agreement_frame, bg="white", border=0, width=400)
    yes_no_frame.grid(row=7, column=0, pady=10, sticky=N)
    yes_btn = Button(yes_no_frame, text="YES", width=20, height=1, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, command=lambda: user_agreement(agreement,status="yes"))
    yes_btn.grid(row=0, column=0, pady=10, padx=10, sticky=N)
    no_btn = Button(yes_no_frame, text="NO", width=20, height=1, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, command=lambda: user_agreement(agreement,status="no"))
    no_btn.grid(row=0, column=1, pady=10, padx=10, sticky=N)


def user_profile():
    global session_main,main_frame
    profile_info = ["Not Found!", "Not Found", "00000000000"]#this is sample this has to be removed and connected to the main program
    sessioned_profile_info = get_profile_info(session_main)
    if sessioned_profile_info != -1:
        profile_info = [sessioned_profile_info[0].text, sessioned_profile_info[1].text, sessioned_profile_info[2].text]
    bg_color = "white"
    #frame
    global frame_about
    frame_about = LabelFrame(
        main_frame, 
        text="User Profile", 
        width=500, 
        height=500, 
        bg=bg_color, 
        border=0, 
        labelanchor=N)
    frame_about.grid(row=0, column=0, sticky=N)
    #variables
    user_profile_info = f'''    ==============================   
                    [USER PROFILE]
    ============================== 
      
    User Name  : {profile_info[0]}
    User Email  : {profile_info[1]}
    User Phone : {profile_info[2]}
    ''' + (f"Please Login First!" if sessioned_profile_info == -1 else "")
    #variables
    user_inf = Label(
        frame_about, 
        bg=bg_color, 
        text=user_profile_info, 
        font=("Arial", 10, "bold"),
        relief=SUNKEN,
        anchor=W, 
        border=0,
        justify=LEFT,
        padx=10,
        pady=10)
    user_inf.grid(sticky=W)
def clear_data():
    #clear all the files in this directory
    reply = messagebox.askyesno("Clear Data", "Are you sure you want to clear all the links generated?")
    if reply:
        for file in os.listdir("Generated Links/"):
            if file.endswith(".txt"):
                f = "Generated Links/"+file
                os.remove(f)
        messagebox.showinfo("Clear Data", "All the generated links has been cleared!")

def user_options():
    global main_frame
    bg_color = "white"
    pady = 2

    global frame_option
    frame_option = LabelFrame(
    main_frame,
    text="Options", 
    width=500, 
    height=500, 
    bg=bg_color, 
    border=0, 
    labelanchor=N,
    padx=50)
    frame_option.grid(row=0, column=1, sticky=W,ipady=pady)
    
    global auth_state
    auth_text = "LOGIN" if auth_state else "LOGOUT"

    login_logout = Button(
        frame_option, 
        text=auth_text, 
        width=20, 
        height=2, 
        bg="white", 
        fg="black", 
        font=("Arial", 10, "bold"), 
        relief=RAISED, border=0, command=lambda: authentication(auth_state))
    login_logout.grid(row=0, column=0, sticky=W, pady=pady)
    
    clear_all = Button(frame_option, text="CLEAR ALL", width=20, height=2, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, command=lambda: clear_data())
    clear_all.grid(row=1, column=0, sticky=W, pady=pady)
    
    exit_program = Button(frame_option, text="EXIT", width=20, height=2, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0,command=exit)
    exit_program.grid(row=2, column=0, sticky=W, pady=pady)

def np_btn_cm(np_state):
    global current_item,search_result_items
    if len(search_result_items) == 0:
        messagebox.showwarning("Warning","No search result found!")
        return
    if np_state == "next" and current_item < len(search_result_items)-4:
        current_item = current_item + 4
        search_result_box(current_item)
    elif np_state == "previous" and current_item > 0:
        current_item = current_item - 4
        search_result_box(current_item)
    else:
        messagebox.showwarning("Warning","No more items!")

def search_result(search_term,options):
    global search_result_items,current_item,session_main,logged_in
    if options == "":
        messagebox.showwarning("Warning","Please select an option!")
    else:
        if logged_in == False:
            messagebox.showwarning("Warning","Please Login First!")
            return
        search_result_items = search(session_main,options,search_term)
        current_item = 0
        search_result_box(current_item)

def search_result_box(current_item):
    global search_result_frame,item_show_list,search_result_items
    bg_color = 'white'
    pady=5
    items = search_result_items
    for count in range(4): ##this is going to be a fixed list
        item_show_list[count-1][0].destroy()
        item_show_list[count-1][1].destroy()
        item_count=current_item+count
        if item_count >= len(items):
            label = Label(search_result_frame, text=f'''\n\n''', font=("Arial", 10, "bold"), bg=bg_color, justify=LEFT,width=50, anchor=W,wraplength=320)
            button = Button(search_result_frame, text="         ", width=10, height=1, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0)
            label.grid(row=count, column=0, sticky=W, pady=pady)
            button.grid(row=count, column=2, sticky=E, pady=pady)
        else:
            label = Label(search_result_frame, text=f'''{items[item_count][0]['count']}\n{items[item_count][1]['item_name']}\n''' + [x for x in f'''{items[item_count][1]['item_info']}'''.split('/')][0], font=("Arial", 10, "bold"), bg=bg_color, justify=LEFT,width=50, anchor=W,wraplength=320)
            button = Button(search_result_frame, text="GET LINKS", width=10, height=1, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, command=lambda temp=item_count: link_crawler_get(items[temp][1]['item_name'],items[temp][1]['item_url'],items[temp][2]['type']))
            label.grid(row=count, column=0, sticky=W, pady=pady)
            button.grid(row=count, column=2, sticky=E, pady=pady)
        item_show_list[count-1][0] = label
        item_show_list[count-1][1] = button

def search_frame():
    global main_frame
    bg_color = "white"
    pady = 5

    frame_search = LabelFrame(
    main_frame,
    text="Search", 
    width=540, 
    height=330, 
    bg=bg_color, 
    border=0, 
    labelanchor=N,
    padx=10,
    pady=10)
    frame_search.grid(row=1, column=0, columnspan=2,ipady=pady)

    #create a search bar
    search_q = StringVar()
    search_bar = Entry(frame_search,textvariable=search_q, width=52, border=0, font=("Arial", 10, "bold"))
    search_bar.grid(row=0, column=0, sticky=W)
    
    #option series of movies
    op_frame = LabelFrame(frame_search, bg=bg_color, border=0, width=100)
    op_frame.grid(row=1, column=0, columnspan=2, sticky=W, pady=pady)
    
    options = StringVar()
    
    option1 = Radiobutton(op_frame, text="Series", variable=options, value="series", bg=bg_color, font=("Arial", 10, "bold"))
    option2 = Radiobutton(op_frame, text="Movies", variable=options, value="movies", bg=bg_color, font=("Arial", 10, "bold"))
    option1.grid(row=0, column=0, sticky=W, ipadx=pady, ipady=pady, padx=pady)
    option2.grid(row=0, column=1, sticky=W, ipadx=pady, ipady=pady)

    #create a search button
    search_button = Button(frame_search, text="SEARCH", width=10, height=1, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, command=lambda: search_result(search_q.get(),options.get()))
    search_button.grid(row=0, column=1, sticky=W)

    #create next and previous button
    next_button = Button(op_frame, text="NEXT", width=10, height=1, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, command=lambda: np_btn_cm('next'))
    next_button.grid(row=0, column=2, pady=pady, padx=(90,10))
    prev_button = Button(op_frame, text="PREVIOUS", width=10, height=1, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0, command=lambda: np_btn_cm('previous'))
    prev_button.grid(row=0, column=3, pady=pady, padx=pady)

    #create a search result frame
    global search_result_frame
    search_result_frame = LabelFrame(
    frame_search,
    width=540,
    height=230,
    bg=bg_color,
    border=1,
    labelanchor=N,
    padx=10)
    search_result_frame.grid(row=2, column=0, columnspan=2, sticky=W)
    
    global item_show_list
    for count in range(4): ##this is going to be a fixed list
        label = Label(search_result_frame, text=f''' \n\n''', font=("Arial", 10, "bold"), bg=bg_color, justify=LEFT,width=50, anchor=W,wraplength=320)
        button = Button(search_result_frame, text="         ", width=10, height=1, bg="white", fg="black", font=("Arial", 10, "bold"), relief=RAISED, border=0)
        label.grid(row=count, column=0, sticky=W, pady=pady)
        button.grid(row=count, column=2, sticky=E, pady=pady)
        item_show_list.append([label,button])


def main_init():
    global session_main, auth_state, logged_in
    session_main, status = login(session_main, "","")
    if status==1:
        auth_state = False
        logged_in = True

def main():
    #starting the session and login
    main_init()

    #main window
    root = Tk()
    root.title("DFLIX LINK GENERATOR")
    root.geometry("600x650")
    root.resizable(False,False)
    #user agreement is must
    #
    user_agreement(root,status="begin")
    #
    bg_color = "white"
    #title section
    main_title = Label(root,bg=bg_color, text="DFLIX LINK GENERATOR", font=("Arial", 20, "bold"))
    main_title.pack(fill="both")
    #global
    global main_frame
    main_frame = LabelFrame(root, width=550, height=550, bg="white", border=0, padx=20, pady=10)
    main_frame.pack(fill="both", expand="yes")
    
    #user info section
    user_profile()
    #options selection section
    user_options()
    #search section
    search_frame()


    root.mainloop()
if __name__ == '__main__':
    main()