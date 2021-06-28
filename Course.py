# Consts
MAX_CLASS_SIZE = 16
MIN_CLASS_SIZE = 6
NUM_COURSES = 40
NUM_STUDENTS = 400

"""

This class represents a course with six fields.

name: name of the course
student: list of all student objects currently assigned that course
fixable: designates whether a given class can be made to fit the requirements (based on signups, but assumed True to start)
min_size and max_size: class-specific requirements on the minimum and maximum number of students allowed
id: the veracross_class_id, which is fed into the program
faculty: who is teaching the class
"""


class Course:
    # Fields
    def __init__(self, n, s, min_size, max_size, id, f):
        self.name = n
        self.students = s
        self.fixable = True
        self.min_size = min_size
        self.max_size = max_size
        self.id = id
        self.faculty = f

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
        if self.size() < self.min_size or self.size() > self.max_size:
            return False
        return True

    # Calculates the disparity of the class
    def disparity(self):
        # Disparity is a measurement of the difference between the ideal class
        # size and the current class size

        # If the class is too big, disparity is positive
        if self.size() > self.max_size:
            return self.size() - self.max_size

        # If the class is too small, disparity is negative
        elif self.size() < self.min_size:
            return self.size() - self.min_size

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

    # Measure of how far we are from perfection
    # Minimum is 0
    def cost(self):
        avg_size = NUM_STUDENTS/NUM_COURSES
        pref_disparity = [s.preferences.index(s.course) for s in self.students]
        return sum(pref_disparity)

    def toList(self):
        x = [self.name, self.faculty, str(self.size()) + " / " + str(self.max_size), str(self.cost())]
        if self.fixable:
            x.append("y")
        else:
            x.append("UNFIXABLE")
        for s in self.students:
            x.append(s.name +  " (Form " + s.form + "), p#" + str( s.preferences.index(self) + 1 ) )
        return x
