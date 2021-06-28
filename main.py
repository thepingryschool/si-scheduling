# TODO LIST:
# - pre script to make sure all of the courses have at least 6 signups
# - course-specific student limits? (build into object-oriented stuff)
# - limiting courses based on grade level?
# - prioritize the course running over student getting top priority
# - more test data? randomness component? satisfaction score?

# Pandas, of course
import pandas as pd

# Libraries for interacting with the google sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Python libraries
import random
import csv
from operator import attrgetter
import numpy as np

# Import student and course classes
from Student import Student
from Course import Course, MAX_CLASS_SIZE, MIN_CLASS_SIZE

# CONST for how many students should be in each class per form
# Other class related consts can be found in ./Course.py
STUDENTS_PER_FORM = 2

# List of all available classes as Course objects
CLASSES = []

# List of all students that signed up on Google Sheets as Student objects
STUDENTS = []


def get_sheet_data(sheet_number):
    # Use OAUTH2 and Google API client to authorize the application with gspread
    # gspread is a pip library for interacting with the google sheets API
    # Learn more about the Google API client here: https://developers.google.com/sheets/api
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    client = gspread.authorize(creds)

    # Open the sheet and read data using gspread library
    sheet = client.open("Spring Intensive Signup (Responses)").get_worksheet(sheet_number)
    return sheet.get_all_values()



def process_data():
    # Get the data from the spreadsheet using Google API
    data = get_sheet_data(5)
    course_specific_info = get_sheet_data(0)

    # Get the course names from the spreadsheet
    # Course names are stored in the first row of the spreadsheet with the format:
    # Select Your Courses! [Course Name Here]
    for cell in data[0]:
        # If the first word of the cell is "Select", it's a course
        if (cell[0:6] == "Select"):
            # Remove the surrounding parts of the course name
            className = cell[22:len(cell) - 1]

            # Set default values for the course info (used when not provided)
            id = "unknown"
            min_size = MIN_CLASS_SIZE
            max_size = MAX_CLASS_SIZE
            faculty = "unknown"

            # Loop through spreadsheet containing course specific info
            for row in course_specific_info:
                if row[0] == className:
                    faculty = row[1]
                    id = row[2]
                    min_size = row[3]
                    max_size = row[4]

            # Add class name to array
            CLASSES.append(Course(className, [], int(min_size), int(max_size), id, faculty))

    # Iterate over the rows of sheet data
    # For each student, create a Student object with the appropriate fields
    skipFirst = True

    # Loop through each registered user
    for row in data:
        # Skip the first row containing the titles
        if skipFirst:
            skipFirst = False
            continue

        # Find the preferred courses by getting the index of their choices
        # Then, get the course objects through the CLASSES array
        # Classes are ordered in the array the same way they are ordered in the data row
        coursePrefs = []
        coursePrefs.append(CLASSES[row.index("First Choice") - 1])
        coursePrefs.append(CLASSES[row.index("Second Choice") - 1])
        coursePrefs.append(CLASSES[row.index("Third Choice") - 1])
        coursePrefs.append(CLASSES[row.index("Fourth Choice") - 1])
        coursePrefs.append(CLASSES[row.index("Fifth Choice") - 1])

        # Store the users first choice
        firstChoice = CLASSES[row.index("First Choice") - 1]

        # Get the user's name, email, and form from the data
        name = row[len(row) - 3]
        form = row[len(row) - 1]
        email = row[len(row) - 2]

        # Create a new Student class object and add to list of students
        # STUDENTS ARE INTIAILIZED WITH THEIR FIRST CHOICE AS THEIR COURSE
        s = Student(coursePrefs, firstChoice, name, email, form)
        STUDENTS.append(s)
        firstChoice.students.append(s)

    # Screen the input data. Each course must have at least 6 signups. If not, it
    # is emptied and its students are relocated to other courses.
    prescreen()

# Method to screen every class before processing preferences. If the class has
# less than 6 signups, it is removed from the courses list and its students are
# relocated to other classes.
def prescreen():
    # Dictionary to count the number of students in each course
    count = {}

    # Loop through each course, initializing dict
    for course in CLASSES:
        count[course.name] = 0

    # Loop through each student's preferences
    for s in STUDENTS:
        for p in s.preferences:
            count[p.name] += 1

    # Check if any course has less than six signups overall
    # Move all students in those problem courses to the next viable course
    for key,val in count.items():
        if val < 6:
            for c in CLASSES:
                if c.name == key:
                    # Courses are deemed unfixable if they have less than 6 signups
                    c.fixable = False

                    # Loop through all students in the course and relocate them to 2nd choice
                    for s in c.students:
                        pref_index = 0
                        while (pref_index < 5):
                            if s.preferences[pref_index].fixable == True:
                                move_student(s, s.preferences[pref_index])
                                pref_index = 5
                            pref_index += 1

