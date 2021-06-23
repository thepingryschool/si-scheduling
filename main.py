import pandas as pd
import gspread
import random
from operator import attrgetter
from oauth2client.service_account import ServiceAccountCredentials
from Student import Student
from Course import Course, MAX_CLASS_SIZE

STUDENTS_PER_FORM = 2

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
    bad_courses.sort(key=lambda x: len(x.students))

    print("BEFORE")
    for x in bad_courses:
        print(x.name + ": " + str(x.size()) + " --> ", end="")
        print(x.distribution())
    print()

    for course in bad_courses:
        print(course.name + "NAME")

        # Sort students based on their form (ascending)
        # Sorting guarantees that later down the line, moving students around
        # begins with underclassmen, therefore ensuring upperclassmen priority
        sortedStudents = sorted(course.students, key=attrgetter('form'))

        # Disparity is positive when surplus, negative when shortage
        #       if surplus (disparity positive) --> remove a student
        #       if shortage (disparity negative) --> add a student
        # See definition in Course.py for more info.

        # Calculate the disparity for the current course
        disparity = course.disparity()

        # Calculate the distribution for the current course
        # e.g. [3,3,3] means 3 frosh, 3 soph, 3 junior
        dist = course.distribution()

        # Keep looping until the current course's problems are resolved
        while abs(disparity) > 0 or min(dist) < 2:
            print("dist" + str(dist))
            print(disparity)

            # Distribution is good, but we have a surplus.
            # So, put a young student in a class they prefer.
            if min(dist) > 1 and disparity > 0:
                # Check all students in the problem class, *starting with youngest*
                for s in sortedStudents:
                    # Ensure distribution remains valid (convert form to index)
                    if dist[int(s.form) - 3] > 2:
                        # Find one of the user's preferences that has room for
                        # the new student. If no preferences have room, continue
                        # to the next youngest student in the problem course
                        valid_pref_index = -1

                        for i, pref in enumerate(s.preferences):
                            if pref.size() + 1 < MAX_CLASS_SIZE:
                                valid_pref_index = i
                                break

                        if valid_pref_index != -1:
                            move_student(s, s.preferences[valid_pref_index])
                            break

            # Distribution is incorrect (implying a shortage), so we need to
            # take a form-specific student from another class, remedying the
            # disparity and distribution problems at the same time.
            elif min(dist) < 2:
                print("changing bottom")
                # Figure out which form needs fixing in the class
                gradeIndex = dist.index(min(dist))

                find = False

                # Loop through all available classes
                for c in CLASSES:
                    # Ignore the current problem course and ensure that giving a
                    # student will not disrupt the distribution
                    if c is not course and c.distribution()[gradeIndex] > 2:
                        # Loop through all students in each class, first checking
                        # everyone's first preference, then their second, so on
                        valid_student_index = -1

                        found = False
                        currentIndex = 0

                        while (currentIndex < 5 and not found):

                            for i, student in enumerate(c.students):

                                # Check the form of the student and their current preference level
                                if student.form == str(gradeIndex + 3) and course == student.preferences[currentIndex]:
                                    found = True
                                    valid_student_index = i
                                    break

                            currentIndex += 1

                        # If we found a useable student index, then move the student and exit
                        # Otherwise, continue looping through classes
                        if valid_student_index != -1:
                            move_student(c.students[valid_student_index], course)
                            break

            # Re-sort students to ensure that underclassmen priority is maintained
            # as students are added/removed
            sortedStudents = sorted(course.students, key=attrgetter('form'))

            # Re-calculate disparity and distribution after changes
            disparity = course.disparity()
            dist = course.distribution()

    print("AFTER")
    for x in CLASSES:
        print(x.name + ": " + str(x.size()) + "")
        for s in x.students:
            print(s.name + " (" + s.form + ", " +
                  str(s.preferences.index(x) + 1) + ")")
        print('\n')

# Simple utility method, moves a student from one course to another
# NOTE: assumes that the student is already enrolled in old_class


def move_student(student, new_class):
    print("old", student.course.name)
    old_class = student.course
    old_class.students.remove(student)
    new_class.students.append(student)
    student.course = new_class
    print("new", student.course.name)

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
