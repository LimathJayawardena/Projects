import random as r


def word():
    print("----Encryptor & Decryptor----")

    mode = input("Type '1' to Encrypt or '2' to Decrypt: ")

    user_word = input("Enter word: ")
    user_shift = int(
        input("Enter how many letters need to shift(only 1 to 26): "))

    if mode == '2':
        user_shift = -user_shift

    new_user_word = ''

    for letter in user_word:
        if letter == " ":
            new_user_word += " "
        elif letter.isupper():
            start = ord("A")
            new_user_word += chr(((ord(letter)-start+user_shift) % 26)+start)
        elif letter.islower():
            start = ord("a")
            new_user_word += chr(((ord(letter)-start+user_shift) % 26)+start)
        else:
            new_user_word += letter

    print("Result: " + new_user_word)


def quiz():
    words = ['digit', 'cipher', 'python']
    word = r.choice(words)
    shift = r.randint(1, 3)
    start = ord("a")
    points = 0
    round = 1

    while round < 11:
        new_word = ""
        print("----Quiz----")
        print(f"Current Round:{round}")
        round += 1
        for letter in word:
            new_word += chr(((ord(letter)-start+shift) % 26)+start)
        print(new_word)

        user = int(input("Enter how many shift?"))
        if user == shift:
            points += 1
            print(f"+1 point.Your points={points}")
        else:
            print(f"no.of shifts={shift}")

        word = r.choice(words)
        shift = r.randint(1, 3)


print("-----Caesar Cipher Tool-----")


while True:
    print()
    choice = int(input(
        "What Service do you want?\n 1.Letter Shifter(Encrypt or Decrypt)\n 2.Quiz\n Enter-->"))

    if choice == 1:
        print()
        word()
    elif choice == 2:
        print()
        quiz()
    else:
        print("Error 1 or 2!")

    print()
    again = input(
        "Do you want to continue? (type 'stop' to exit, or 'anything' else to continue): ")
    if again.lower() == "stop":
        break
