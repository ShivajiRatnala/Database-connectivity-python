import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Your Password',
        database='Your Database Name'
    )
    cursor = connection.cursor()
    account_no = input("Enter your Account number: ")

    if not account_no.isdigit() or len(account_no) != 16:
        print("Invalid Account number")
    else:
        # Access the data using parameterized queries to prevent SQL injection
        extract_user = "SELECT User_name, Account_balance, pincode FROM users_data WHERE Account_no = %s"
        cursor.execute(extract_user, (account_no,))
        
        # Fetch the data
        fetch_info = cursor.fetchone()

        # Check user 
        if fetch_info:
            user_name, current_amount, pincode = fetch_info
            print(f"Welcome {user_name}")

            print('1. Withdraw Amount', '2. Mini Statement', '3. Change PIN')

            select_option = int(input("Enter an option: "))

            if select_option == 1:
                print('Withdraw Amount')
                amount = int(input('Enter your amount: '))
                if amount > current_amount:
                    print("Insufficient Balance")
                else:
                    # User PIN verification to withdraw amount
                    while True:
                        pin = int(input('Enter your pin: '))

                        if pin == pincode:
                            update_amount = current_amount - amount
                            # Update query to remaining amount
                            update_query = 'UPDATE users_data SET Account_balance = %s WHERE Account_no = %s'
                            cursor.execute(update_query, (update_amount, account_no))
                            connection.commit()
                            print(f"Withdraw amount is {amount}")
                            print(f'Your Remaining account balance is {update_amount}')
                            break
                        else:
                            print('Invalid pin, check again')

            elif select_option == 2:
                print(f"User name is:{user_name} ")
                print(f"Your current balance is:{current_amount} ")
            else:
                previous_pin = int(input('Enter you pin: '))

                if previous_pin == pincode:
                    #Generating New pin Code
                    New_pin = input("Enter a New_Pin: ")

                    if not New_pin.isdigit() or len(New_pin) != 6:
                        print("The pin required Numbers and 6 digits only")
                    else:
                        update_pin = 'UPDATE users_data SET pincode = %s WHERE Account_no = %s'
                        cursor.execute(update_pin,(New_pin,account_no))
                        connection.commit()
                        print("Your pin is updated successfully")
                else:
                    print('Invalid pincode')                        
        else:
            print("Account not found.")
            
except mysql.connector.Error as error:
    print("Sorry! Server is not available. Error:", error)

finally:
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'connection' in locals() and connection.is_connected():
        connection.close()
