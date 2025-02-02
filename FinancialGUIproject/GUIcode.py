import tkinter
import hashlib #hashing passwords.
from tkinter import messagebox
#need to import image library
from PIL import Image, ImageTk # image and imageTk modules come from the same library Pillow
import os 
#import sqlite3 
from datetime import datetime  
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    
#set up gloabl variable 
expense_data = {} #global dictionary 

# need to create a file to store all the new and current user passwords and usernames. 
CREDENTIAL_FILE = 'credentials.txt'

#create a function to load user credentials from the file into a dictionary
def load_credentials():
    credentials = {} #empty dictionary. 
    #do a try block first time ever using it typicall use it to test a block of code for errors 
    try: 
        with open(CREDENTIAL_FILE, "r") as file: #we are attempting to open our file credentials and read each line. / this is how you open a file. 
            for line in file:
                username, hashed_password = line.strip().split(",")
                credentials[username] = hashed_password
    except FileNotFoundError: #this line what it does is that if file does not exist dont crash just continue execution
        pass # if the file does not exist, we start with an empty dictionary also pass means "do nothing" in Python. 
    return credentials #if nothing exists then credentials remains an empty dictionary because the file reading logic was skipped. 
    
    

# now we need a function to save a new user credential to the file. 
# going to open the file and then hash the password. 
def save_credential(username, password): 
    with open(CREDENTIAL_FILE, "a") as file: # note the "a" means add or append items into the file. 
        hashed_password = hashlib.sha256(password.encode()).hexdigest() #if you are wondeirng what this is its simply the SHA-256 hashing algorthm from python hasblib module to hash password securely. The password.encode
        #converts the plain-text password into bytes. and Hexdigest() converts the hashed value into a readable hexadecimal string
        file.write(f"{username},{hashed_password}\n") # this is used to write the username and then the hashed password into the file. 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#create a connection to SQLITE database 

#typically when in general I want to create a database I need these two lines to create or interact with SQLite database.

#create function to insert expenses into database. 
def save_expenses(entries, window): #passed a parameter entries to enter the expeves and save it to the data base we created called weekly expenses. 
    global expense_data  # Use the global dictionary
    today = datetime.now().strftime("%Y-%m-%d")  # Today's date

    for day, entry in entries.items():
        amount = entry.get()  # Get the amount entered for the day
        if amount.strip():  # Check if the user entered a valid amount
            # Add to expense_data
            if today not in expense_data:
                expense_data[today] = {}
            expense_data[today][day] = float(amount)

    # Close the "Insert Data" window and return to the dashboard
    window.destroy()

      
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#login button function.  
def login_button(): 
    username = login_entry.get() #username and password are created to get user input. 
    password = password_entry.get()  
    credentials = load_credentials()

    
    if (username in credentials and credentials[username] == hashlib.sha256(password.encode()).hexdigest()): #if statement checks if the entered username exists as a key in user_credentials and matches the entered password with the stored password for that username.
        #so what we are doing in the if statement is we check if the credentials which has the loaded credentails check to see if that username is already registered or not. 
        #the messagebox.showinfo just shows the user that the login was successful and leads them to the next page. 
        messagebox.showinfo("Login Successful!")
        
        #close login window 
        login_window.destroy() 
        
        #open dashboard onto this window. Here we called the function. 
        open_dash_window()
        
    else:
        #print("Invalid Username or Password") 
        messagebox.showinfo("Invalid Username or Password")
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#function for the dashboard page to represent the data. 
def open_dash_window():
    #creating a dashbaord page that gives options for user to select between keeping log of finances and saves that log viewing a graph of finances and gives a new financial tip everytime you press the button. From each button go into the differenent categories. 
    dash_window = tkinter.Tk() #the reason why we didnt use toplevel is because we are not going from a button to 
    dash_window.title('Dashboard Page') # set up dashboard page which will have its own background image. 
    dash_window.geometry('800x600') 
    
    load_background_image(dash_window) 

    #Now have to add Labels 
    text_widget = tkinter.Label( #text widget that displays some text about dashboard page. 
        dash_window,
        text="Welcome to Your Dashboard.\nHere you will have options to manage and view your finances!",
        wraplength = 600, 
        font = ("Times New Roman", 14),
        justify="center",
        fg = "white",
        bg = "black", 
    ) 
    
    #add a button to track users input of spending on a daily day to day bases on each day. 
    insert_expenses = tkinter.Button(
        dash_window, 
        text="Insert Expenses Data",
        padx = 12, 
        pady = 12,
        activebackground = "blue", 
        activeforeground = "black",
        fg = "white",
        bg = "black", 
        font = ("Times New Roman", 14), 
        command = lambda: insertexpenses,
        ) 
    

    view_expense_chart = tkinter.Button(
        text = "View Expense Graph", 
        padx = 12, 
        pady = 12,
        activebackground = "black", 
        activeforeground = "white",
        fg = "white",
        bg = "black", 
        font = ("Times New Roman", 14), 
        command = viewEchart,
    )
    
    Financeadvice_btn = tkinter.Button(
        text = "General Finance Advice", 
        padx = 12, 
        pady = 12, 
        activebackground = "black", 
        activeforeground = "white", 
        fg = "white", 
        bg = "black", 
        font = ("Times New Roman", 14), 
        command = Finance_advice, 
    ) 
    
    #Explanation of the following buttons as a text 
    explanation_of_buttons = tkinter.Label(
        text = "The three following buttons are used in 3 ways. The first button is used to insert data about your expenses. The second button is used to see the general illustration of your expenses through a graph, and finally the third is a summary of the data presented when you inputted your expenses. ", 
        wraplength = 600, 
        font = ("Times New Roman", 14),
        justify="center",
        fg = "white",
        bg = "black", 
    )
    
    
    # Configure columns for even spacing
    dash_window.columnconfigure(0, weight=1)  # Left-side column
    dash_window.columnconfigure(1, weight=1)  # Center column
    dash_window.columnconfigure(2, weight=1)  # Right-side column

    
    #Grid Labels of Buttons: 
    text_widget.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky = "nsew")  # Centered text
    
    insert_expenses.grid(row=1, column=0, padx = 20, pady=10, sticky="e")  # Left-aligned button

    view_expense_chart.grid(row = 1, column = 1, padx = 15, pady = 15, sticky = "w")

    Financeadvice_btn.grid(row = 1, column = 2, padx = 15, pady = 15, sticky = "w")  
    
    explanation_of_buttons.grid(row = 2, column = 0, columnspan = 3, padx = 20, pady = 20, sticky = "nsew")
    

