import csv
from Milestone2 import LinkedQueue, EnrollmentRecord, HashMapping, binary_search_helper, merge_sort_helper, quicksort_helper
from datetime import date

def load_courses(filename, university):
    with open(filename, "r", newline= '') as csv_file:
        my_reader = csv.DictReader(csv_file)
        for row in my_reader:
            course_id = row["course_id"]
            credits = int(row["credits"])
            capacity = int(row["capacity"])
            university.add_course(course_id, credits, capacity)

def load_course_prerequisites(filename, university: "University"):
    with open(filename, "r", newline= '') as csv_file:
        my_reader = csv.DictReader(csv_file)
        for row in my_reader:
            course_id = row["course_id"]
            prereq = row["prerequisite"]
            
            course = university.get_course(course_id)
            if prereq != "":
                course.prerequisite[prereq] = True
            
def university_data_to_dict(filename):
    # This was created by ryan and it reads the csv file, creates, stores, and returns the dict with the information included
    """
    Created by Ryan.

    Reads a CSV file containing university data  and returns
    a dictionary with student_id, name, and courses
    """
    university_dict = {}

    with open(filename, "r", newline = '') as csv_file:
        my_reader = csv.DictReader(csv_file)
        for row in my_reader:
            student_id = row['student_id'] # takes in the student_id and its row
            name = row['name'] # gets the name of whats in that student_id's row
            courses = row['courses'] # gets the course of whats in that student_id's row
            courses_dict = {} # make a dictionary for the courses
            course_pairs = courses.split(";")
            for pair in course_pairs: 
                course, grade = pair.split(":") #splits course as key and grade as value inside of the dict
                courses_dict[course] = grade

            university_dict[student_id] = { #when inputted a student_id gives out the name and courses which values are courses_dict
                "name": name,
                "courses": courses_dict
        }
    return university_dict

class Courses: 
    """
    By: Ryan
    
    This represents a university course. It stores the course_code,
    number of credits, and a list of enrolled Student objects.
    """
    def __init__(self, course_code: str, credits: int, capacity: int, prerequisite: HashMapping):
        """
        Initializes a Course object with course_code, credit value,
        and list of students enrolled.
        """
        self.course = course_code
        self.credits = credits
        self.capacity = capacity
        self.prerequisite = prerequisite
        
        self.enrolled = [] # list of EnrollmentRecord
        self.waitlist = LinkedQueue() # queue of student objects
        self.sorted_by = None
    
    # Supposed to add a Student object to the course roster    
    def request_enroll(self, student: "Student", enroll_date: str):
        for record in self.enrolled:
            if record.student.student_id == student.student_id:
                raise ValueError("Student already enrolled")
            
        """
        Prereq checker
        """
        for prereq, _ in self.prerequisite.items():
            if prereq not in student.courses:
                raise ValueError(f"Missing prerequisite: {prereq}")
        
        if len(self.enrolled) < self.capacity:
            record = EnrollmentRecord(student, enroll_date)
            self.enrolled.append(record)
        else:
            self.waitlist.enqueue(student)
   
    def drop(self, student_id: str, enroll_date: str = None):
        if self.sorted_by != "id":
           raise ValueError("Roster must be sorted by ID first")
       
        index = binary_search_helper(self.enrolled, student_id)
       
        if index == -1:
            raise ValueError("Student not found")
        self.enrolled.pop(index)
        self.sorted_by = None
        
        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()
            if enroll_date is not None:
                new_date = enroll_date
            else:
                new_date = date.today().strftime("%Y-%m-%d")
            new_record = EnrollmentRecord(next_student, new_date)
            self.enrolled.append(new_record)
   
   # returns the number of students currently enrolled 
    def get_student_count(self) -> int:
        """
        Returns the number of students currently enrolled in the course.
        """
        return len(self.enrolled)
    
    def sort_enrolled(self, by, algorithm):
        """
        Sorts the roster by name, id, or enroll date using either Merge or Quick Sort
        """
        def get_val(record):
            if by == 'id': 
                return record.student.student_id
            if by == 'name': 
                return record.student.name
            return record.enroll_date

        paired_list = []
        for record in self.enrolled:
            key = get_val(record)
            paired_list.append((key,record))
        
        if algorithm == 'Merge':
            merge_sort_helper(paired_list)
        
        if algorithm == 'Quick':
            quicksort_helper(paired_list)
        
        # Get the sorted records
        self.enrolled = []
        for pair in paired_list:
            self.enrolled.append(pair[1])
            
        self.sorted_by = by
    
