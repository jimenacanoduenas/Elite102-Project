import mysql.connector
connection = mysql.connector.connect(user = 'root', database = 'Elite102-Project', password = 'password')
curr_email = "" # keeps track of current users email (unique to each user)

# CLI functions
def login_screen(): # Used for logging in to an existing account
    curr_email = ""
    print("~~~~~~~~~~~~~~~~~~~~~~~ Login ~~~~~~~~~~~~~~~~~~~~~~~~")
    email_input = input("Email: ")
    # Check that account exists
    if(check_email(email_input) == -1):
        print("Account does not exist.")
        print("1. Try again")
        print("2. Create new account")
        user_input = input("")
        if (user_input == "2"):
            return (2, curr_email)
        elif (user_input != "1"):
            print("Invalid input.")
        return (0, curr_email)
    else:
        # Ask for account password
        curr_email = email_input
        pass_input = input("Password: ")
        if (pass_input == check_password(email_input)):
            print("Login successful! Welcome " + check_name(email_input) + "!") 
            return (1, curr_email)
        else:
            print("Wrong password.")
            print("1. Try again")
            print("2. Create new account")
            user_input = input("")
            if (user_input == "2"):
                return (2, curr_email)
            elif (user_input != "1"):
                print("Invalid input.")
            return (0, curr_email) 
def create_account_screen(): # Used for creating a new account
    curr_email = ""
    print("~~~~~~~~~~~~~~~~~~~ Create Account ~~~~~~~~~~~~~~~~~~~~")
    email_input = input("Email: ")
    # Check that account does not already exist
    if(check_email(email_input) == 0):
        print("Account already exists.")
        print("1. Try again")
        print("2. Login")
        user_input = input("")
        if (user_input == "2"):
            return (2, curr_email)
        elif (user_input != "1"):
            print("Invalid input.")
        return (0, curr_email)
    # Ask for remaining account information
    else:
        curr_email = email_input
        pass_input = input("Password: ")
        name_input = input("Name: ")
        create_account(email_input, pass_input, name_input)
        print("Welcome to C2C Bank, " + name_input + "!")
        return (1, curr_email)
def account_screen(email): # Used for primary account functions
    acc_email = email
    print("~~~~~~~~~~~~~~~~~~ Account Options ~~~~~~~~~~~~~~~~~~")
    print("1. Check balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Wire transfer to another account")
    print("5. Update account details")
    print("6. Delete account")
    print("7. Logout")
    user_input = input("")
    if (user_input == "1"):
        print("Current balance is " + str(check_balance(acc_email)) + ".")
        return (True, acc_email)
    elif (user_input == "2"):
        print("How much would you like to deposit?")
        deposit_input = int(input(""))
        deposit(acc_email, deposit_input)
        return (True, acc_email)
    elif (user_input == "3"):
        print("How much would you like to withdraw?")
        withdraw_input = int(input(""))
        withdraw(acc_email, withdraw_input)
        return (True, acc_email)
    elif (user_input == "4"):
        print("Which account would you like to transfer to?")
        receive_email = input("Email: ")
        if (check_email(receive_email) == -1):
            print("Account does not exist.")
        elif (receive_email == acc_email):
            print("Cannot wire to yourself.")
        else:
            print("How much would you like to transfer?")
            wire_amount = int(input(""))
            wire(acc_email, receive_email, wire_amount)
        return (True, acc_email)    
    elif (user_input == "5"):
        print("What would you like to update?")
        print("1. Email")
        print("2. Name")
        print("3. Password")
        print("4. Return")
        update_input = input("")
        if (update_input == "1"):
            print("Current email: " + acc_email)
            new_email = input("New email: ")
            acc_email = update_email(acc_email, new_email)
        elif (update_input == "2"):
            print("Current name: " + check_name(acc_email))
            new_name = input("New name: ")
            update_name(acc_email, new_name)
        elif (update_input == "3"):
            new_password = input("New password: ")
            update_password(acc_email, new_password)
        elif (update_input == "4"):
            print("Account details unchanged.")
        else:
            print("Invalid input.")
        return (True, acc_email)
    elif(user_input == "6"):
        print("Are you sure you would like to delete your account?")
        print("1. Yes")
        print("2. No")
        delete_input = input("")
        if (delete_input == "1"):
            delete_account(acc_email)
            print("Account associated with email " + acc_email + " deleted.")
            return (False, acc_email)
        elif (delete_input == "2"):
            print("Account was not deleted.")
            return (True, acc_email)
        else:
            print("Invalid input.")
            return (True, acc_email)
    elif(user_input == "7"):
        print("Logout successful.")
        return (False, acc_email)

# Account information functions
def check_balance(email): # Returns account balance given email
   query = ("SELECT balance FROM accounts WHERE email = '" + email + "'")
   cursor = connection.cursor()
   cursor.execute(query)
   for bal in cursor:
       balance = bal[0]
   cursor.close()
   return balance
def check_password(email): # Returns password given email
    query = ("SELECT password FROM accounts WHERE email = '" + email + "'")
    cursor = connection.cursor()
    cursor.execute(query)
    for passw in cursor:
        password = passw[0]
    return password
def check_email(email): # Returns whether an account exists given email
    query = ("SELECT account_id FROM accounts WHERE email = '" + email + "'")
    cursor = connection.cursor()
    cursor.execute(query)
    account = cursor.fetchone()
    if (account == None):
        # account does not exist
        return -1
    else:
        # account exists
        return 0