#functions for the buttons and leading onto new screen.

#have to edit this and change 
def insertexpenses(): #will use sqlite for database to store user data and input and be able to retrieve data. so here youll def be learning some sql but remember stay on top of sql. 

    #create a new Toplevel window for inserting expenses. 
    insertdata_window = tkinter.Toplevel() # Toplevel is a widget that creates a new, seperate window that is associated with main root window (Tk)
    insertdata_window.title("Insert Data Window")
    insertdata_window.geometry('800x600') 
    
    #call the function and put the window we want to pass through it which in this case is the signup window 
    load_background_image(insertdata_window)  
    
    #add days of the week 
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    #number of entries made for each day: 
    entries = {}
    
    
    #create a title text to ask user to insert 
    title_label = tkinter.Label(insertdata_window,
        text = "Enter Your Expenses for Each Day",
        font = ("Times New Roman", 16), 
        bg = "black",
        fg = "white", 
    ) 
    
    for i, day in enumerate(days):
        label = tkinter.Label(
            insertdata_window,
            text=day,
            font=("Times New Roman", 14),
            bg="black",
            fg="white",
            anchor="w",
        )
        label.grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")

        entry = tkinter.Entry(insertdata_window, font=("Times New Roman", 14), justify="center")
        entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")
        entries[day] = entry

    save_Data_button = tkinter.Button(
        insertdata_window,
        text="Save Expenses",
        font=("Times New Roman", 14),
        bg="black",
        fg="white",
        command=lambda: save_expenses(entries, insertdata_window),
    )
    save_Data_button.grid(row=len(days) + 1, column=0, columnspan=2, pady=20)
    
    

#Button functions. 
def viewEchart(): #have to change and edit this.
     
    global expense_data 
    today = datetime.now().strftime("%Y-%m-%d")  # Today's date

    if today not in expense_data:
        tkinter.messagebox.showinfo("No Data", "No expenses recorded for today.")
        return

    data = expense_data[today]
    days = list(data.keys())
    amounts = list(data.values())

    # Plot the data
    plt.bar(days, amounts, color='skyblue')
    plt.title("Daily Expenses")
    plt.xlabel("Days of the Week")
    plt.ylabel("Amount Spent")
    plt.show()       

