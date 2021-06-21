class Course:
    # Fields
    def __init__(self, n, s):
        self.name = n
        self.students = s

    # Methods
    def size():
        return len(students)

    def age_distribution():
        counts = {"3": 0, "4": 0, "5": 0}
        for s in students:
            counts[s.form] += 1
        return counts

    def isValid():
        for key, val in self.age_distribution():
            if val < 4:
                return False
        if self.size < 6 or self.size > 16:
            return False
        return True
