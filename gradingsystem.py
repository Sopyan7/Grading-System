import json
from os import system, name
from time import sleep

# Minimum
def min(list):
    m = float('inf')
    pos = 0
    for x in range(0,len(list)):
        if list[x] < m:
            m = list[x]
            pos = x
    return (m,pos)

#Maximum
def max(list):
    m = -float('inf')
    pos=0
    for x in range(0,len(list)):
        if list[x] > m:
            m = list[x]
            pos = x
    return (m,pos)

#Sum
def sum(list):
    s = 0
    for x in list:
        s += x
    return s

#Average
def average(list):
    av = 0
    s = 0
    for x in list:
        s += x
    av = s/len(list)
    return av

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

def get_all_modules():
    with open('module.json','r') as file:
        json_data = json.load(file)
        return json_data['modules']
    return False


class Module:

    def __init__(self,id,name,code,assessments,weights,students=[]):
        self.id = id
        self.name = name
        self.code = code
        self.assessments = assessments
        self.weights = weights
        self.students = students

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
        modules = get_all_modules()
        print('--[Add student]--')
        firstname = input('Firstname of the student: ')
        lastname = input('Lastname of the student: ')
        studentid = self.typed_input('Student ID: ', int, 'whole number')
        if modules:
            for module in modules:
                self.module = Module(module["id"],module["name"],module["code"],module["assessments"],module["weights"],module["students"])
                clear()
                scores = []
                while len(scores) < self.module.assessments:
                    while True:
                        score = self.typed_input(
                            f'Module of {self.module.id} and Points from assessment ' + str(len(scores) + 1) + ': ',
                            int,
                            'whole number'
                        )
                        if 100 >= score >= 0:
                            break
                        print('Score must be between 0 and 100.')
                    scores.append(score)
                student = Student(firstname, lastname, studentid, scores)
                self.module.students.append(student)
                save_student(student.__dict__,self.module.id)
            print('√ Added student to all modules ' + firstname + ' ' + lastname)
        else:
            print('Sorry we couldn\'t any data. Please recheck and try again.')
            sleep(2)

def main_menu():
    print('--[Main Menu]--')
    print('Actions:')
    print('1. Add a new Module')
    print('2. Add new Modules (Minimum 3)')
    print('3. Move to Student Menu')
    print('4. Exit')

def sort_object(student,key):
    changed = True
    if key == 'lastname':
        while changed:
            last=None
            changed = False
            for lno, l in enumerate(student):
                if last is not None and l[key] > last:
                    student[lno - 1]['firstname'], student[lno]['firstname'] = student[lno]['firstname'], student[lno - 1]['firstname']
                    student[lno - 1]['lastname'], student[lno]['lastname'] = student[lno]['lastname'], student[lno - 1]['lastname']
                    student[lno - 1]['id'], student[lno]['id'] = student[lno]['id'], student[lno - 1]['id']
                    student[lno - 1]['scores'], student[lno]['scores'] = student[lno]['scores'], student[lno - 1]['scores']
                    student[lno - 1]['average'], student[lno]['average'] = student[lno]['average'], student[lno - 1]['average']
                    changed = True
                else:
                    last = student[0][key]
        return student
    elif key == 'firstname':
        while changed:
            last=None
            changed = False
            for lno, l in enumerate(student):
                if last is not None and l[key] < last:
                    student[lno - 1]['firstname'], student[lno]['firstname'] = student[lno]['firstname'], student[lno - 1]['firstname']
                    student[lno - 1]['lastname'], student[lno]['lastname'] = student[lno]['lastname'], student[lno - 1]['lastname']
                    student[lno - 1]['id'], student[lno]['id'] = student[lno]['id'], student[lno - 1]['id']
                    student[lno - 1]['scores'], student[lno]['scores'] = student[lno]['scores'], student[lno - 1]['scores']
                    student[lno - 1]['average'], student[lno]['average'] = student[lno]['average'], student[lno - 1]['average']
                    changed = True
                else:
                    last = student[0][key]
        return student
    elif key == 'scores':
        while changed:
            last=None
            changed = False
            total = 0
            for lno, l in enumerate(student):
                total = sum(l[key])
                if last is not None and total > last:
                    student[lno - 1]['firstname'], student[lno]['firstname'] = student[lno]['firstname'], student[lno - 1]['firstname']
                    student[lno - 1]['lastname'], student[lno]['lastname'] = student[lno]['lastname'], student[lno - 1]['lastname']
                    student[lno - 1]['id'], student[lno]['id'] = student[lno]['id'], student[lno - 1]['id']
                    student[lno - 1]['scores'], student[lno]['scores'] = student[lno]['scores'], student[lno - 1]['scores']
                    student[lno - 1]['average'], student[lno]['average'] = student[lno]['average'], student[lno - 1]['average']
                    changed = True
                else:
                    last = sum(student[0][key])
        return student
    else:
        return False