# There are three steps in the assignment process:
# 1) Assign each student their top choice (initialized)
# 2) Determine which classes are problematic and which aren't
#       - Only working with the problem classes from now on
# 3) Determine whether the problem class has a surplus or a shortage
#       - Surplus --> push student to their next lowest choice class available
#           without ruining the grade distribution
#       - Shortage --> pull student with problem class in their preferences
#           and remedy grade distribution.
def assign():
    # Find the courses with problems
    bad_courses = [c for c in CLASSES if not c.isValid() and c.fixable]

    # Sort problematic courses based on size
    bad_courses.sort(key=lambda x: len(x.students))

    for course in bad_courses:
        # Sort students based on their form (ascending, youngest first)
        # Sorting guarantees that later down the line, moving students around
        # begins with underclassmen, therefore ensuring upperclassmen priority
        # and is ultimately more efficient because younger students are more
        # likely to be moved.
        sortedStudents = sorted(course.students, key=attrgetter('form'))

        # Disparity is positive when surplus, negative when shortage.
        #       If surplus (disparity positive) --> remove a student.
        #       If shortage (disparity negative) --> add a student.
        # See definition in Course.py for more info.

        # Calculate the disparity for the current course
        disparity = course.disparity()

        # Calculate the distribution for the current course
        # e.g. [3,3,3] means 3 frosh, 3 soph, 3 junior
        dist = course.distribution()

        # Keep looping until the current course's problems are resolved
        while (abs(disparity) > 0 or min(dist) < 2) and course.fixable:
            # Distribution is okay, but we have a surplus.
            # So, put a student in a class they prefer without ruining distribution.
            if min(dist) > 1 and disparity > 0:
                # Determine which form should be moved out. Four seats in each
                # class are reserved for freshmen and another four for sophomores,
                # We model using a stack. Freshmen are top priority to move (because upperclassmen priority),
                # but if too few freshman, we look for sophomores, etc.
                form_to_move = [3]

                if dist[0] <= 0.25* course.max_size: #4:
                    form_to_move.append(4)
                if dist[1] <= 0.25* course.max_size:
                    form_to_move.append(5)

                while len(form_to_move) != 0:

                    current_pref_index = 0
                    found = False

                    # Loop through all students' first choice, then second, and so on
                    while current_pref_index < 5 and not found:
                        # Course 19 [4, 5, 9]
                        # Check all students in the problem class, *starting with youngest*
                        for s in sortedStudents:
                            # Check that the student is in the correct form and check
                            # the students preferred course to see if it has space for them
                            candidate = s.preferences[current_pref_index]

                            if (dist[form_to_move[-1] - 3] > 2 and \
                                    s.form == str(form_to_move[-1]) and \
                                    candidate.name != s.course.name and \
                                    candidate.size() + 1 <= candidate.max_size and \
                                    candidate.fixable == True ):

                                # Terminate the loops surrounding this block
                                found = True
                                form_to_move = []

                                # Remove from the list of sorted students
                                sortedStudents.remove(s)

                                # Move the student
                                move_student(s, candidate)
                                break

                        # If nothing can be founda t teh current preference level,
                        # move to the next one.
                        current_pref_index += 1

                    # If we couldn't find a student in the desired form with the right preference
                    # we pop from the stack and look to the next best form
                    if (len(form_to_move) != 0):
                        form_to_move.pop()

            # Distribution is incorrect, so we need to take a form-specific student
            # from another class, remedying the distribution problem. If this extra
            # student creates a surplus, it will be resolved in the next iteration
            # of the outmost while loop.
            elif min(dist) < 2:
                # Figure out which form needs fixing in the class
                gradeIndex = dist.index(min(dist))

                # If we fail to take a student from the specific grade,
                # we lower our standard and take ANY student who has
                # this course preference
                if not take_student(course, gradeIndex + 3):
                    # Flag the class as not fixable if we again fail
                    course.fixable = take_student(course)

            # Re-calculate disparity and distribution after changes
            disparity = course.disparity()
            dist = course.distribution()

