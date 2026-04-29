import unittest
from Milestone import University
from Milestone2 import HashMapping 

class TestMilestone3(unittest.TestCase):
    # Hashmap Tests
    def test_collision(self):
        # Checks to see if collision handling works since 5 and 15 go to bucket 5
        hashmap = HashMapping(10)
        hashmap[5] = "apple"
        hashmap[15] = "banana"

        self.assertEqual(hashmap[5], "apple")
        self.assertEqual(hashmap[15], "banana")

        # Checks if overwriting existing keys changes length or not
        hashmap[5] = "orange"
        self.assertEqual(hashmap[5], "orange")
        self.assertEqual(len(hashmap), 2)

    def test_rehashing(self):
        hashmap = HashMapping(5)
        hashmap[5] = "apple"
        hashmap[15] = "banana"
        hashmap[7] = "orange"
        hashmap[3] = "watermelon"

        self.assertEqual(len(hashmap), 4)
        self.assertEqual(hashmap._size, 10)
    
    # Enrollment Tests
    def test_prereq(self):
        uni = University()
        uni.add_course("CSE1010", 3, 30)
        uni.add_course("CSE2050", 3, 30)
        uni.add_course("CSE3100", 3, 30)
        uni.add_course("CSE3500", 3, 30)
        
        uni.get_course("CSE2050").prerequisite["CSE1010"] = True
        uni.get_course("CSE3100").prerequisite["CSE2050"] = True
        uni.get_course("CSE3500").prerequisite["CSE3100"] = True

        # Initializes Ryan and has only taken CSE1010
        student1 = uni.add_student("STU00001", "Ryan")
        student1.enroll("CSE1010", "A")
        
        # Tests to see if Ryan has taken CSE 2050 or not
        course = uni.get_course("CSE3100")
        with self.assertRaises(ValueError):
            course.request_enroll(student1, "2026-04-04")

        # Initializes Johnny and has taken CSE2050
        student2 = uni.add_student("STU00002", "Johnny")
        student2.enroll("CSE1010", "B+")
        student2.enroll("CSE2050", "A")

        # Tests to see if Johnny has taken CSE 2050 or not
        course.request_enroll(student2, "2026-04-05")
        self.assertEqual(course.get_student_count(), 1)

    # Sorting Tests (MERGE)
    def test_mergesort(self):
        uni = University()
        course = uni.add_course("CSE2050", 3, 10)
        student1 = uni.add_student("STU00001", "Johnny")
        student2 = uni.add_student("STU00002", "Ryan")
        course.request_enroll(student2, "2026-04-03")
        course.request_enroll(student1, "2026-04-01")

        course.sort_enrolled('id', 'merge')
        self.assertEqual(course.enrolled[0].student.student_id, "STU00001")

        course.sort_enrolled("name", "merge")
        self.assertEqual(course.enrolled[0].student.name, "Johnny")

        course.sort_enrolled('date', 'merge')
        self.assertEqual(course.enrolled[0].enroll_date, "2026-04-01")
        self.assertEqual(course.enrolled[1].enroll_date, "2026-04-03")
    
    # Sorting Tests (QUICK)
    def test_quicksort(self):
        uni = University()
        course = uni.add_course("CSE2050", 3, 10)
        student1 = uni.add_student("STU00001", "Johnny")
        student2 = uni.add_student("STU00002", "Ryan")
        course.request_enroll(student2, "2026-04-03")
        course.request_enroll(student1, "2026-04-01")

        course.sort_enrolled('id', 'quick')
        self.assertEqual(course.enrolled[0].student.student_id, "STU00001")

        course.sort_enrolled("name", "quick")
        self.assertEqual(course.enrolled[0].student.name, "Johnny")

        course.sort_enrolled('date', 'quick')
        self.assertEqual(course.enrolled[0].enroll_date, "2026-04-01")
        self.assertEqual (course.enrolled[1].enroll_date, "2026-04-03")

if __name__ == "__main__":
    unittest.main()