def action_1(ic):
    ic.create_module()
    sleep(2)
def action_2(ic):
    modules = None
    while True:
        try:
            modules = int(input('How many modules you want to create - '))
            if modules < 3:
                print('Value should be Minimum 3')
                continue
            break
        except ValueError:
            print('Value should be integer')
    count = 0
    while count < modules:
        count = count + 1
        ic.create_module()
    sleep(2)
    system('cls')

def display_all_students(sort=None):
    if sort is None:
        headers = ['Student ID','Firstname', 'Lastname', 'Total score', 'Average score', 'Grade', 'Degree']
        rows = []
        modules = get_all_modules()
        for module_data in modules:
            module = Module(module_data["id"],module_data["name"],module_data["code"],module_data["assessments"],module_data["weights"],module_data["students"])
            print(f'\n\nModule {module.id}\n--------------\n\n')
            for student_data in module.students:
                student = Student(student_data["firstname"],student_data["lastname"],student_data["id"],student_data["scores"])
                row = [student.id , student.firstname, student.lastname, 0 , 0]
                for i in range(module.assessments):
                    row[3] += student.scores[i]
                    row[4] += student.scores[i] * module.weights[i]
                row.extend(performance(row[3]))
                rows.append(row)
            table_print(headers, rows)
            rows = []
    else:
        headers = ['Student ID','Firstname', 'Lastname', 'Total score', 'Average score', 'Grade', 'Degree']
        rows = []
        modules = get_all_modules()
        for module_data in modules:
            module = Module(module_data["id"],module_data["name"],module_data["code"],module_data["assessments"],module_data["weights"],module_data["students"])
            student_sorted = sort_object(module_data['students'],sort)

            print(f'\n\nModule {module.id}\n--------------\n\n')
            for student_data in student_sorted:
                student = Student(student_data["firstname"],student_data["lastname"],student_data["id"],student_data["scores"])
                row = [student.id , student.firstname, student.lastname, 0 , 0]
                for i in range(module.assessments):
                    row[3] += student.scores[i]
                    row[4] += student.scores[i] * module.weights[i]
                row.extend(performance(row[3]))
                rows.append(row)
            table_print(headers, rows)
            rows = []

