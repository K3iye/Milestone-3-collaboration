# Milestone-3-collaboration
 -------------- How to use the program --------------------
To use the program you can open a python file and import University class from Milestone. The university class handles all inputs and is able to make objects for courses and students.
- use add_course() to create a course object
- use add_student() to create a student object
- enroll a student in a course with a grade
- Calculate students GPA
(Example code below) 
Another key thing to take into account highest grade is A lowest is F, grades like B+ and B- are included as well.

------------------ Example code ----------------------
from Milestone import University

uconn = University()

# Add a course
uconn.add_course("CSE2050", 3)

# Add a student
student = uconn.add_student("STU00001", "Johnny")

# Enroll the student in a course
student.enroll("CSE2050", "A")

# Calculate GPA
print(student.calculate_gpa())

---------------- How to run tests ---------------
To run the tests you can simply run the test_case.py file, if all tests pass, everything is working as intended.

