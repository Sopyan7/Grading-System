import json
from os import system, name
from time import sleep

def sort_algorithm(list, key=lambda obj: obj):
    changed = True
    while changed:
        last = None
        changed = False
        for lno, l in enumerate(list):
            if last is not None and key(l) < last:
                list[lno - 1], list[lno] = list[lno], list[lno - 1]
                changed = True

            last = key(l)
# Minimum
def min(list):
    m = float('inf')
    for x in list:
        if x < m:
            m = x
    return m

#Maximum
def max(list):
    m = -float('inf')
    for x in list:
        if x > m:
            m = x
    return m

#Sum
def sum(list):
    s = 0
    for x in list:
        s += x
    return s

#Enumerate List
def enumerate(list):
    l = []
    i = 0
    for x in list:
        l.append((i, x))
        i += 1
    return l

#Doing the table 
def table_print(headers, rows):
    longest = []
    for headerno, header in enumerate(headers):
        hl = len(header)
        for row in rows:
            if len(str(row[headerno])) > hl:
                hl = len(str(row[headerno]))
        longest.append(hl)

    header_str = ''
    header_sub = ''
    for headerno, header in enumerate(headers):
        header_str += header.ljust(longest[headerno]) + ' '
        header_sub += '-' * longest[headerno] + ' '

    print(header_str[:-1])
    print(header_sub[:-1])
    for row in rows:
        item_str = ''
        for itemno, item in enumerate(row):
            item_str += str(item).ljust(longest[itemno]) + ' '
        print(item_str[:-1])

def save_data_module(data:dict):
    try:
        with open('module.json','r') as file:
            json_data = json.load(file)
            json_data['modules'].append(data)
            with open('module.json','w') as file1:
                json.dump(json_data,file1)
    except Exception as E:
        print(E)
        json_data = {
            'modules':[]
        }
        json_data['modules'].append(data)
        with open('module.json','w') as file1:
            json.dump(json_data,file1)

def save_student(data:dict , id:str):
    try:
        with open('module.json','r') as file:
                json_data = json.load(file)
                for module in json_data['modules']:
                    if module["id"] == id:
                        module["students"].append(data)
                        with open('module.json','w') as file1:
                            json.dump(json_data,file1)
                            return True
    except:
        return False

def get_module_by_id(id:str):
    with open('module.json','r') as file:
        json_data = json.load(file)
        for module in json_data['modules']:
            if module["id"] == id:
                return module
        return False


class Module:

    def __init__(self,id,name,code,assessments,weights,students=[]):
        self.id = id
        self.name = name
        self.code = code
        self.assessments = assessments
        self.weights = weights
        self.students = students
    
    def calculate_average_score(self, assessment=None):
        if self.students:
            scores = []
            if assessment is None:
                for student in self.students:
                    scores.append(student.average)
            else:
                for student in self.students:
                    scores.append(student.scores[assessment])
            return int(sum(scores) / len(scores))
        return 0

    def get_min_max_avg(self, assessment=None):
        if self.students:
            scores = []
            if assessment is None:
                for student in self.students:
                    scores.extend(student.scores)
            else:
                for student in self.students:
                    scores.append(student.scores[assessment])

            return min(scores), max(scores), sum(scores) / len(scores)

        return 0, 0

    def display_student_table(self, sort='score', full_student_info=False):
        if sort == 'firstname':
            def key(student):
                return student.firstname
        elif sort == 'lastname':
            def key(student):
                return student.lastname
        elif sort == 'score':
            def key(student):
                return -sum(student.scores)
        else:
            raise ValueError("sort must be 'firstname', 'lastname' or 'score'")

        # Sort
        students = self.students.copy()
        sort_algorithm(students, key=key)

        headers = ['Firstname', 'Lastname', 'Total score', 'Average score', 'Grade', 'Degree']
        if full_student_info:
            headers.append('Student ID')

        rows = []
        for student in students:
            row = [student.firstname, student.lastname, 0,student.average]
            for x in range(self.assessments):
                row[2] += student.scores[x] * self.weights[x]
            row[2] = int(row[2])
            row.extend(performance(row[2]))
            if full_student_info:
                row.append(student.id)
            rows.append(row)

        table_print(headers, rows)
		
		#Display Assessments
    def display_assessments(self):
        headers = ['Assessment', 'Lowest score', 'Highest score', 'Average score']
        rows = [
            ['All combined', *self.get_min_max_avg()]
        ]
        for assessment in range(self.assessments):
            rows.append([assessment, *self.get_min_max_avg(assessment)])

        table_print(headers, rows)

class Student:
    def __init__(self, firstname, lastname, id, scores):
        self.firstname = firstname
        self.lastname = lastname
        self.id = id
        self.scores = scores
        if scores:
            self.average = int(sum(scores) / len(scores))
        else:
            self.average = 0

#Grade performance counter
def performance(score: float):
    if score >= 70:
        return 'Excellent', 'First'
    elif score >= 60:
        return 'Good to very Good', 'Upper Second 2:1'
    elif score >= 50:
        return 'Satisfying', 'Lower Second 2:2'
    elif score >= 40:
        return 'Sufficient', 'Third 3'
    return 'Unsatisfactory', 'Fail'


