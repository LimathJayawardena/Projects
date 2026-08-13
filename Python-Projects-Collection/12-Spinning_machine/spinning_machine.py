import random as r


def spining():
    global r1, r2, r3
    # Renamed 'list' to 'symbols' because 'list' is a keyword in Python
    symbols = ['🥭', '🍎', '⭐', '🍍']
    r1 = r.choice(symbols)
    r2 = r.choice(symbols)
    r3 = r.choice(symbols)
    return f"{r1}|{r2}|{r3}"


def main():
    global wallet, bet
    wallet = int(input("Enter Wallet Amount:Rs."))
    while wallet > 0:
        try:
            bet = int(input(f"Current Wallet: {wallet}. Enter Your Bet:Rs."))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if bet > wallet:
            print("You don't have enough money for that bet!")
            continue

        print("Result!")
        print(spining())

        if r1 == r2 == r3:
            pay = (wallet - bet) + (bet * 5)
            print(f"YOU WON TRIPLE! Balance: {pay}")
            wallet = pay
        elif r1 == r2 or r2 == r3 or r1 == r3:
            pay = (wallet - bet) + (bet * 2)
            print(f"YOU WON DOUBLE! Balance: {pay}")
            wallet = pay
        else:
            pay = (wallet - bet)
            print(f"You Lost! Balance: {pay}")
            wallet = pay

    print("Game Over! Your wallet is empty.")


if __name__ == "__main__":
    main()