def Finance_advice(): 
    #this function is going to hold some financial advice if you need any. 
    #create window top level for this function in order to show and load background image. 
    
    FinanceAdvice_window = tkinter.Toplevel() #if we used the the tkinter.Tk() it was associated as a main root and for most of these we have it as toplevel windows. 
    FinanceAdvice_window.geometry('800x600') 
    FinanceAdvice_window.title("General Finance Advice") 
    
    load_background_image(FinanceAdvice_window) 
    
    #creating widgets as mostly texts and bullet points with the financial advice.  
    
    text_widget1 = tkinter.Label(
        FinanceAdvice_window,
        text = "When it comes to Finance its good to have knowledge about it to stay ahead. Here are a few tips and tricks to help you out when it comes to your finances !", 
        font = ("Times New Roman", 14),
        wraplength = 450,
        pady = 15,
        bg = "black",
        fg = "white",
    ) 
    
    text_widget2 = tkinter.Label(
        FinanceAdvice_window,
        text = "The first financial tip is to create a budget. With a budget you can track your income and expenses monthly to understand where your money goes and leaves. Tools like excel, budgeting apps, or financial software can help you!",
        wraplength = 450, #helps to reduce not making everything into one whole line.  
        font = ("Times New Roman", 14), 
        pady = 15, 
        bg = "black", 
        fg = "white", 
        ) 
    
    text_widget3 = tkinter.Label(
        FinanceAdvice_window, 
        text = "Build an Emergency Fund where you save 3 - 6 months worth of living expenses for emergencies, repairs, or in case you lose your job.", 
        wraplength = 450, 
        pady = 15,
        font = ('Times New ROman', 14),
        bg = "black", 
        fg = "white", 
    )
    
    text_widget3.pack()
    text_widget2.pack()
    text_widget1.pack() 


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#function to load_background_image 

def load_background_image(window):
    global photo # makes photo a global variable. so its accessible throughout the code and other functions.  
    image_path = os.path.join(os.getcwd(), "image.png")
    image = Image.open(image_path)
    image_resized = image.resize((800,600)) # we resize it to the geometry of the window screen. 
    photo = ImageTk.PhotoImage(image_resized) 
    
    #add image as a label
    label = tkinter.Label(window, image = photo)
    #image packing for the login window. 
    #image label to place background image on the login window. 
    label.place(x=0, y=0, relwidth=1, relheight=1)
    label.lower() #sends image label to the background 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def signup_button_click(): # this function will be responsible for the switch between windows from login to sign up. 
        
    signup_window = tkinter.Toplevel(login_window) # Toplevel is a widget that creates a new, seperate window that is associated with main root window (Tk)
    signup_window.title("Sign up Window")
    signup_window.geometry('800x600') 
    #signup_window.configure(bg = "black") 
    
    #call the function and put the window we want to pass through it which in this case is the signup window 
    load_background_image(signup_window) 
    
    tkinter.Label(
        signup_window,
        text = "If you don't have an account this page will help you Sign up!",
        font =("Times New Roman", 15), 
        fg = "white", # remember this is for the text color. 
        bg = "black", #background for the text. 
        ).pack(pady=30) # this is the vertical distance between the top and bottom. 
            
        #Label for registering for acc. 
    tkinter.Label(
        signup_window, 
        text = "Below please create a username and password", 
        font =("Times New Roman", 13), 
        fg = "white", # remember this is for the text color. 
        bg = "black",
        ).pack(pady=15) 
            
    tkinter.Label(
        signup_window,
        text="New Username",
        font=("Times New Roman", 13),
        fg="blue",
        bg="white"
        ).pack(pady=15)
    new_username_entry = tkinter.Entry(signup_window)
    new_username_entry.pack(pady=5)

    tkinter.Label(
        signup_window, 
        text = "New Password", 
        font = ("Times New Roman", 13),
        fg = "white",
        bg = "black",
        ).pack(pady=15)
    new_password_entry = tkinter.Entry(signup_window, show="*")
    new_password_entry.pack(pady=5)
    
