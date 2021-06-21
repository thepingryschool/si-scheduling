import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from Student import Student
from Course import Course

# Consts
MAX_CLASS_SIZE = 16
MIN_CLASS_SIZE = 6
NUM_COURSES = 40

# List of all available classes as Course objects
CLASSES = []

# List of all students that signed up on Google Sheets as Student objects
STUDENTS = []

def get_sheet_data():
    # Use OAUTH2 and Google API client to authorize the application with gspread
    # gspread is a pip library for interacting with the google sheets API
    # Learn more about the Google API client here: https://developers.google.com/sheets/api
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
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
    # For each student, do two things:
    # 1) Create an entry in preferences with their course selections
    # 2) Put their form into the static FORMS data
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

# Calculates the strength of a given scheduling arrangment
#    based on how well it satisfies each student's preferences
# NOTE: assumes student has been assigned a top-five preferred class
def utility():
    u = 0
    for s in STUDENTS:
        u += s.utility()
    return u

# There are three steps in the assignment process:
# 1) Assign each student their top choice
# 2) Balance class age distributions
# 3) Fix outstanding class size issues
# Fixes will be made MAXIMIZE overall utility and GUARANTEE upperclassmen priority

# assign top Choice
# classes that don't have issues --> REMOVE!
# each class that has an issue --> FIX
#   find out if we can jill two birds with one stone
def assign():
    bad_courses = [c for c in COURSES if !c.isValid()]
    for i in range(len(bad_courses)):
        for j in range(len(bad_course)):
            if i != j:


    # Step 1
    #student_assignments = [val[0] for key,val in preferences.items()]
    #class_assignments = make_class_assignments()


    # Step 2
    # find classes that have too many or too few
    # collect those students who don't fit
    # for class, students in class_assignments.items():
    #     if len(class) > MAX_CLASS_SIZE or len(class) < MIN_CLASS_SIZE:


def debug_print_vars():
    print("CLASSES")
    for x in CLASSES:
        print(x.name + ": ", end='')
        for student in x.students:
            print(student, end=", ")
    print("\n\n")

    print ("STUDENTS")
    for y in STUDENTS:
        print(y.name + ", " + y.course.name + ", " + y.email)

    print("\n\n")

    print("FORMS")
    print(FORMS)
    print("\n\n")

    print("PREFERENCES")
    print(preferences)
    print("\n\n")

    print("STUDENT ASSIGNMENTS")
    print(student_assignments)
    print("\n\n")

    print("CLASS ASSIGNMENTS")
    print(class_assignments)
    print("\n\n")

def main():
    process_data()
    assign()
    debug_print_vars()

main()
