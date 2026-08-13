import random
guess = random.randint(1, 100)

while True:
    try:
        number = int(input("Guess the number 1 to 100:"))

        if guess < number:
            print("Too High!")
        elif guess > number:
            print("Too Low!")
        else:
            print("congrats")
            break
    except ValueError:
        print("Enter valid number")
