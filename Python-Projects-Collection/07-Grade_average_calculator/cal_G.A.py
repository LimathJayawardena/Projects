def calculate_average(grades_list):
    if not grades_list:
        return 0.0

    total = sum(grades_list)
    count = len(grades_list)

    return total / count


def run_grade_calculator():
    grades = []
    print("Grade Average Calculator")
    print("Enter 'stop' at any time to calculate the average.")

    while True:
        user_input = input("Enter a grade: ").strip().lower()

        if user_input == 'stop':
            break

        try:
            grade = float(user_input)

            if grade < 0:
                print("Grades must be non-negative.")
                continue

            grades.append(grade)
            print(
                f"Added grade: {grade}. Current number of grades: {len(grades)}")

        except ValueError:
            print("Invalid input. Please enter a number or 'stop'.")

    final_avg = calculate_average(grades)

    if final_avg > 0:
        print("\n--- RESULTS ---")
        print(f"Total Grades Entered: {len(grades)}")
        print(f"Calculated Average: {final_avg:.2f}")
        print("---------------")
    else:
        print("\nNo valid grades were entered.")


run_grade_calculator()