def confirm_creds(): #Have another function to confirm credentials this is a button once user presses confirm 
    #we have to get the users data from the input 
    new_username = new_username_entry.get() # gets the username that is entered on the register page. 
    new_password = new_password_entry.get() 
        
    #here we load existing credentials
    existing_credentials = load_credentials() 
        
    #check for emptyness 
    if (new_username in existing_credentials == ""): 
        print("Error Empty input Please input valid username")
            
    elif (new_password in existing_credentials == ""): 
        print("Error Empty input Please input valid password")
        
    #we have to check if the new username is in the dictionary we created
    if new_username in existing_credentials:
        print("Username Exists already, Please choose another username")
    else:
        save_credential(new_username, new_password)
        print("Account Created Successfully")
        signup_window.destroy() # closes the signup window. 
        #is a seperate function keep an eye on the indentation.   
        # this function will retrieve the new pass and user and check if new user and new pass
        
        
    tkinter.Button(
        signup_window, 
        text = "Confirm new Username & Password", 
        padx = 12, 
        pady = 12, 
        relief = "ridge",
        fg = "white", 
        bg = "black",
        command=confirm_creds,
        ).pack(pady=15)
    
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Main Window aka the login window.
login_window = tkinter.Tk() # main window aka the login page window. 
login_window.title("Login and Sign up page")
login_window.geometry('800x600') 

load_background_image(login_window)

#read the background image
#image_path = os.path.join(os.getcwd(), "image.jpg")
#image = Image.open(image_path)
#image2 = image.resize((800,600)) # we resize it to the geometry of the window screen. 
#photo = ImageTk.PhotoImage(image2) 


#-----------------------------------------------------------------------------------------------------------------------------------------------------

# labels here which are basically the stuff we want to show on the screen. 
Title_label = tkinter.Label(
    login_window, 
    text="Welcome to Finance Manager", 
    pady = 10, #this adds the spacing between the wdigets
    padx = 10, #this adds spacing between the widgets. 
    font = ("Times New Roman", 25), #this is for the text itself like the font and size. 
    bg="black", #this is for the background of that text like the color. here we got it to match the  background white
    fg="White" #color of the text. 
) 

login_label = tkinter.Label(
    login_window, 
    text="Username:", 
    padx = 10, 
    pady = 10, #dont forget the commas
    font = ("Times new Roman", 15), 
    bg = "black",
    fg = "white",
    )
login_entry = tkinter.Entry(login_window) 


password_label = tkinter.Label(
    login_window, 
    text="Password:", 
    padx = 10, 
    pady = 10, 
    font = ("Times New Roman", 15),
    bg = "black", 
    fg = "white"
    )

password_entry = tkinter.Entry(login_window, show="*")  

#button
login_button = tkinter.Button(
    login_window, 
    text="Login", 
    padx = 12,
    pady = 12,
    fg = "white",
    bg = "black",
    command=login_button, 
    ) #the on_button_click is the function that will be executed when the button is clicked. 


#dont have an account to sign up button
signup_button = tkinter.Button(
    login_window, 
    text = "Dont have an Account?, Sign up today!", 
    relief = "ridge", 
    bd = 10, # border width. 
    fg = "white", #makes it look like a link 
    bg = "black",
    font = ("Times New Roman", 14, "italic", "underline"), 
    cursor ="hand2", # this changes the cursor to a hand. 
    command = signup_button_click, # dont forget this so button is called. 
)

#image label for login window. 
label = tkinter.Label(login_window, image = photo)
   
#image packing for the login window. 
#image label to place background image on the login window. 
label.place(x=0, y=0, relwidth=1, relheight=1)
label.lower() #sends image label to the background 



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
#Packing Labels below here note that packing is basically just pasting the widget onto the screen. 
Title_label.pack(pady=(110,10), anchor='center') # we use the anchor function to center for the widgets \ the (50,10) represents the amount of vertical padding above and below the widget. 
login_label.pack(pady = 5, anchor='center') 
login_entry.pack(pady = 5, anchor='center') 
password_label.pack(pady = 5, anchor='center') 
password_entry.pack(pady = 5, anchor='center') 
login_button.pack(pady = 20, anchor='center') #add 20 px of space between the entry and the button. We didnt put it on the label because it wont influence the other widgets only the internal layout of that widget.  
signup_button.pack(pady = 5, anchor ='center')


# window mainloop
login_window.mainloop() #first window 


