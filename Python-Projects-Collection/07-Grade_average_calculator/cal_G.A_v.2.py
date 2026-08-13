
def calculation():
    count = 0
    Total = 0
    marks_list = []
    pas = str(input("Enter the password to continue:"))
    if len(pas) < 4:
        return "Password must be at least 4 characters long."
    elif 4 >= len(pas) <= 8:
        while True:
            marks = input("Enter marks ,if you want stop enter that key:")
            if marks == pas:
                if count == 0:
                    return "Nothing and program stopped.."
                else:
                    return f"Total grade entered:{count}\n Class Average:{Total/count:.2f}\n"
                    break
            try:
                choice = float(marks)
                if choice < 0:
                    return "enter positive number"
                    continue
                else:
                    marks_list.append(choice)
                    count += 1
                    Total += choice
            except ValueError:
                return "Invalid value."
    else:
        return "Password must be between 4 and 8 characters long."


print(calculation())
