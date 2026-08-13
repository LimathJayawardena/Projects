def show_balance():
    return f"""
        +---------ABC bank Receipt---------+
        Current Balance:Rs.{c_balance}
        """


def deposit():
    d_amount = float(input("Enter the Deposit Amount:Rs."))
    return f"""
        +---------ABC bank Receipt---------+
                  Deposit Success!
        Deposit Amount:Rs.{d_amount}
        Current Balance:Rs.{c_balance+d_amount}
        +----------------------------------+
        """


def withdraw():
    print( f"""
        +---------ABC bank Receipt---------+
        Current Balance:Rs.{c_balance:.2f}""")
    w_amount = float(input("Enter the Withdrawal Amount:Rs."))
    if c_balance-w_amount <= 0:
        return f"""
        +---------ABC bank Receipt---------+
                INSUFFICIENT BALANCE!
        Current Balance:Rs.{c_balance:.2f}
        +----------------------------------+
           """
    else:
        return f"""
        +---------ABC bank Receipt---------+
                Withdrawal Success!
        Withdrawal Amount:Rs.{w_amount:.2f}
        Current Balance:Rs.{c_balance-w_amount:.2f}
        +----------------------------------+
        """


def main():
    global c_balance
    print("+-------WELCOME TO ABC BANK-------+")
    c_balance = float(input("Enter the Current balance:Rs."))
    while True:
        choice = int(input(
            'Services:\n1.Show Balance\n2.Deposit\n3.Withdrawal\n4.Quit\nEnter your choice: '))
        if choice == 1:
            print(show_balance())
        if choice == 2:
            print(deposit())
        if choice == 3:
            print(withdraw())
        if choice == 4:
            break


if __name__ == '__main__':
    main()
