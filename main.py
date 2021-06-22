import pandas as pd
import gspread
from operator import attrgetter
from oauth2client.service_account import ServiceAccountCredentials
from Student import Student
from Course import Course


# List of all available classes as Course objects
CLASSES = []

# List of all students that signed up on Google Sheets as Student objects
STUDENTS = []


def get_sheet_data():
    # Use OAUTH2 and Google API client to authorize the application with gspread
    # gspread is a pip library for interacting with the google sheets API
    # Learn more about the Google API client here: https://developers.google.com/sheets/api
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    client = gspread.authorize(creds)

    # Open the sheet and read data using gspread library
    sheet = client.open("Spring Intensive Signup (Responses)").sheet1
    return sheet.get_all_values()


def process_data():
    # Get the data from the API
    data = get_sheet_data()

    # Get the course names from the spreadsheet
    # Course names are stored in the first row of the spreadsheet with the format:
    # Select Your Courses! [Course Name Here]
    for cell in data[0]:
        # If the first word of the cell is "Select", it's a course
        if (cell[0:6] == "Select"):
            # Remove the surrounding parts of the course name
            className = cell[22:len(cell) - 1]

            # Add class name to array
            CLASSES.append(Course(className, []))

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

# Calculates the strength of a given scheduling arrangment
#    based on how well it satisfies each student's preferences
# NOTE: assumes student has been assigned a top-five preferred class
# I dont htink we need this


def utility():
    u = 0
    for s in STUDENTS:
        u += s.utility()
    return u

# There are three steps in the assignment process:
# 1) Assign each student their top choice (initialized)
# 2) Determine which classes are problematic and which aren't
#       - Only working with the problem classes from now on
# 3) Iterate through classes --> move random (starting with underclassmen)
#        to their second choice class.
# 4) Check whether all issues are resolved, and if not, keep looping


def assign():
    # Find the courses with problems
    bad_courses = [c for c in CLASSES if not c.isValid()]

    # Sort problematic courses based on size
    bad_courses.sort(key=lambda x : len(x.students))

    # for x in bad_courses:
    #     print(x.name + ": " + str(x.size())

    for course in bad_courses:
        # Sort students based on their form (ascending)
        sortedStudents = sorted(course.students, key=attrgetter('form'))

        # Disparity is positive when surplus, negative when shortage
        #   if surplus (disparity positive) --> remove a student
        #   if shortage (disparity negative) --> add a student

        # Calculate the disparity for the current course
        disparity = course.disparity()
        dist = course.distribution() # --> for example, [3,3,3] means 3 frosh, 3 soph, 3 junior

        while abs(disparity) > 0 and min(dist) > 1:
            # Surplus in the class
            if disparity > 0:
                # pushing out the youngest student to the smallest bad class
                move_student(sortedStudents[0], bad_courses[0])

            # Shortage in the class
            elif disparity < 0:
                # pulling the youngest student from the biggest class
                topSorted = sorted(bad_courses[-1].students, key=attrgetter('form'))
                move_student(topSorted[0], course)

            if min(dist) < 2

            # Re-sort courses and students
            bad_courses.sort(key=lambda x : len(x.students))
            sortedStudents = sorted(course.students, key=attrgetter('form'))

            # Re-calculate disparity
            disparity = course.disparity()

    for x in CLASSES:
        print(x.name + ": " + str(x.size()))

# Simple utility method, moves a student from one course to another
# NOTE: assumes that the student is already enrolled in old_class

def move_student(student, new_class):
    print("old", student.course.name)
    old_class = student.course
    old_class.students.remove(student)
    new_class.students.append(student)
    student.course = new_class
    print("new",student.course.name)

# Debugging method, shows Classes and Students


def debug_print_vars():
    print("CLASSES")
    for x in CLASSES:
        print(x.name + ": ", end='')
        for student in x.students:
            print(student, end=", ")
        print()
    print("\n\n")

    print("STUDENTS")
    for y in STUDENTS:
        print(y.name + ", " + y.course.name + ", " + y.email)

    print("\n\n")


def main():
    process_data()
    # debug_print_vars()
    assign()


main()
