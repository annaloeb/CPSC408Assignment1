import csv
import sqlite3

StudentDB = "StudentDB.db"
# set exit variable that will exit main menu and stop the program when set to True
exit = False

# capitalize the first letter of all inputs to make user input case-insensitive
def capitalizeFirstLetters(string):
    words = string.split()
    capitalized_words = [word.capitalize() for word in words]
    result = ' '.join(capitalized_words)
    return result

# read contents of csv file into Student table
def read_csv():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()

    with open('studentdata.csv','r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            cursor.execute("INSERT INTO Student(FirstName, LastName, GPA, Major, Address, City, State, ZipCode, MobilePhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (row[0], row[1], row[8], row[7], row[2], row[3], row[4], row[5], row[6]))
        conn.commit()
        conn.close()
    print("\n Database Initialized")

# Get user input for main menu options
def getOption():
    print("\nOptions:")
    print("1. Initialize Database")
    print("2. Display all students and their information")
    print("3. Add a Student")
    print("4. Update a Student")
    print('5. Delete a Student')
    print('6. Find a Student')
    print('7. Exit')
    option = input("Enter the option number: ")
    # make sure input is a valid menu option
    while option not in ["1", "2", "3", "4", "5", "6", "7"]:
        print("Invalid option. Please enter a number between 1 and 7.")
        option = input("Enter the option number: ")
    return option

# get user input for update menu options
def getUpdateOption():
    print("\nUpdate Options:")
    print("1. Update student's major")
    print("2. Update student's faculty advisor")
    print("3. Update student's phone number")
    print("4. Go Back")
    option = input("Enter the option number: ")
    # make sure input is a valid menu option
    while option not in ["1", "2", "3", "4"]:
        print("Invalid option. Please enter a number between 1 and 4.")
        option = input("Enter the option number: ")
    return option

# get user input for search menu options
def getSearchOption():
    print("\nSearch Options:")
    print("1. Search by Major")
    print("2. Search by GPA")
    print("3. Search by City")
    print("4. Search by State")
    print("5. Search by Advisor")
    print("6. Go Back")
    option = input("Enter the option number: ")
    # make sure input is a valid menu option
    while option not in ["1", "2", "3", "4", "5", "6"]:
        print("Invalid option. Please enter a number between 1 and 6.")
        option = input("Enter the option number: ")
    return option
def displayAllStudents():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()

    # display column values for each row in table
    for student in students:
        deleted = ""
        if student[11] == 0:
            deleted = "No"
        else:
            deleted = "yes"
        print(f"Student Name: {student[1]} {student[2]}")
        print(f"Student ID: {student[0]}")
        print(f"GPA: {student[3]}")
        print(f"Major: {student[4]}")
        print(f"Faculty Advisor: {student[5]}")
        print(f"Address: {student[6]}")
        print(f"City: {student[7]}")
        print(f"State: {student[8]}")
        print(f"Zip Code: {student[9]}")
        print(f"Phone Number: {student[10]}")
        print(f"Is Deleted?: {deleted}  \n")
    conn.close()

# ensure user input is a valid state by referencing the "States" table, return True if input matches a state in the table
def isValidState(state, cursor):
    cursor.execute("SELECT COUNT(*) FROM States WHERE StateName = ?", (state,))
    result = cursor.fetchone()
    return result[0] > 0

def addStudent():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    FirstName = capitalizeFirstLetters(input("Enter the student's first name: "))
    LastName = capitalizeFirstLetters(input("Enter the student's last name: "))
    # ensure GPA is a valid number, print error and re-prompt if not
    while True:
        GPA = input("Enter the student's GPA: ")
        try:
            GPA = float(GPA)
            if GPA > 4.0 or GPA < 0:
                print("GPA must be between 0.0 and 4.0")
            else:
                break
        except ValueError:
            print('GPA must be a valid number of the type 0.0')
    Major = capitalizeFirstLetters(input("Enter the student's major: "))
    Address = capitalizeFirstLetters(input("Enter the student's address: "))
    City = capitalizeFirstLetters(input("Enter the student's city: "))
    # ensure input is a valid state, print error and re-prompt if not
    while True:
        State = capitalizeFirstLetters(input("Enter the student's state: "))
        if isValidState(State, cursor):
            break
        else:
            print("Invalid state. Please enter a valid state name.")
    # ensure zip code is a valid number, print error and re-prompt if not
    while True:
        ZipCode = input("Enter the student's zip code: ")
        if len(ZipCode) == 5:
            break
        else:
            print("Invalid zip code. Zip code must be exactly 5 digits long.")
    MobilePhoneNumber = input("Enter the student's mobile phone number: ")

    cursor.execute("INSERT INTO Student(FirstName, LastName, GPA, Major, Address, City, State, ZipCode, MobilePhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (FirstName, LastName, GPA, Major, Address, City, State, ZipCode, MobilePhoneNumber))
    conn.commit()
    conn.close()
    print("\n New Student Record Added Successfully")

# ensure user input is a valid student id by referencing the "Student" table, return True if input matches an SID in the table
def sid_exists(sID, cursor):
    # Check if the studentID already exists in the Student table
    cursor.execute("SELECT COUNT(*) FROM Student WHERE StudentID = ?", (sID,))
    result = cursor.fetchone()
    return result[0] > 0

def updateStudentMajor():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    # ensure SID is valid
    while True:
        sID = input("Enter the Student ID of the student you would like to update: ")
        try:
            sID = int(sID)
            if sid_exists(sID, cursor):
                break
            else:
                print('Student ID must be an existing student ID.')
        except ValueError:
            print('Student ID must be a valid number.')
    newMajor = input("Enter the new Major for this student: ")
    cursor.execute(f"UPDATE Student SET Major = ? WHERE StudentID = ?", (capitalizeFirstLetters(newMajor), sID))
    conn.commit()
    conn.close()
    print("\n Major Updated Successfully")

def updateStudentAdvisor():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    # ensure SID is valid
    while True:
        sID = input("Enter the Student ID of the student you would like to update: ")
        try:
            sID = int(sID)
            if sid_exists(sID, cursor):
                break
            else:
                print('Student ID must be an existing student ID.')
        except ValueError:
            print('Student ID must be a valid number.')
    newAdvisor = input("Enter the First and Last name of the new Advisor for this student: ")
    cursor.execute(f"UPDATE Student SET FacultyAdvisor = ? WHERE StudentID = ?", (capitalizeFirstLetters(newAdvisor), sID))
    conn.commit()
    conn.close()
    print("\n Advisor Updated Successfully")

def updateStudentPhone():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    # ensure SID is valid
    while True:
        sID = input("Enter the Student ID of the student you would like to update: ")
        try:
            sID = int(sID)
            if sid_exists(sID, cursor):
                break
            else:
                print('Student ID must be an existing student ID.')
        except ValueError:
            print('Student ID must be a valid number.')
    newPhone = input("Enter the new phone number for this student: ")
    cursor.execute(f"UPDATE Student SET MobilePhoneNumber = ? WHERE StudentID = ?", (newPhone, sID))
    conn.commit()
    conn.close()
    print("\n Phone Number Updated Successfully")

def deleteStudent():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    # ensure SID is valid
    while True:
        sID = input("Enter the Student ID of the student you would like to update: ")
        try:
            sID = int(sID)
            if sid_exists(sID, cursor):
                break
            else:
                print('Student ID does not exist. Please enter a valid student ID.')
        except ValueError:
            print('Student ID does not exist. Student ID must be a valid number')
    cursor.execute(f"UPDATE Student SET isDeleted = ? WHERE StudentId = ?", (1, sID))
    conn.commit()
    conn.close()
    print("\n Student Deleted Successfully")

def searchMajor():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    major = input("Enter the Major you would like to search by: ")
    cursor.execute(f"SElECT * FROM Student WHERE Major = ?", (capitalizeFirstLetters(major),))
    students = cursor.fetchall()
    # display column values for each row in table where major = input
    for student in students:
        deleted = ""
        if student[11] == 0:
            deleted = "No"
        else:
            deleted = "yes"
        print(f"\nStudent Name: {student[1]} {student[2]}")
        print(f"Student ID: {student[0]}")
        print(f"GPA: {student[3]}")
        print(f"Major: {student[4]}")
        print(f"Faculty Advisor: {student[5]}")
        print(f"Address: {student[6]}")
        print(f"City: {student[7]}")
        print(f"State: {student[8]}")
        print(f"Zip Code: {student[9]}")
        print(f"Phone Number: {student[10]}")
        print(f"Is Deleted?: {deleted}  \n")
    conn.close()

def searchGPA():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    # ensure GPA is valid
    while True:
        GPA = input("Enter the GPA value you would like to search by: ")
        try:
            GPA = float(GPA)
            if GPA > 4.0 or GPA < 0:
                print("GPA must be between 0.0 and 4.0")
            else:
                break
        except ValueError:
            print('GPA must be a valid number of the type 0.0')
    cursor.execute(f"SElECT * FROM Student WHERE GPA = ?", (GPA,))
    students = cursor.fetchall()
    # display column values for each row in table where GPA = input
    for student in students:
        deleted = ""
        if student[11] == 0:
            deleted = "No"
        else:
            deleted = "yes"
        print(f"\nStudent Name: {student[1]} {student[2]}")
        print(f"Student ID: {student[0]}")
        print(f"GPA: {student[3]}")
        print(f"Major: {student[4]}")
        print(f"Faculty Advisor: {student[5]}")
        print(f"Address: {student[6]}")
        print(f"City: {student[7]}")
        print(f"State: {student[8]}")
        print(f"Zip Code: {student[9]}")
        print(f"Phone Number: {student[10]}")
        print(f"Is Deleted?: {deleted}  \n")
    conn.close()

def searchCity():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    city = input("Enter the City you would like to search by: ")
    cursor.execute(f"SElECT * FROM Student WHERE City = ?", (capitalizeFirstLetters(city),))
    students = cursor.fetchall()
    # display column values for each row in table where city = input
    for student in students:
        deleted = ""
        if student[11] == 0:
            deleted = "No"
        else:
            deleted = "yes"
        print(f"\nStudent Name: {student[1]} {student[2]}")
        print(f"Student ID: {student[0]}")
        print(f"GPA: {student[3]}")
        print(f"Major: {student[4]}")
        print(f"Faculty Advisor: {student[5]}")
        print(f"Address: {student[6]}")
        print(f"City: {student[7]}")
        print(f"State: {student[8]}")
        print(f"Zip Code: {student[9]}")
        print(f"Phone Number: {student[10]}")
        print(f"Is Deleted?: {deleted}  \n")
    conn.close()

def searchState():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    state = input("Enter the State you would like to search by: ")
    cursor.execute(f"SElECT * FROM Student WHERE State = ?", (capitalizeFirstLetters(state),))
    students = cursor.fetchall()
    # display column values for each row in table where state = input
    for student in students:
        deleted = ""
        if student[11] == 0:
            deleted = "No"
        else:
            deleted = "yes"
        print(f"\nStudent Name: {student[1]} {student[2]}")
        print(f"Student ID: {student[0]}")
        print(f"GPA: {student[3]}")
        print(f"Major: {student[4]}")
        print(f"Faculty Advisor: {student[5]}")
        print(f"Address: {student[6]}")
        print(f"City: {student[7]}")
        print(f"State: {student[8]}")
        print(f"Zip Code: {student[9]}")
        print(f"Phone Number: {student[10]}")
        print(f"Is Deleted?: {deleted}  \n")
    conn.close()

def searchAdvisor():
    conn = sqlite3.connect(StudentDB)
    cursor = conn.cursor()
    advisor = input("Enter the Name of the Advisor you would like to search by: ")
    cursor.execute(f"SElECT * FROM Student WHERE FacultyAdvisor = ?", (capitalizeFirstLetters(advisor),))
    students = cursor.fetchall()
    # display column values for each row in table where advisor = input
    for student in students:
        deleted = ""
        if student[11] == 0:
            deleted = "No"
        else:
            deleted = "yes"
        print(f"\nStudent Name: {student[1]} {student[2]}")
        print(f"Student ID: {student[0]}")
        print(f"GPA: {student[3]}")
        print(f"Major: {student[4]}")
        print(f"Faculty Advisor: {student[5]}")
        print(f"Address: {student[6]}")
        print(f"City: {student[7]}")
        print(f"State: {student[8]}")
        print(f"Zip Code: {student[9]}")
        print(f"Phone Number: {student[10]}")
        print(f"Is Deleted?: {deleted}  \n")
    conn.close()


# Main Menu Logic
while not exit:
    option = getOption()
    if option == "1":
        read_csv()
    elif option == "2":
        print("All Student Data: \n")
        displayAllStudents()
    elif option == "3":
        addStudent()
    elif option == "4":
        updateOption = getUpdateOption()
        while updateOption != "4":
            if updateOption == "1":
                updateStudentMajor()
            elif updateOption == "2":
                updateStudentAdvisor()
            elif updateOption == "3":
                updateStudentPhone()
            break
    elif option == "5":
        deleteStudent()
    elif option == "6":
        searchOption = getSearchOption()
        while searchOption != "6":
            if searchOption == "1":
               searchMajor()
            elif searchOption == "2":
                searchGPA()
            elif searchOption == "3":
                searchCity()
            elif searchOption == "4":
                searchState()
            elif searchOption == "5":
                searchAdvisor()
            break
    elif option == "7":
        exit = True
