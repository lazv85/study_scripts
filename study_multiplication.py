import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def multiplication_test(number, wrong_answers):
    while wrong_answers:
        factor = random.randint(2, 9)
        while (number, factor) not in wrong_answers:            
            factor = random.randint(2, 9)

        input(f"press any key. ")
        clear_screen()

        # Get user input
        user_answer = input(f"What is {number} x {factor} = ? ")
        # Check if the input is a valid number
        if not user_answer.isdigit():
            print("Please enter a valid number.")
            continue

        # Convert the user's answer to an integer
        user_answer = int(user_answer)

        # Check the user's answer
        if user_answer == number * factor:
            print("Correct! Well done.")
            wrong_answers.remove((number, factor))
        else:
            print(f"Wrong answer. It is {number*factor}")

if __name__ == "__main__":
    # Get user input as a number from 1 to 9
    while True:
        user_input = input("Enter a number from 2 to 9: ")

        # Check if the input is a valid number
        if user_input.isdigit() and 2 <= int(user_input) <= 9:
            chosen_number = int(user_input)
            break
        else:
            print("Please enter a valid number from 1 to 9.")

    # Set to store wrong answers for future reference
    wrong_answers = {(chosen_number, factor) for factor in range(2, 10)}

    # Start the multiplication test
    multiplication_test(chosen_number, wrong_answers)
    