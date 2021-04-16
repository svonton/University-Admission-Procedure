"""physics and math for the Physics department, chemistry for the Chemistry department,
math for the Mathematics department, computer science and math for the Engineering Department,
chemistry and physics for the Biotech department."""

num_students = int(input())
applicant_keys = ['name', 'last_name', 'physics', 'chemistry', 'math', 'computer science', 'special exam',
                  '1_priority', '2_priority', '3_priority']
department_keys = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
department_exams = {'Biotech': ['chemistry', 'physics'], 'Chemistry': ['chemistry'],
                    'Engineering': ['computer science', 'math'],
                    'Mathematics': ['math'], 'Physics': ['physics', 'math']}
single_exam_dep = ['Mathematics', 'Chemistry']
with open('applicant_list_7.txt', 'r') as f:
    applicants = []
    for line in f:  # read line by line from file info about every applicant
        # create a dictionary for every applicant
        applicant = {key: value for key, value in zip(applicant_keys, line.split())}
        applicants.append(applicant)  # add every applicant to the list with all applicants
for applicant in applicants:
    applicant['final_score'] = 0.0
applicants[0]['final_score'] = 1.1
print(applicants)


def sort_by(cntx):
    return sorted(cntx, key=lambda x: (-float(x['final_score']), x['1_priority'], x['name']))


def final_score_calc(cntx, exam):
    if len(exam) > 1:
        for cur_cntx in cntx:
            exam_score = float((float(cur_cntx[exam[0]])+float(cur_cntx[exam[1]]))/2)
            cur_cntx['final_score'] = exam_score if float(cur_cntx['special exam']) <= exam_score \
                else float(cur_cntx['special exam'])
        return cntx
    else:
        for cur_cntx in cntx:
            cur_cntx['final_score'] = float(cur_cntx[exam[0]]) if float(cur_cntx[exam[0]]) >= float(cur_cntx['special exam']) \
                else float(cur_cntx['special exam'])
        return cntx


# dictionary with keys as departments, will add a list of new students to every department
departments = {key: [] for key in department_keys}


def accept_students(priority):
    global applicants
    for department in departments:
        applicants = final_score_calc(applicants, department_exams[department])
        applicants = sort_by(applicants)
        num_accepted_students = len(departments[department])  # check how many students are already accepted
        not_accepted_applicants = []
        for applicant in applicants:
            if applicant[priority] == department and num_accepted_students < num_students:
                departments[department].append(applicant)
                num_accepted_students += 1
            else:
                not_accepted_applicants.append(applicant)  # add not accepted students to a new list of applicants
        applicants = list(not_accepted_applicants)  # updates the list of applicants


# add students to departments according to their priorities
for priority in ['1_priority', '2_priority', '3_priority']:
    accept_students(priority)

# print results, sort students according to GPA and names
for depart, students in departments.items():
    print(depart)
    file_name = depart+'.txt'
    with open(file_name, 'w') as f:
        students = sorted(students, key=lambda x: (-float(x['final_score']), x['name']))
        for student in students:
            print(student['name'], student['last_name'], student['final_score'])
            write_srt = student['name']+' '+student['last_name']+' '+str(student['final_score'])+'\n'
            f.write(write_srt)
        f.write('')
        print()


