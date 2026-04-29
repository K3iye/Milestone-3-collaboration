from Milestone import University, load_course_prerequisites, load_courses

# MILESTONE 2 DEMO
# Set up university and course 
uni = University()
course = uni.add_course("CSE1010", 3, 2)

# Create 
stu1 = uni.add_student("STU00001", "Ryan")
stu2 = uni.add_student("STU00002", "Johnny")
stu3 = uni.add_student("STU00003", "Swamy")

course.request_enroll(stu1, "2026-04-08")
course.request_enroll(stu2, "2026-04-02")
course.request_enroll(stu3, "2026-04-05") # goes to waitlist capacity(2)

print("Enrolled:", course.enrolled)
print("Waitlist size:", len(course.waitlist))

course.sort_enrolled("id", "merge")
course.drop("STU00001")

print("After drop:")
print("Enrolled:", course.enrolled)
print("Waitlist size:", len(course.waitlist))

# MILESTONE 3 DEMO
# Set up university and load courses/prerequisites
uni2 = University()
load_courses("course_catalog_CSE10_with_capacity.csv", uni2)
load_course_prerequisites("cse_prerequisites.csv", uni2)

# Let's use CSE3100 for example which needs CSE2050 as a pre-req
student1 = uni2.add_student("STU00001", "Ryan")
student1.enroll("CSE1010", "A")
cse3100 = uni2.get_course("CSE3100")

# This test should have it fail because Ryan hasn't taken CSE2050 yet
try:
    cse3100.request_enroll(student1, "2026-04-04")
except ValueError as course_error:
    print(f"Error: {course_error}")

# Now let's get someone who completed CSE2050
student2 = uni2.add_student("STU00002", "Johnny")
student2.enroll("CSE2050", "A")
cse3100.request_enroll(student2, "2026-04-04")

# Let's check if Johnny is enrolled in CSE3100
print(cse3100.enrolled)