def check_name(email): # Returns account name given email
    query = ("SELECT name FROM accounts WHERE email = '" + email + "'")
    cursor = connection.cursor()
    cursor.execute(query)
    for username in cursor:
       name = username[0]
    cursor.close()
    return name
def check_id(email): # Returns account id given email
    query = ("SELECT account_id FROM accounts WHERE email = '" + email + "'")
    cursor = connection.cursor()
    cursor.execute(query)
    for account_id in cursor:
       id = account_id[0]
    cursor.close()
    return id

# Update account information functions
def update_email(old_email, new_email): # Updates account email
    if (check_email(new_email) == 0):
        print("Account already exists with that email.")
        return old_email
    else:
        query = ("UPDATE accounts SET email = '" + new_email + "' WHERE email = '" + old_email + "'")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Email change succesful.")
        return new_email
def update_name(email, new_name): # Updates account name given email
    query = ("UPDATE accounts SET name = '" + new_name + "' WHERE email = '" + email + "'")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("Name change succesful.")   
def update_password(email, new_pass): # Updates account password given email
    query = ("UPDATE accounts SET password = '" + new_pass + "' WHERE email = '" + email + "'")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("Password change succesful.")
def delete_account(email): # Deletes account given email
    query = ("DELETE FROM accounts WHERE email = '" + email + "'")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
def create_account(email, passw, name): # Creates new account given account information
    query = ("INSERT INTO accounts (ACCOUNT_TYPE, NAME, EMAIL, PASSWORD, BALANCE) VALUES ('0', '" + name + "', '" + email + "', '" + passw + "', '0')")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
def withdraw(email, amount): # Withdraws balance given email
    balance = check_balance(email)
    # check that amount is valid
    if (amount <= 0):
        print("Invalid withdrawal amount.")
    # check that balance is enough
    elif (balance < amount):
        print("Insufficent funds.")
    else:
        balance = balance - amount
        # update balance
        query = ("UPDATE accounts SET balance = " + str(balance) + " WHERE email = '" + email + "'")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        # log transaction in database
        query = ("INSERT INTO transactions (ACCOUNT_ID, TYPE, AMOUNT) VALUES ('" + str(check_id(email)) + "', 'WITHDRAW', '" + str(amount) + "')")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Withdrawal succesful, remaining balance is " + str(balance) + ".")
def deposit(email, amount): # Deposits balance given email
    # check that amount is valid
    if (amount <= 0):
        print("Invalid deposit amount.")
    else:
        # update balance
        balance = check_balance(email) + amount
        query = ("UPDATE accounts SET balance = " + str(balance) + " WHERE email = '" + email + "'")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        # log transaction in database
        query = ("INSERT INTO transactions (ACCOUNT_ID, TYPE, AMOUNT) VALUES ('" + str(check_id(email)) + "', 'DEPOSIT', '" + str(amount) + "')")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Deposit succesful, updated balance is " + str(balance) + ".")
def wire(sender_email, receiver_email, amount):
    balance = check_balance(sender_email)
    # check amount is valid
    if (amount <= 0):
        print("Invalid wire amount.")
    # check that balance is enough
    elif (balance < amount):
        print("Insufficent funds.")
    else:
        balance = balance - amount
        # update balance of sender
        query = ("UPDATE accounts SET balance = " + str(balance) + " WHERE email = '" + sender_email + "'")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        # update balance of receiver
        receiver_balance = check_balance(receiver_email) + amount
        query = ("UPDATE accounts SET balance = " + str(receiver_balance) + " WHERE email = '" + receiver_email + "'")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        # log transaction in database
        query = ("INSERT INTO transactions (ACCOUNT_ID, TYPE, AMOUNT) VALUES ('" + str(check_id(sender_email)) + "', 'WIRE OUT', '" + str(amount) + "')")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        query = ("INSERT INTO transactions (ACCOUNT_ID, TYPE, AMOUNT) VALUES ('" + str(check_id(receiver_email)) + "', 'WIRE IN', '" + str(amount) + "')")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Wire transfer successful, remaining balance is " + str(balance) + ".")
    


# Main program loop
while(True):
    # CLI works by prompting user with menu of options
    print("~~~~~~~~~~~~~~~~ Welcome to C2C Bank! ~~~~~~~~~~~~~~~~")
    print("Please select an option by responding with its number.") 
    print("1. Login")
    print("2. Create new account")
    user_input = input("")
    while (user_input != "1" and user_input !="2"):
        print("Invalid input.")
        print("~~~~~~~~~~~~~~~~ Welcome to C2C Bank! ~~~~~~~~~~~~~~~~")
        print("Please select an option by responding with its number.") 
        print("1. Login")
        print("2. Create new account")
        user_input = input("")
    login_success = False
    login_create = user_input
    # Keep looping to login/create account screens until user is able to log in
    # Return current email along with logged in status so the user account is kept track of
    while (not login_success):
        if (login_create == "1"):
            login_result = login_screen()
            if(login_result[0] == 0):
                login_success = False
            elif(login_result[0] == 1):
                login_success = True
                curr_email = login_result[1]
            else:
                login_create = "2"
        if (login_create == "2"):
            create_result = create_account_screen()
            if(create_result[0] == 0):
                login_success = False
            elif(create_result[0] == 1):
                login_success = True
                curr_email = create_result[1]
            else:
                login_create = "1"

    # While logged in, loop account screen until user logs out or deletes account
    logged_in = True
    while(logged_in):
        # Return current email along with logged in status in case email is updated within account screen
        account_status = account_screen(curr_email)
        logged_in = account_status[0]
        curr_email = account_status[1]   