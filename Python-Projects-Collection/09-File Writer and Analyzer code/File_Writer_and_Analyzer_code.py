import os

FILE_NAME = "numbers.txt"

def write_numbers_to_file():
    print("--- Enter Numbers (Type 'done' when finished) ---")
    number_list = []
    
    while True:
        user_input = input("Enter a number: ").strip().lower()
        
        if user_input == 'done':
            break
        
        try:
            number = float(user_input)
            number_list.append(str(number))
        except ValueError:
            print("Invalid input. Please enter a valid number or 'done'.")
            
    try:
        with open(FILE_NAME, 'w') as file:
            file.write('\n'.join(number_list))
        print(f"\n✅ Successfully wrote {len(number_list)} numbers to '{FILE_NAME}'.")
    except IOError as e:
        print(f"❌ Error writing to file: {e}")


def read_and_analyze_file():
    if not os.path.exists(FILE_NAME):
        print(f"File '{FILE_NAME}' not found. Please run the writing function first.")
        return

    total_sum = 0
    count = 0
    
    try:
        with open(FILE_NAME, 'r') as file:
            for line in file:
                try:
                    number = float(line.strip())
                    total_sum += number
                    count += 1
                except ValueError:
                    continue 

        if count == 0:
            print("\nFile is empty or contains no valid numbers.")
            return

        average = total_sum / count

        print(f"\n📈 Analysis of '{FILE_NAME}':")
        print(f"Total Numbers Processed: {count}")
        print(f"Sum of Numbers: {total_sum:.2f}")
        print(f"Average: {average:.2f}")

    except IOError as e:
        print(f"❌ Error reading file: {e}")

if __name__ == "__main__":
    write_numbers_to_file()
    read_and_analyze_file()