import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

MAX_CLASS_SIZE = 16
MIN_CLASS_SIZE = 6
NUM_COURSES = 40

# List of all available classes
# EXAMPLE: CLASSES = ["class1", "class2", ...]
CLASSES = []

# List of student in each form
# EXAMPLE {3: ["johndoe1@pingry.org", ...], 4: ...}
FORMS = {"3":[], "4":[], "5":[], "6":[]}

# Store the preferences of each student in a dictionary
# Ordered array containing preferences from 1-5
# EXAMPLE: preferences: ["student3": ["class4", "class2", "class3", "class1", "class6"], ...]
preferences = {}

# NOTE: Yes, class_assignments and student_assignments hold the same information, just in different ways.
# class_assignments: ["class1": ["student2", "student5", ...], ...]
class_assignments = {}

# student_assignments: ["student1":"class5", ...]
student_assignments = {}

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
    #       Select Your Courses! [Course Name Here]
    for x in range(0, len(data[0])):
        # If the first word of the cell is "Select", it's a course
        if (data[0][x][0:6] == "Select"):
            # Remove the surrounding parts of the course name
            className = data[0][x][22:len(data[0][x]) - 1]

            # Add class name to array
            CLASSES.append(className)

    # Iterate over the rows of sheet data
    # For each student, do two things:
    # 1) Create an entry in preferences with their course selections
    # 2) Put their form into the static FORMS data
    skipFirst = True

    for row in data:
        # Skip the first row containing the titles
        if skipFirst:
            skipFirst = False
            continue

        # Find the preferred courses by getting the index of their choices
        # Then, get the course names through the CLASSES array
        # Classes are ordered in the array the same way they are ordered in the data row
        coursePrefs = []
        coursePrefs.append(CLASSES[row.index("First Choice") - 1])
        coursePrefs.append(CLASSES[row.index("Second Choice") - 1])
        coursePrefs.append(CLASSES[row.index("Third Choice") - 1])
        coursePrefs.append(CLASSES[row.index("Fourth Choice") - 1])
        coursePrefs.append(CLASSES[row.index("Fifth Choice") - 1])

        # Add the course preferences to the preferences
        preferences[row[len(row) - 2]] = coursePrefs

        # Add the student's email to the forms
        FORMS[row[len(row) - 1]].append(row[len(row) - 2])

# Calculates the strength of a given scheduling arrangment
#    based on how well it satisfies each student's preferences
# NOTE: assumes student has been assigned a top-five preferred class
def utility(preferences, student_assignments):
    u = 0
    for student,class in student_assignments.items():
        u += preferences[student].index(class)
    return u

# There are three steps in the assignment process:
# 1) Assign each student their top choice
# 2) Balance class age distributions
# 3) Fix outstanding class size issues
# Fixes will be made MAXIMIZE overall utility and GUARANTEE upperclassmen

# assign top Choice
# classes that don't have issues --> REMOVE!
# each class that has an issue --> FIX
#   find out if we can jill two birds with one stone
def assign(preferences):
    # Step 1
    student_assignments = [val[0] for key,val in preferences.items()]
    class_assignments = make_class_assignments()

    # Step 2
    # find classes that have too many or too few
    # collect those students who don't fit
    for class, students in class_assignments.items():
        if len(class) > MAX_CLASS_SIZE or len(class) < MIN_CLASS_SIZE:


    return class_assignments


# Quick conversion from the student assignments structure
def make_class_assignments():
    class_assignments = {}
    for class in CLASSES:
        class_assignments[class] = [val for key,val in student_assignments.items() if key == class]
    return class_assignments

def check_valid_class():
    pass

def main():
    process_data()
