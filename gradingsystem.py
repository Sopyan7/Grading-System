# Bubble Sort Algorithm
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

#Entering Module (name, code, N of assessments)
class Module:
    def __init__(self, name, code, assessments, weights):
        self.name = name
        self.code = code
        self.asssessments = assessments
        self.weights = weights
        self.students = []

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
            def key(student: Student):
                return student.firstname
        elif sort == 'lastname':
            def key(student: Student):
                return student.lastname
        elif sort == 'score':
            def key(student: Student):
                # I could use `student.average`, but the task strictly says "Sort the output based on the TOTAL SCORE [...]"
                # I invert the value, because the best score should be at the top
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
            row = [student.firstname, student.lastname, 0,
                   student.average]
            for x in range(len(self.asssessments)):
                student[2] += student.scores[x] * self.weights[x]
            student[2] = int(student[2])
            row.extend(performance(student[2]))
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
        for assessment in range(self.asssessments):
            rows.append([assessment, *self.get_min_max_avg(assessment)])

        table_print(headers, rows)

#Students Class
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

    def typed_input(self, phrase, type, typename):
        while True:
            str = input(phrase)
            try:
                return type(str)
            except ValueError:
                print('Expected a ' + typename)
		#Creating Module
    def create_module(self):
        print('--[Module creation]--')
        name = input('Module name: ')
        code = input('Module code: ')
        while True:
            assessments = self.typed_input('Amount of assessments: ', int,
                                           'whole number')
            if assessments > 0:
                break
            print('Amount must be above 0.')
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

        self.module = Module(name, code, assessments, weights)
        print('√ Created the module ' + name)
		
		#Adding Student
    def add_student(self):
        print('--[Add student]--')
        firstname = input('Firstname of the student: ')
        lastname = input('Lastname of the student: ')
        studentid = self.typed_input('Student ID: ', int, 'whole number')
        scores = []
        while len(scores) < self.module.asssessments:
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
        print('√ Added student ' + firstname + ' ' + lastname)
		#Listing Options
    def list(self):
        print('--[List Settings]--')
        while True:
            yesno = input('Full info? [Y/n] ').lower()
            if yesno in 'yn':
                yesno = yesno == 'y'  # convert to boolean
                break
        while True:
            sortmode = input('Sorted by? [firstname/lastname/score] ')
            if sortmode in ('firstname', 'lastname', 'score'):
                break

        self.module.display_student_table(sortmode, yesno)
		#Choosing Options
    def main(self):
        self.create_module()
        while True:
            print('--[Main Menu]--')
            print('Actions:')
            print('  1. Add student')
            print('  2. List students')
            print('  3. List lowest/highest score of assessments')
            action = self.typed_input('Action: ', int, 'whole number')
            if action == 1:
                self.add_student()
            elif action == 2:
                self.list()
                input('Press return to continue> ')
            elif action == 3:
                self.module.display_assessments()
                input('Press return to continue> ')

            else:
                print('Invalid action.')

#Main Class
if __name__ == '__main__':
    ic = InteractiveControl()
    ic.main()