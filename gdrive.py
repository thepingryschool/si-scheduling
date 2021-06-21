import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Spring Intensive Signup (Responses)").sheet1
data = sheet.get_all_values()

CLASSES = []
FORMS = {"3":[], "4":[], "5":[], "6":[]}


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

preferences = {}
skipFirst = True

for row in data:
    if skipFirst:
        skipFirst = False
        continue

    coursePrefs = []
    coursePrefs.append(CLASSES[row.index("First Choice") - 1])
    coursePrefs.append(CLASSES[row.index("Second Choice") - 1])
    coursePrefs.append(CLASSES[row.index("Third Choice") - 1])
    coursePrefs.append(CLASSES[row.index("Fourth Choice") - 1])
    coursePrefs.append(CLASSES[row.index("Fifth Choice") - 1])

    preferences[row[len(row) - 2]] = coursePrefs

    FORMS[row[len(row) - 1]].append(row[len(row) - 2])



print (preferences)
print (FORMS)
