import random

emojis = {'r': '🪨', 'p': '📄', 's': '✂️'}
choice = ("r", "p", "s")


def get_user_choice():
    while True:
        user_choice = input('Rock,Paper or Scissors? (r/p/s)-').lower()
        if user_choice in choice:
            return user_choice
        else:
            print('invalid choice!')


def display_choice(user_choice, computer_choice):
    print(f'Your Choice {emojis[user_choice]}')
    print(f'Computer Choice {emojis[computer_choice]}')


def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        print('tie!')
    elif (
        (user_choice == 'r' and computer_choice == 's') or
        (user_choice == 's' and computer_choice == 'p') or
            (user_choice == 'p' and computer_choice == 'r')):
        print('Your WIN!')
    else:
        print('Your LOSE!')


def play_game():
    while True:
        user_choice = get_user_choice()
        computer_choice = random.choice(choice)

        display_choice(user_choice, computer_choice)

        determine_winner(user_choice, computer_choice)

        should_Continue = input('continue? (y/n)').lower()
        if should_Continue == "n":
            break


play_game()