class Student:
    """
    By: Johnny
    
    This represents a student at the university. Stores student_id, name,
    and a dictionary of courses taken with the grade value recieved.     
    """
    def __init__(self,student_id: str, name: str, courses: dict):
        """
        Initializes a Student object with an ID, name, and 
        a dictionary of courses taken with grades recieved.
        """
        if len(student_id) != 8: 
            raise ValueError("Student_id isn't equal to 8 characters")
        if student_id[0:3] != "STU":
            raise ValueError("Student_id does not start with STU")
        for i in student_id[3:]:
            if i < "0" or i > "9":
                raise ValueError("Student_id doesn't include numbers after the STU character")
        self.student_id = student_id
        self.name = name
        #courses is a dictionary of courses a student has taken Course: grade "A", "B+"
        self.courses = courses
        self.student_courses = []
        for key in self.courses:
            self.student_courses.append(key)
        self.grade_point = {
        'A' : 4.0, 'A-' : 3.7,
        'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,
        'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,
        'D' : 1.0,
        'F' : 0.0
        }
    
    def enroll(self, course: str, grade: str):
        """
        By: Johnny
        Enrolls student ina  course and assigns a grade.
        """
        if grade not in self.grade_point:
            raise ValueError("Grade does not exist in grade point")
        if course in self.student_courses:
            raise ValueError(f"The student is already enrolled in {course}")
        self.courses[course] = grade
        self.student_courses.append(course)
        
    def update_grade(self,course: str,grade: str):
        """
        By: Ryan
        Updates the student's grade for a specific course.
        """
        if grade not in self.grade_point:
            raise ValueError("Grade does not exist in grade point")
        if course not in self.courses:
            raise ValueError("Course is not in the catalog")
        self.courses[course] = grade
    
    def calculate_gpa(self) -> float:
        """
        By: Ryan
        
        Calculates and returns a float value of the student's GPA based on
        course grades and credit value of the courses.
        """
        total_gpa = 0
        student_cred = []
        self.student_grades = []
        self.student_gpanum = []

        """
        Created by Ryan:
        This loop appends the values of the courses to student_grades
        """
        for value in self.courses.values():
            self.student_grades.append(value)

        """
        Created by Ryan:
        This loop finds for every grade in the list of student_grades, if
        grade is in grade_point then it appends the grade num of that grade to
        a new list of gpa numbers.
        """
        
        for grade in self.student_grades:    
            if grade in self.grade_point:
                self.student_gpanum.append(self.grade_point[grade])
    
        for item in self.student_courses:
            if item in course_data:
                student_cred.append(course_data[item]) # gives all the credits

        self.total_cred = sum(student_cred)
        
        for i in range(len(self.student_gpanum)):
            total_gpa = total_gpa + (self.student_gpanum[i] * student_cred[i])

        """
        Created by Ryan:
        This verifies that the total credits isn't zero and if it is will return
        the gpa as 0. Else it returns the total gpa divided by the total credits
        """

        if self.total_cred == 0:
            return 0.00
        else:
            total_gpa /= self.total_cred
            return f"{total_gpa:.2f}"
    
    def get_courses(self) -> list:
        """
        By: Johnny
        Returns a list of courses the student has taken.
        """
        return self.student_courses
    
    def get_course_info(self) -> str:
        """
        By:Johnny
        Returns the formatted information about the students, name, courses, grades,
        and total credits.
        """
        return f"{self.name} has taken {self.student_courses}, and has these grades {self.student_grades}, these classes accumulate to {self.total_cred} credits."   

class University:
    """
    Completly made by: Johnny
    
    Represents the university system. It manages and creates Student and Course
    objects while providing methods to add and retrieve information from them.  
    """
    def __init__(self):
        """
        Initializses the University with empty dictionaries for students
        and courses.
        """
        # Student Object
        self.students = {}
        
        #Course Object
        self.courses = {}
        
    def add_course(self, course_code: str, credits: int, capacity: int, prerequisites: HashMapping = None) -> Courses: # Course object
        """
        Adds a new course to the university if it does not exist.
        Returns the course object.
        """ 
        if course_code in self.courses:
            raise ValueError("Course already exists")
        
        new_course = Courses(course_code, credits, capacity, HashMapping())
        self.courses[course_code] = new_course
        return new_course

    def add_student(self, student_id: str, name: str) -> Student: # Student object 
        """
        Adds a new student to the university if they do not exist.
        Returns the student object.
        """
        if student_id in self.students:
            raise ValueError("Student already exists")
        
        if student_id in self.students:
            return self.students[student_id]
        
        new_student = Student(student_id, name, {})
        self.students[student_id] = new_student
        return new_student
    
    def get_student(self, student_id: str) -> Student: #Student Object
        """
        Returns the Student object for the ID given, or None
        if the student does not exist.
        """
        if student_id in self.students:
            return self.students[student_id]
        raise ValueError

    def get_course(self, course_code: str) -> Courses: # Course object
        """
        Returns the Course object for the given course code, or None 
        if the course does not exist.
        """
        if course_code in self.courses:
            return self.courses[course_code]
        raise ValueError
    
    def get_course_enrollment(self, course_code: str) -> int:
        """
        Returns the number of students enrolled in the given course.
        """
        student_count = self.courses[course_code].get_student_count()
        return student_count
    
    def get_students_in_course(self, course_code: str) -> list[Student] | None: # List of student objects or None if course doesn't exist
        """
        Returns a list of Student objects enrolled in the course, or None
        if the course does not exist.
        """
        if course_code in self.courses:
            return self.courses[course_code].students
        return None

