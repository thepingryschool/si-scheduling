# Spring Intensive Scheduling Program

Starting in the spring of 2022, The Pingry School will be implementing 2-week intensive courses in place of final exams.
There will be around 40 courses in a variety of subjects for the ~420 freshmen, sophomores, and juniors (seniors will still
be doing Independent Senior Projects, or ISPs, at this time). Students will sign up for their courses through a Google Form,
in which they will be asked to identify their top 5 choices.

This code (implemented in Python) takes in the course preferences of students (as .csv) and outputs course rosters (as .csv in the Veracross
[Class Enrollment Import Type](https://learn.veracross.com/docs/class-enrollment-import-type#uploading-the-data "Class Enrollment Import Type")).

Here are the parameters for classes:
1) Each class must have between 6 and 16 students
2) Each class must have at least two of each form (freshmen = Form III, sophomores = Form IV, juniors = Form V)
3) Older students have a higher priority in choosing classes

Our general approach is as follows:
1) Assign each student their top choice
2) Identify "problem classes" which have either shortages or surpluses.
  a) If shortage --> figure out which age student you need most --> locate this student who has the course in their preferences
  b) If surplus --> move youngest student to their next preference class that doesn't have a surplus
3) Run through all problem classes until they are fixed

NOTE: Sometimes, course preferences are skewed, and classes don't have enough signups to fill requirements. In this case, the classes are flagged
as "unfixable" and exported regardless -- they can be later fixed by a veracross admin.