def display_min_max_students(id:str,assessment:int,full_info=False):
    headers = ['Assessment','Lowest Score','Highest Score','High Scorer', 'Low Scorer', 'Average Score']
    rows = []
    module_data = get_module_by_id(id)
    module = Module(module_data["id"],module_data["name"],module_data["code"],module_data["assessments"],module_data["weights"],module_data["students"])
    if assessment <= module.assessments:
        scores = []
        for i in range(0,len(module.students)):
            scores.append(module.students[i]['scores'][assessment-1])
        min_num,min_pos = min(scores)
        max_num,max_pos = max(scores)
        high_score = f"{module.students[max_pos]['firstname']} {module.students[max_pos]['lastname']} - {module.students[max_pos]['id']}"
        low_score = f"{module.students[min_pos]['firstname']} {module.students[min_pos]['lastname']} - {module.students[min_pos]['id']}"
        row = [assessment , min_num , max_num , high_score, low_score, average(scores)]
        rows.append(row)
        table_print(headers, rows)
        if full_info == True:
            headers_1 = ['Student ID','Firstname','Lastname','Total Score','Average Secore','Grade','Degree']
            rows_1 = []

            # High Scorer Result
            student = Student(module.students[max_pos]["firstname"],module.students[max_pos]["lastname"],module.students[max_pos]["id"],module.students[max_pos]["scores"])
            row_1 = [student.id , student.firstname, student.lastname, 0 , 0]
            for i in range(module.assessments):
                row_1[3] += student.scores[i]
                row_1[4] += student.scores[i] * module.weights[i]
            row_1.extend(performance(row_1[3]))
            rows_1.append(row_1)
            print('\nHigh Scorer Info\n------------------\n\n')
            table_print(headers_1, rows_1)
            print('\nLow Scorer Info\n------------------\n\n')
            rows_1 = []
            row_1 = []

            # Low Scorer Result

            student = Student(module.students[min_pos]["firstname"],module.students[min_pos]["lastname"],module.students[min_pos]["id"],module.students[min_pos]["scores"])
            row_1 = [student.id , student.firstname, student.lastname, 0 , 0]
            for i in range(module.assessments):
                row_1[3] += student.scores[i]
                row_1[4] += student.scores[i] * module.weights[i]
            row_1.extend(performance(row_1[3]))
            rows_1.append(row_1)
            table_print(headers_1, rows_1)
        input('Press Return to continue> ')
    else:
        print('Couldn\'t Find any assessment. Please recheck and try again\n')
        input('Press Return to continue> ')

def display_average_score(id:str):
    headers = ['Assessment','Average Score']
    rows = []
    module_data = get_module_by_id(id)
    module = Module(module_data["id"],module_data["name"],module_data["code"],module_data["assessments"],module_data["weights"],module_data["students"])
    scores = []
    for x in range(0,module.assessments):
        for i in range(0,len(module.students)):
            scores.append(module.students[i]['scores'][x])
        row = [ x+1, average(scores)]
        rows.append(row)
    table_print(headers, rows)
    input('Press Return to continue> ')

def display_min_max_module(full_info=False):
    headers = ['Assessment','Lowest Score', 'Highest Score', 'Low Scorer', 'High Scorer']
    rows = []
    headers_1 = ['Student ID','Firstname','Lastname','Total Score','Average Score','Grade','Degree']
    row_1 = []
    row_2 = []
    data_row_1 = []
    data_row_2 = []
    modules_data = get_all_modules()
    for module_data in modules_data:
        rows = []
        print('\n\nModule ' + module_data["id"] + '\n-----------------------\n\n')
        module = Module(module_data["id"],module_data["name"],module_data["code"],module_data["assessments"],module_data["weights"],module_data["students"])
        scores = []
        for x in range(0,module.assessments):
            scores = []
            for i in range(0,len(module.students)):
                scores.append(module.students[i]['scores'][x])
            min_num,min_pos = min(scores)
            max_num,max_pos = max(scores)
            high_score = f"{module.students[max_pos]['firstname']} {module.students[max_pos]['lastname']} - {module.students[max_pos]['id']}"
            low_score = f"{module.students[min_pos]['firstname']} {module.students[min_pos]['lastname']} - {module.students[min_pos]['id']}"
            row = [ x+1, min_num, max_num, low_score, high_score]
            rows.append(row)
            if full_info == True:

                # High Scorer Result
                student = Student(module.students[max_pos]["firstname"],module.students[max_pos]["lastname"],module.students[max_pos]["id"],module.students[max_pos]["scores"])
                data_row_1 = [student.id , student.firstname, student.lastname, 0 , 0]
                for i in range(module.assessments):
                    data_row_1[3] += student.scores[i]
                    data_row_1[4] += student.scores[i] * module.weights[i]
                data_row_1.extend(performance(data_row_1[3]))
                row_1.append(data_row_1)

                # Low Scorer Result
                student = Student(module.students[min_pos]["firstname"],module.students[min_pos]["lastname"],module.students[min_pos]["id"],module.students[min_pos]["scores"])
                data_row_2 = [student.id , student.firstname, student.lastname, 0 , 0]
                for i in range(module.assessments):
                    data_row_2[3] += student.scores[i]
                    data_row_2[4] += student.scores[i] * module.weights[i]
                data_row_2.extend(performance(data_row_2[3]))
                row_2.append(data_row_2)
        table_print(headers, rows)
        if full_info == True:
            print('\nHigh Scorer Info\n------------------\n\n')
            table_print(headers_1, row_1)
            print('\nLow Scorer Info\n------------------\n\n')
            table_print(headers_1, row_2)
            row_1 = []
            row_2 = []
            data_row_1 = []
            data_row_2 = []
    # if full_info == True:
    #     print('\nHigh Scorer Info\n------------------\n\n')
    #     table_print(headers_1, row_1)
    #     print('\nLow Scorer Info\n------------------\n\n')
    #     table_print(headers_1, row_2)
    input('Press Return to continue> ')

