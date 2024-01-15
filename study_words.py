import sys
import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_file(file_path):
    try:
        my_hashmap = {}
        with open(file_path, 'r') as file:
            for line in file.readlines():
                result = line.strip().split("-")                
                my_hashmap[result[0]] = result[1]
            return my_hashmap
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

def build_questions(dict):
    arr = []
    for k in dict.keys():
        arr.append(k)
    l = len(arr)
    comb = []
    for k in dict.keys():
        t = -1
        while t == -1:
            m = random.randint(0, l-1)
            if arr[m] != k:
                t = m
        comb.append([k, dict[k], "y"])
        comb.append([k, dict[arr[t]], "n"])
    return comb

def test(questions):
    while questions:
        input(f"press any key. ")
        clear_screen()
        m = random.randint(0, len(questions)-1)
        answer = input(f"Is it correct [y/n]: {questions[m][0]} - {questions[m][1]}: ")
        if answer == questions[m][2]:
            print("It is right answer.")
            questions.pop(m)
        else:
            print("It is wrong answer.")

if __name__ == "__main__":
    # Check if the script is provided with the file path as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        questions = build_questions(read_file(file_path))
        test(questions)