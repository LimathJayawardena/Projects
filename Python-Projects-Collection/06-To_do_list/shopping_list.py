my_list = []

while True:
    command = input("Add/View/Exit:").lower()
    if command == "add":
        new_item = input("Enter the new item:")
        my_list.append(new_item)
    elif command == "view":
        for item in my_list:
            print(item)
    elif command == "exit":
        print("Bye...!")
        break
    else:
        print("Invalid choice..!")