def main_function(ic):
    while True:
        system('cls')
        main_menu()
        try:
            select = int(input('Enter your Choice: '))
            clear()
            if select < 1 or select > 4:
                print('Invalid Choice.')
                sleep(2)
                clear()
                continue
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
        except ValueError:
            print('Its not a number')
            sleep(2)
            clear()
            continue

def student_function(ic):
    while True:
        print('--[Student Menu]--')
        print('Actions:')
        print('  1. Add student')
        print('  2. List all students data [Total Score, Average, Degree]')
        print('  3. List and sort all student data')
        print('  4. List Minimum/Maximum and Average for a specific module/assessment')
        print('  5. List Average score for each module over all assessments')
        print('  6. List Minimum/Maximum for a specific module/assessment')
        print('  7. Go Back to main menu')
        try:
            select = int(input('Enter your Choice: '))
            clear()
            if select < 1 or select > 7:
                print('Invalid Choice.')
                sleep(2)
                clear()
                continue
            elif select == 1:
                ic.add_student()
                sleep(2)
                clear()
            elif select == 2:
                sort = None
                display_all_students(sort)
                input('Press return to continue> ')
                clear()
            elif select == 3:
                sort = None
                while True:
                    sort = input('How you wanna sort[firstname , lastname , scores]: ')
                    if sort == 'firstname' or sort == 'lastname' or sort == 'scores':
                        break
                    else:
                        continue
                display_all_students(sort)
                input('Press return to continue> ')
                clear()
            elif select == 4:
                id = input('Please specify Module ID:- ')
                assessment = int(input('Please specify Assessment Number:- '))
                full_info = input('do you want to display full info [y]/[n]:- ')
                if full_info == 'y' or full_info == 'Y':
                    display_min_max_students(id,assessment,full_info=True)
                else:
                    display_min_max_students(id,assessment,full_info=False)
                clear()
            elif select == 5:
                id = input('Please specify Module ID:- ')
                display_average_score(id)
                clear()
            elif select == 6:
                full_info = input('Do you want to display full info [y]/[n]:- ')
                if full_info == 'y' or full_info == 'Y':
                    display_min_max_module(True)
                else:
                    display_min_max_module(False)
                clear()
            elif select == 7:
                break
        except ValueError:
            print('Its not a number')
            sleep(2)
            clear()
            continue
def clear():
    system('cls')

if __name__ == '__main__':
    ic = InteractiveControl()
    while True:
        main_function(ic)
        clear()

