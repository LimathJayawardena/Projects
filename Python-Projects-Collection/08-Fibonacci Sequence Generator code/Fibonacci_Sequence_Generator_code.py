def generate_fibonacci(limit):
    a, b = 0, 1
    sequence = []

    while a < limit:
        sequence.append(a)
        a, b = b, a + b

    return sequence


try:
    max_value = int(
        input("Enter the maximum value for the Fibonacci sequence: "))

    if max_value < 0:
        print("Please enter a non-negative number.")
    else:
        fib_sequence = generate_fibonacci(max_value)
        print(f"\n✨ Fibonacci Sequence (up to {max_value}):")
        print(', '.join(map(str, fib_sequence)))

except ValueError:
    print("Invalid input. Please enter a whole number.")
