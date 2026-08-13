import random
import string


def generator():
    print('Password Generator')
    try:
        num = int(input('Enter the length of the password(min-5):-'))
    except:
        print('Syntax Error...!\nEnter whole number:-')

    all_chars = string.ascii_letters+string.digits+string.punctuation

    if num <= 4:
        print('Length too short!')
        return

    password_list = []

    for _ in range(num):
        password_list.append(random.choice(all_chars))

    random.shuffle(password_list)

    password = "".join(password_list)

    print(f'Your password is {password}')


logo()
generator()
