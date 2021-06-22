# Consts
MAX_CLASS_SIZE = 16
MIN_CLASS_SIZE = 6
NUM_COURSES = 40

class Course:
    # Fields
    def __init__(self, n, s):
        self.name = n
        self.students = s

    # Methods
    def size(self):
        return len(self.students)

    def age_distribution(self):
        counts = {"3": 0, "4": 0, "5": 0}
        for s in self.students:
            counts[s.form] += 1
        return counts

    def isValid(self):
        # for key, val in self.age_distribution().items():
        #     if val < 4:
        #         return False
        if self.size() < 6 or self.size() > 16:
            return False
        return True

    def disparity(self):
        # Disparity is a measurement of the difference between the ideal class
        # size and the current class size

        # If the class is too big, disparity is positive
        if self.size() >= MAX_CLASS_SIZE:
            return self.size() - MAX_CLASS_SIZE

        # If the class is too small, disparity is negative
        else:
            return self.size() - MIN_CLASS_SIZE

    def distribution(self):
        a = [0, 0, 0]

        for x in self.students:
            if x.form == 3:
                a[0]++
            elif x.form == 4:
                a[1]++
            else:
                a[2]++
