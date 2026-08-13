choice = input("Enter Your data type is faranheit or Celsius(F/C)?").lower()
if choice == 'c':
    temp = int(input("Enter the temperature in Celsius: "))
    tot = (temp*9/5)+32
    print(f"{tot:.2f}'F")
elif choice == 'f':
    temp = int(input("Enter the temperature in Faranhiet: "))
    tot = (temp-32)*5/9
    print(f"{tot:.2f}'C")
else:
    print("Invalid Input")
