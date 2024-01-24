import sys
import random
import os
import argparse

num_wrong_answers = 5

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def randon_excl(set, n):
    t = -1
    while t == -1:
        m = random.randint(0, n-1)
        if not (m in set):
            t = m
    return t

def read_file(file_path):
    try:
        my_hashmap = {}
        with open(file_path, 'r') as file:
            for line in file.readlines():
                result = line.strip().split("-")
                key = result[0].strip()
                value = result[1].strip()
                my_hashmap[key] = value
            return my_hashmap
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

def words(dict):
    arr = []
    for k in dict.keys():
        arr.append(k)
    return arr 

def build_questions(used_words, stat, dict):    
    l = len(used_words)
    comb = {}
    for index, element in enumerate(used_words):
        if (stat[element]["tried"] < 4 or
            (stat[element]["correct_answer"]-1)*0.4 < stat[element]["wrong_answer"]):
            resp = []
            resp.append([dict[element], "y"])
            used = {index}
            for i in range(num_wrong_answers):
                t = randon_excl(used, l)
                used.add(t)
                resp.append([dict[used_words[t]], "n"])
            random.shuffle(resp)
            comb[element] = resp
    return comb

def ask_question(key, dict, stat, questions):
    stat[key]["tried"] = stat[key]["tried"] + 1
    print(key)
    print()
    resp = questions[key]
    for i in range(num_wrong_answers + 1):
        print (f"{i} - {resp[i][0]}")
        print()
    
    print("99 - to stop program")

    answer = -1
    while answer == -1:
        ans = input(f"enter the number of answer: ")
        if is_numeric(ans):
            answer = int(ans)
        else:
            print("incorrect input, try again")

    if answer == 99:
        return "q"
    
    if resp[answer][1] == "y":
        stat[key]["correct_answer"] = stat[key]["correct_answer"] + 1
        print("correct answer")        
        return "y"
    else:
        stat[key]["wrong_answer"] = stat[key]["wrong_answer"] + 1
        print("wrong answer")
        print()
        print(f"correct answer is {key} - {dict[key]}")
        return "n"
    
def test(used_words, dict, stat, questions):
    while questions:
        m = random.randint(0, len(used_words)-1)
        key = used_words[m]       
        if key in questions:
            input(f"press any key. ")
            clear_screen()
            question_to_go = len(questions)
            print(f"{question_to_go} question to go")
            print()
            resp = ask_question(key, dict, stat, questions)
            if resp == "q":
                return
            if resp == "y":
                questions.pop(key)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process directory and file arguments.')
    
    # Define the command line arguments
    parser.add_argument('-d', '--directory', help='Specify the directory path.')
    parser.add_argument('-f', '--filename', help='Specify the file name.')
    parser.add_argument('-s', '--stat', help='Specify the file name with word statistics.')

    args = parser.parse_args()

    try:
        ret = {}
        ret["dir"] = args.directory
        ret["file"] = args.filename
        if args.stat is None:
            ret["stat"] = ret["file"] + "_stat"
        else:
            ret["stat"] = args.stat
        return ret
    except Exception:
        print("Usage: study_words.py -d <dir> -f <input_file>")
        return {}

def build_words_stat(used_words, stat):
    for w in used_words:
        if not (w in stat):
            stat[w] = {}
            stat[w]["tried"] = 0
            stat[w]["wrong_answer"] = 0
            stat[w]["correct_answer"] = 0
    return stat

def read_words_stat(file_path):
    try:
        my_hashmap = {}
        with open(file_path, 'r') as file:
            for line in file.readlines():
                result = line.strip().split(":")
                w_stat_arr = result[1].strip().split(",")
                w_stat_map = {}
                w_stat_map["tried"] = int(w_stat_arr[0])
                w_stat_map["correct_answer"] = int(w_stat_arr[1])
                w_stat_map["wrong_answer"] = int(w_stat_arr[2])
                my_hashmap[result[0]] = w_stat_map
        return my_hashmap
    except FileNotFoundError:
        print(f"No stat file found: '{file_path}'")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def write_words_stat(stat, file_path):
    with open(file_path, 'w') as file:
        for s in stat.keys():
            line = s + ":" + str(stat[s]["tried"]) + "," + str(stat[s]["correct_answer"]) + "," + str(stat[s]["wrong_answer"])
            file.write(line)
            file.write('\n')
def main():
   args = parse_arguments()
   if not args:
       return
    # Check if the script is provided with the file path as a command-line argument
   file_path = args["dir"] + "/" + args["file"]
   stat_path = args["dir"] + "/" + args["stat"]   

   dict = read_file(file_path)
   stat = read_words_stat(stat_path)   
   used_words = words(dict)
   stat = build_words_stat(used_words, stat)
   questions = build_questions(used_words, stat, dict)
   test(used_words, dict, stat, questions)
   write_words_stat(stat, stat_path)

if __name__ == "__main__":
    main()
        