# Consts
MAX_CLASS_SIZE = 16
MIN_CLASS_SIZE = 6
NUM_COURSES = 40

# MAKE A SATISTFACTION SCORE

"""

This class represents a course with two fields.

Name: name of the course
Student: list of all student objects currently assigned that course

"""


class Course:
    # Fields
    def __init__(self, n, s):
        self.name = n
        self.students = s
        self.fixable = True

    # Methods
    # Returns the size of the class
    def size(self):
        return len(self.students)

    # Returns the distribution of grades in a given class
    def age_distribution(self):
        counts = {"3": 0, "4": 0, "5": 0}
        for s in self.students:
            counts[s.form] += 1
        return counts

    # Checks whether a class is valid --> both distribution and size
    def isValid(self):
        for key, val in self.age_distribution().items():
            if val <= 2:
                return False
        if self.size() < 6 or self.size() > 16:
            return False
        return True

    # Calculates the disparity of the class
    def disparity(self):
        # Disparity is a measurement of the difference between the ideal class
        # size and the current class size

        # If the class is too big, disparity is positive
        if self.size() > MAX_CLASS_SIZE:
            return self.size() - MAX_CLASS_SIZE

        # If the class is too small, disparity is negative
        elif self.size() < MIN_CLASS_SIZE:
            return self.size() - MIN_CLASS_SIZE

        # If the class is within the good bounds, disparity is 0
        else:
            return 0

    # Returns the distribution of grades using a list instead of dictionary
    def distribution(self):
        a = [0, 0, 0]

        for x in self.students:
            if x.form == "3":
                a[0] += 1
            elif x.form == "4":
                a[1] += 1
            else:
                a[2] += 1

        return a
