import random

hangman ={0:(" ",
        " ",
        " "),
     1:("0",
        " ",
        " "),
     2:("0",
        "|",
        " "),
     3:(" 0",
        "/|",
        " "),
     4:(" 0",
        "/|\\ ",
        " "),
     5:(" 0",
        "/|\\",
        "/"),
     6:(" 0",
        "/|\\",
        "/ \\")}
  

words=("boss","cat","orange")
    
    
def display_man(wrong):
    print("------------")
    for line in hangman[wrong]:
        print(line)
    print("------------")

def display_hint(hint):
    print(" ".join(hint))
            
def display_answer(answer):
    ...

def main():
    answer= random.choice(words)
    hint= ["_"]*len(answer)
    wrong=0
    guess=set()
    running=True

    while running:
        display_man(wrong)
        display_hint(hint)
        guess_word=input("Enter a letter:").lower()

        if len(guess_word) !=1 or not guess_word.isalpha():
            print("Invalid input!")
            continue
        
        if guess_word in guess:
            print(f"{guess_word} is already guessed")
            continue
        
        guess.add(guess_word)
        

        if guess_word in answer:
            for i in range(len(answer)):
                if answer[i]==guess_word:
                    hint[i]=guess_word
        else:
            wrong+=1


        if "_" not in hint:
            display_man(wrong)
            display_answer(answer)
            print("You win")
            running=False
        elif wrong >= len(hangman)-1:
            display_man(wrong)
            display_answer(answer)
            print("You loss")
            running=False
            

            
if __name__=="__main__":
    main()


    