# Take any student with the given course in their preferences
# Returns True if student is found, False if otherwise
def take_student(course, form = 1):
    # Current preference index
    pref_index = 0

    # Loop through every students first index, then their second index, so on
    while pref_index < 5:
        for student in STUDENTS:
            # Check that the student has the course in their preferences, is
            # not already in that class, and that new and old classes have space.
            if student.preferences[pref_index] == course \
                    and student.course != course \
                    and student.course.size() > student.course.min_size \
                    and student.preferences[pref_index].size() + 1 < student.preferences[pref_index].max_size:
                # If a user specifies a form, thne check the form too.
                # Otherwise, as soon as there is a match, return it.
                if form == 1 or student.form == str(form):
                    move_student(student, course)
                    return True

        pref_index += 1

    # Return false if nothing valid is found
    return False

# Simple utility method, moves a student from one course to another
# NOTE: assumes that the student is already enrolled in old_class
def move_student(student, new_class):
    old_class = student.course
    old_class.students.remove(student)
    new_class.students.append(student)
    student.course = new_class

# Convert course to a Veracross formatted class enrollment CSV
# Find more information in the README file.
def courses_to_csv():
    # Open the .csv file and utilize python csv package
    f = open('class_roster.csv', 'w')
    writer = csv.writer(f)

    # Title row of the csv file
    first_row = ["veracross_class_id", "class_id", "school_year",
                 "veracross_student_id", "enrollment_level_id"]
    writer.writerow(first_row)

    # For each student, create a new row with course and student info
    for s in STUDENTS:
        new_row = [s.course.id, s.course.name, "2021-22", s.email, s.form]
        writer.writerow(new_row)

    f.close()

# Pushes course enrollment data to spreadsheet.
# Makes two worksheets: one in Veracross format, one in a more visually appealing way
def courses_to_spreadsheet():
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'client_secret.json', scope)
        client = gspread.authorize(creds)
        roster1 = client.open("Spring Intensive Signup (Responses)").get_worksheet(2)
        big = [["Course", "Faculty", "size / max", "fixable?", "Students"]]
        for c in CLASSES:
            big.append(c.toList())
        roster1.update('A1', big)

        roster2 = client.open("Spring Intensive Signup (Responses)").get_worksheet(3)
        big2 = []
        big2.append(["Name", "Course Assigned", "Cost"])
        sortedStudents = sorted(STUDENTS, key= Student.cost , reverse=True)
        for s in sortedStudents:
            big2.append(s.toList())

        roster2.update('A1', big2)

        roster3 = client.open("Spring Intensive Signup (Responses)").get_worksheet(4)
        big3 = []
        big3.append(["veracross_class_id", "class_id", "school_year",
                     "veracross_student_id", "enrollment_level_id"])
        for s in STUDENTS:
            big3.append([s.course.id, s.course.name, "2021-22", s.email, s.form])
        roster3.update('A1', big3)






# Debugging method, shows Classes and Students
def debug_print_vars():
    print("\nCLASS ENROLLMENTS: " + str(len(STUDENTS)) + " students, " + str(len(CLASSES)) + " courses. \n")
    sumcost = 0
    for x in CLASSES:
        if not x.fixable:
            print("[UNFIXABLE]\t", end="")
        else:
            print("           \t", end="")
        print(f"{x.name}: {str(x.size())} / {str(x.max_size)} --> Cost: {str(x.cost())}")
        sumcost += x.cost()
    print("\n")
    print("           \tTOTAL COST: " + str(sumcost))
    print("\n")



# Utility method to print the analytics of our scheduling.
def print_analytics():
    total_pref = 0
    num_students = len(STUDENTS)

    total_clength = 0
    num_courses = len(CLASSES)

    for student in STUDENTS:
        total_pref = student.preferences.index(student.course) + 1

    for course in CLASSES:
        total_clength += course.size()

    print("AVERAGE PREFERENCE LEVEL: " + str(total_pref / num_students + 1))
    print("AVERAGE COURSE SIZE: " + str(total_clength / num_courses))

    print()


def main():
    process_data()
    assign()
    courses_to_csv()
    courses_to_spreadsheet()
    debug_print_vars()
    print_analytics()

main()
