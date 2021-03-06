"""

This class represents a single student with the following fields.

Preferences: list of the 5 courses the student selected
Course: current course they are assigned
Name: first and last name of the student
Email: Pingry email address of the student
Form: grade level of the student (9th --> 3, 10th --> 4, etc.)

"""
class Student:
    # Fields
    def __init__(self, p, c, n, e, f):
        self.preferences = p
        self.course = c
        self.name = n
        self.email = e
        self.form = f

    # Calculates how far a student's assignment is from top choice
    def cost(self):
        return self.preferences.index(self.course)

    def toList(self):
        return [self.name, self.course.name, self.cost()]
