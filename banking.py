
no = int(input("How many times do you want to iterate the system?: "))
i = 0
balance = 0.0
while i < no:
    print('***************************************************')
    print('********************Welcome****************')
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Exit")
    choice = int(input("Enter any choice above: "))
   
    if choice == 1:
        deposit = float(input("Enter amount to deposit: "))
        if deposit < 0:
            print("Enter valid amount")
        else:
            print("Thanks for the deposit!")
            balance += deposit
    elif choice == 2:
        withdrawal = float(input("Enter amount to withdraw: "))
        if withdrawal < 0 or withdrawal > balance:
            print("Enter valid amount")
        else:
            balance -= withdrawal
            print("Thanks for withdawal!")
    elif choice == 3:
        print(f"Your balance is: {balance:.2f}")
    elif choice == 4:
        print("Goodbye")
        break
    else:
        print("Invalid choice")
    i+=1



