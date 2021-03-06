# Spring Intensive Scheduling Program

Starting in the spring of 2022, The Pingry School will be implementing two-week intensive courses in place of final exams.
There will be around 40 courses in a variety of subjects for the ~420 freshmen, sophomores, and juniors (seniors will still
be doing Independent Senior Projects, or ISPs, at this time). Students will sign up for their courses through a Google Form,
in which they will be asked to identify their top 5 choices.

This code (implemented in Python) takes in the course preferences of students and certain course-specific information (as .csv) and outputs course rosters (as .csv in the Veracross [Class Enrollment Import Type](https://learn.veracross.com/docs/class-enrollment-import-type#uploading-the-data "Class Enrollment Import Type")). We also output statistics regarding the cost (the sum of how far each student is from their top preference), the average preference level of assigned courses, and the average course size.

INSTRUCTIONS FOR USER: 
1) Navigate to this [folder](https://drive.google.com/drive/folders/1a6nPndI_uVMxW75Ub5PmGNAaQQOcO7X5) which contains both the form and the spreadsheet
2) Send out "Spring Intensive Signup" Google Form to target audience, fully collect results.
3) Go to the "Course Data" tab. This is where you will input information about each course's name, teachers, Veracross Course ID, and size requirements. Also see the column which asks for the number of schedules and a parameter called "alpha." This alpha parameter, which goes from 0 to 1, is supposed to indicate how much age preference should matter when choosing who should be moved out of their top choice class. Alpha = 1 means age takes full priority over course preference; alpha = 0 means all ages are treated the same. An inputted alpha outside the range of 0 and 1 will indicate the desire to use full priority for age. In any case, list as many alphas as the number of schedules you indicate.
4) Download the si-scheduling package to your computer. If on Mac, go to terminal and type: <br />
```
cd path/to/package
python main.py real
```
NOTE: if you don't include the "real" command-line argument, you will be <br />
5) Check the folder for results. Will include the same information in three formats: course rosters, students sorted by satisfaction, and the Veracross course-enrollment csv format. 


Here are the parameters for class rosters:
1) Each class should meet their specific minimum and maximum signup requirements (for most classes, these numbers are 6 and 16, respectively).
2) Each class should have at least two of each form (freshmen = Form III, sophomores = Form IV, juniors = Form V).
3) Older students have a higher priority in choosing classes??????but, you must hold four seats for freshmen and sophomores.

Our general approach is as follows:
1) Assign each student to their top choice class
2) Identify "problem classes" which have either shortages or surpluses in signups. <br />
  a) If shortage --> figure out which form the course is lacking --> locate a student from this form who has the course in their preferences <br />
  b) If surplus --> move out the youngest student to their next preference class that doesn't have a surplus
3) Run through all problem classes until they are fixed

NOTE: Sometimes, course preferences are very skewed or classes don't have enough signups to fill requirements. In these cases, where a class cannot be made to meet requirements, it is flagged as "unfixable" and exported regardless. This is an issue that should be fixed by a veracross admin.