class InteractiveControl:
    def __init__(self):
        self.module = None

    def object_decoder(self,data:dict):
        print(data)
        self.module.id = data["id"]
        self.module.name = data["name"]
        self.module.code = data["code"]
        self.module.assessments = data["assessments"]
        self.module.weights = data["weights"]
        self.module.students = data["students"]
    
    def show_objects(self):
        for data in range(self.module):
            print(data.__dict__)
    
    def show_data(self):
        print('Module ID - ' + self.module.id)
        print('Module Name - ' + self.module.name)
        print('Module Code - ' + self.module.code)
        print('Assessments - ' + str(self.module.assessments))
        print('Weights - ' + str(self.module.weights))

    def typed_input(self, phrase, type, typename):
        while True:
            str = input(phrase)
            try:
                return type(str)
            except ValueError:
                print('Expected a ' + typename)
    
    def weights_creation(self,assessments):
        weights = []
        while len(weights) < assessments:
            while True:
                weight = self.typed_input(
                    'Weight of the assessment ' + str(len(weights) + 1) + ': ',
                    float,
                    'floating point number'
                )
                if 1 >= weight >= 0:
                    break
                print('Weight must be between 0 and 1.')
            weights.append(weight)
        return weights

	#Creating Module
    def create_module(self):
        print('--[Module creation]--')
        id = input('Module ID: ')
        name = input('Module name: ')
        code = input('Module code: ')
        while True:
            assessments = self.typed_input('Amount of assessments: ', int,'whole number')
            if assessments > 0:
                break
            print('Amount must be above 0.')
        
        while True:
            weights = self.weights_creation(assessments)
            sum = 0
            for i in weights:
                sum = sum + i
            
            if sum == 1.0:
                break
            print('All Weights should be add upto 1.0')

        self.module = Module(id , name, code, assessments, weights)
        save_data_module(self.module.__dict__)
        print('√ Created the module ' + name + ' With ID ' + id)

    def add_student(self):
        module_id = input('Please pass the module ID:- ')
        module = get_module_by_id(module_id)
        if module:
            self.module = Module(module["id"],module["name"],module["code"],module["assessments"],module["weights"],module["students"])
            clear()
            print('--[Add student]--')
            firstname = input('Firstname of the student: ')
            lastname = input('Lastname of the student: ')
            studentid = self.typed_input('Student ID: ', int, 'whole number')
            scores = []
            while len(scores) < self.module.assessments:
                while True:
                    score = self.typed_input(
                        'Points from assessment ' + str(len(scores) + 1) + ': ',
                        int,
                        'whole number'
                    )
                    if 100 >= score >= 0:
                        break
                    print('Score must be between 0 and 100.')
                scores.append(score)

            student = Student(firstname, lastname, studentid, scores)
            self.module.students.append(student)
            save_student(student.__dict__,module_id)
            print('√ Added student ' + firstname + ' ' + lastname)
        else:
            print('Sorry we couldn\'t find that. Please recheck and try again.')
            sleep(2)
    
    def list(self):
        print('--[List Settings]--')
        while True:
            yesno = input('Full info? [Y/n] ').lower()
            if yesno in 'yn':
                yesno = yesno == 'y'  #Convert to boolean
                break
        while True:
            sortmode = input('Sorted by? [firstname/lastname/score] ')
            if sortmode in ('firstname', 'lastname', 'score'):
                break
        self.module.display_student_table(sortmode, yesno)

def main_menu():
    print('--[Main Menu]--')
    print('Actions:')
    print('1. Add a new Module')
    print('2. Add new Modules ( More than 1)')
    print('3. Move to Student Menu')
    print('4. Exit')

def action_1(ic):
    ic.create_module()
    sleep(2)

def action_2(ic):
    modules = None
    while True:
        try:
            modules = int(input('How many modules you want to create - '))
            break
        except ValueError:
            print('Value should be integer')
    count = 0
    while count < modules:
        count = count + 1
        ic.create_module()
    sleep(2)
    system('cls')

def main_function(ic):
    while True:
        system('cls')
        main_menu()
        select = int(input('Enter your Choice: '))
        clear()
        if select < 1 or select > 4:
            print('Invalid Choice.')
            sleep(2)
            clear()
        elif select == 1:
            action_1(ic)
        elif select == 2:
            action_2(ic)
        elif select == 3:
            clear()
            student_function(ic)
            clear()
        elif select == 4:
            print('See you soon :)')
            exit(0)

def student_function(ic):
    while True:
        print('--[Student Menu]--')
        print('Actions:')
        print('  1. Add student')
        print('  2. List students')
        print('  3. List lowest/highest score and weights of assessments')
        print('  4. Go Back to main menu')
        select = int(input('Enter your Choice: '))
        clear()
        if select < 1 or select > 4:
            print('Invalid Choice.')
            exit(0)
        elif select == 1:
            ic.add_student()
            sleep(2)
            clear()
        elif select == 2:
            ic.list()
            input('Press return to continue> ')
            clear()
        elif select == 3:
            ic.module.display_assessments()
            input('Press return to continue> ')
            clear()
        elif select == 4:
            break


def clear():
    system('cls')

if __name__ == '__main__':
    ic = InteractiveControl()
    while True:
        main_function(ic)
        clear()

