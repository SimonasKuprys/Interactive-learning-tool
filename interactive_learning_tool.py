import csv
import random
from tabulate import tabulate
import datetime

#Button object changes active state of value to True or False
class Button:
    def __init__(self, number):
        self.info = Reader.read_file()
        self._number = number

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, new_number):
        self._number = new_number

    def __str__(self):
        return f"What {self.number} {self.info}"

    def change_status(self):
        for row in self.info:
            if self.number == int(row["id"]):
                if row["active"] == "True":
                    row["active"] = "False"
                else:
                    row["active"] = "True"

        with open("quiz.csv", "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row)
            writer.writeheader()
            for row in self.info:
                writer.writerow(row)
#Reads all rows in file
class Reader:
    @classmethod
    def read_file(self):
        try:
            all_info = []
            with open("quiz.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    all_info.append(row)
            self.info = all_info
            return all_info
        except:
            print("File does not exist.")

class Writer:
    def __init__(self, list_data):
        self._list = list_data

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, new_list):
        self._list = new_list
    #append row to csv file
    def append_to_file(self):
        with open("quiz.csv", "a", newline='') as csvfile:
            fieldnames = ["id", "active", "question", "a", "b", "c", "correct_answer", "n_shown_practice", "n_shown_tests", "correct", "incorrect", "percentage_correct"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(self._list)
    #write file to csv file
    def write_to_file(self):
        with open("quiz.csv", "w", newline='') as csvfile:
            fieldnames = ["id", "active", "question", "a", "b", "c", "correct_answer", "n_shown_practice", "n_shown_tests", "correct", "incorrect", "percentage_correct"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self._list)

def main():

    category = ""
    print_menu()
    while True:
        #check if user input is correct
        try:
            category = int(input("Nr.: "))
            if category > 0 and category < 6:
                if category == 4 or category == 5:
                    reader = Reader()
                    question_count = len(reader.read_file())
                    if question_count < 5:
                        print("Please add at least 5 questions before entering practice or test mode.")
                        continue
                break
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")
    #runs corresponding function
    match category:
        case 1:
            sub_menu()
        case 2:
            get_statistics()
        case 3:
            change_status()
        case 4:
            practice()
        case 5 :
            test()

def print_menu():
    print()
    print("Chose category: ")
    print()
    print("1. Add question.")
    print("2. Statistic.")
    print("3. Disable/enable questions.")
    print("4. Practice mode.")
    print("5. Test mode.")
    
def sub_menu():
    print("Choose sub category: ")
    print("1. Add Quiz question.")
    print("2. Add free form question.")
    while True:
        #check for sub menu (quiz or free form question)
        try:
            sub_category = int(input("Nr.: "))
            
            if sub_category == 1:
                add_quiz_question()
                break
            elif sub_category == 2:
                add_free_form_question()
                break
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")
            
#gets question and answer for quiz
def get_quiz_QA():
    quiz_question = input("Enter quiz question: ").lower()
    quiz_answer_a = input("Answer for quiz question A: ").lower()
    quiz_answer_b = input("Answer for quiz question B: ").lower()
    quiz_answer_c = input("Answer for quiz question C: ").lower()
    correct_answer = input("Correct answer: ").lower()
    return (quiz_question,quiz_answer_a,quiz_answer_b,quiz_answer_c,correct_answer)

#writes quiz question and all other info to csv file
def add_quiz_question():
    question, a, b, c, correct_answer = get_quiz_QA()
    id = quiz_id()
    active = True
    default_values = {"n_shown_practice": 0,"n_shown_tests": 0,"correct": 0,"incorrect": 0,"percentage_correct": 0}
    question_data = {"id": id,"active": active,"question": question,"a": a,"b": b,"c": c,"correct_answer": correct_answer}
    question_data.update(default_values)
    writer = Writer(question_data)
    writer.append_to_file()
    
#gets question and answer for free form
def get_free_form_Q():
    free_form_q = input("Enter free form question: ").lower()
    free_form_a = input("Enter answer to free form question: ").lower()
    return (free_form_q,free_form_a)

#writes free form question and all other info to csv file
def add_free_form_question():
    question,correct_answer = get_free_form_Q()
    id = quiz_id()
    active = True
    
    default_values = {"n_shown_practice": 0,"n_shown_tests": 0,"correct": 0,"incorrect": 0,"percentage_correct": 0}
    question_data = {"id": id,"active": active,"question": question,"correct_answer": correct_answer}
    question_data.update(default_values)
    writer = Writer(question_data)
    writer.append_to_file()

#reads all info from csv file and print's it with tabulate
def get_statistics():
    reader = Reader()
    print(tabulate(reader.read_file(),headers="keys",tablefmt="grid"))

#takes input which question to activate or disable
def change_status():
    #checks for valid input
    while True:
        try:
            entered_id = int(input("Enter ID: "))
            break
        except ValueError:
            print("Bad input.")
    reader = Reader()
    question_found = False
    for row in reader.read_file():
        if entered_id == int(row["id"]):
            status = "Active" if row['active'] == "True" else "Inactive"
            print(f"Question with ID {entered_id} is {status}")
            question_found = True
            break
    #if entered id is found asks for comfirmation
    if question_found:
        value = input("Do you want to change the value? (Y/N): ").lower()
        if value == "y":
            button = Button(entered_id)
            button.change_status()
        elif value == "n":
            print("Value has not been changed.")
        else:
            print("Invalid input")
        
    else:
        print("Question with the entered ID was not found.")


def practice():
    reader = Reader()
    #gets all needed info for practice mode
    #practice only on question with state True
    questions, weight = get_weights_and_choices()
    random_choices = weighted_random_choices(questions, weight, k=len(questions))
    all_rows = reader.read_file()

    for i in random_choices:
        for row in all_rows:
            if i == row["question"]:
                print(row["question"])
                n_shown = int(row["n_shown_practice"])
                row["n_shown_practice"] = n_shown + 1
                if row["b"] == "" and row["c"] == "":
                    if_free_form_q(row)
                else:
                    if_quiz_q(row)
                percent = percentage_counter(int(row["correct"]), int(row["incorrect"]))
                row["percentage_correct"] = percent
    writer = Writer(all_rows)
    writer.write_to_file()
    print("Practice finished.")

def test():
    #gets all needed info for test mode
    #test only on question with state True
    reader = Reader()
    date = datetime.datetime.today()
    now = date.strftime("%Y-%m-%d %H:%M:%S")
    score = 0
    all_info = reader.read_file()
    
    #collects questions with active status
    active_questions = get_active_questions(all_info)
    random.shuffle(active_questions)
    len_of_number = check_active_questions(active_questions)
    
    #prints active questions
    for i in active_questions[:len_of_number]:
        for row in all_info:
            if i == row["question"]:
                print(row["question"])
                n_shown = int(row["n_shown_tests"]) 
                row["n_shown_tests"] = n_shown + 1
                if row["b"] == "" and row["c"] == "":
                    score += if_free_form_q(row)
                else:
                    score += if_quiz_q(row)
            #calculates percentage and ads to to row
            percent = percentage_counter(int(row["correct"]),int(row["incorrect"]))
            row["percentage_correct"] = percent  
    print(f"You answered correctly {score} questions out of {len_of_number}.")  
    score_str = f"Out of {len_of_number} questions, {score} was answered correctly."
    print("Test finished.")
    score_and_time =[now,score_str]
    #writes test result to txt file
    with open("results.txt","a",newline='') as txtfile:
        writer = csv.writer(txtfile)
        writer.writerow(score_and_time)
        
    writer = Writer(all_info)   
    writer.write_to_file()  

#loads active questions with state True
def get_active_questions(all_info):
    questions = []
    for row in all_info:
        if row["active"] == "True":
            questions.append(row["question"])
    return questions

#prints how many active question there is, ask how many to test out of given, checks for innput
def check_active_questions(active):
    while True:
        print(f"{len(active)} active questions.")
        try:
            n_of_questions = int(input("Number of questions to test: "))
            if n_of_questions > len(active):
                print(f"Entered number is greater than the number of questions. {len(active)} questions are active.")
            else:
                print(f"{n_of_questions} questions selected.")
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return n_of_questions

#gets all active question and percentage of correctly answered 
def get_weights_and_choices():
    reader = Reader()
    question_list = []
    weights = []
    for row in reader.read_file():
        if row["active"] == "True":
            weights.append(int(row["percentage_correct"]))
            question_list.append(row["question"])
    return question_list,weights

#asks user for question and answer for free form question. add point in csv to correct or incorrect
def if_free_form_q(row):
    score = 0
    question_input = input("Answer: ")
    if question_input == row["correct_answer"]:
        correct = int(row["correct"]) 
        row["correct"] = correct + 1
        score += 1
        print("Correct answer.")
        
    else:
        incorrect = int(row["incorrect"]) 
        row["incorrect"] = incorrect + 1
        print("Incorect answer.")
    return score

#asks user for question and answer for quiz question. add point in csv to correct or incorrect
def if_quiz_q(row):
    score = 0
    print(f"Answer 1: {row['a']}")
    print(f"Answer 2: {row['b']}")
    print(f"Answer 3: {row['c']}")
    quiz_input = input("Write your answer: ").lower()
    if quiz_input == row["correct_answer"]:
        print("you are correct!")
        score += 1
        correct = int(row["correct"])
        row["correct"] = correct + 1
    else:
        incorrect = int(row["incorrect"]) 
        row["incorrect"] = incorrect + 1
        print("You are incorrect!")
    return score

#calculates weights for for question, higher weight - more same questions
def weighted_random_choices(choices, weights, k=1):
    non_zero_weights = [1 if w == 0 else w for w in weights]
    reversed_weights = [100 / w for w in non_zero_weights]
    return random.choices(choices, weights=reversed_weights, k=k)


def percentage_counter(correct, incorrect):
    total = correct + incorrect
    if total == 0:
        return 0
    percent = round((correct / total) * 100)
    return percent

def quiz_id():
    reader = Reader()
    existing_ids = set()
    for row in reader.read_file():
        existing_ids.add(int(row["id"]))
    available_ids = set(range(1, 100))
    unused_ids = available_ids - existing_ids
    if not unused_ids:
        print("No more space in file.")
        exit()
    new_id = random.choice(list(unused_ids))
    return new_id

if __name__ == "__main__":
    main()
    
# https://github.com/SimonasKuprys/Interactive-learning-tool.git
# https://github.com/SimonasKuprys/Card-War-Game.git