"""
Project 6
Canvas Analyzer
CS 1064 Introduction to Programming in Python
Spring 2018

Access the Canvas Learning Management System and process learning analytics.

Edit this file to implement the project.
To test your current solution, run the `test_my_solution.py` file.
Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: Charles Kelley
"""
__version__ = 7
#import statements for this project including all nessesities
import canvas_requests as crs
import matplotlib.pyplot as plt
import datetime as dte

# 1) main
def main(userName):
    #get student file from canvas requests
    studentFile = crs.get_user(userName)
    #print information to display
    print_user_info(studentFile)
    #filter available current classes for user
    filteredCourses = filter_available_courses(crs.get_courses(userName))
    #print filtered courses
    print_courses(filteredCourses)
    #get id numbers for courses
    courseIDS = get_course_ids(filteredCourses)
    #loop for user to choose a valid id
    chosenCourse = choose_course(courseIDS)
    #get submissions to choosen course
    submissions = crs.get_submissions(userName, chosenCourse)
    #get current grade of course
    summarize_points(submissions)
    #catagorize grades by group
    summarize_groups(submissions)
    #plot data for distribution of grade and trend over the semester
    plot_scores(submissions)
    plot_grade_trends(submissions)
    
# 2) print_user_info
def print_user_info(userDict):
    print("Name : " + userDict["name"])
    print("Title : " + userDict["title"])
    print("Primary Email : " + userDict["primary_email"])
    print("Bio : " + userDict["bio"])
# 3) filter_available_courses
def filter_available_courses(userList):
    availableCourses = []
    #loops through all courses
    for course in userList:
        #checks if class is available
        if course["workflow_state"] == 'available':
            #add to course list of available courses
            availableCourses.append(course)
    return availableCourses
# 4) print_courses
def print_courses(courseList):
    #loops through available course list and prints each course with its ID
    for course in courseList:
        print(str(course["id"]) + " : " + course["name"])
# 5) get_course_ids
def get_course_ids(courseList):
    courseIDS = []
    #loops and adds all course IDs to on elist
    for course in courseList:
        courseIDS.append(course["id"])
    return courseIDS
# 6) choose_course
def choose_course(integerList):
    userInput = "0"
    #while loop cycles until a ID is entered that is in the list of given course IDs
    while (int(userInput) not in integerList):
        userInput = input("input a valid course ID: ")
    #returns user entered ID
    return int(userInput)
# 7) summarize_points
def summarize_points(submissionList):
    pointsPossible= 0
    pointsObtained = 0
    #loops and sums scores and possible scores for every submission
    for submission in submissionList:
        #check if submission is graded
        if (submission["score"] != None):
            weight = submission["assignment"]["group"]["group_weight"]
            pointsPossible = pointsPossible + (submission["assignment"]["points_possible"] * weight)
            pointsObtained = pointsObtained + (int(submission["score"]) * weight)
    #find current grade (score / possible score)
    currentGrade = round((pointsObtained / pointsPossible) * 100)
    #print data
    print("Points possible so far: " + str(pointsPossible))
    print("Points obtained: " + str(pointsObtained))
    print("Current Grade: " + str(currentGrade))
# 8) summarize_groups
def summarize_groups(submissionList):
    #creates dictionaries to sum points for specific groups
    groupPointsPossible = {}
    groupPointsObtained = {}
    groupNames = []
    groupGrades = {}
    #loops through all submissions
    for submission in submissionList:
        #checks if submission has a grade
        if (submission["score"] != None):
            #adds group to dictionaries if it is missing
            if submission["assignment"]["group"]["name"] not in groupPointsPossible:
                groupPointsPossible[ submission["assignment"]["group"]["name"]] = 0
                groupPointsObtained[ submission["assignment"]["group"]["name"]] = 0
                #list of group names
                groupNames.append(submission["assignment"]["group"]["name"])
            #adds points possible
            groupPointsPossible[submission["assignment"]["group"]["name"]] += submission["assignment"]["points_possible"]
            #checks if submission has a score
            if (submission["score"] != None):
                groupPointsObtained[submission["assignment"]["group"]["name"]] += submission["score"]
    #calculates grade for each group
    for name in groupNames:
        grade = round((groupPointsObtained[name] / groupPointsPossible[name] ) * 100)
        groupGrades[name] = grade
    for group, grade in groupGrades.items():
        print("* " + group + " : " + str(grade))
        
# 9) plot_scores
def plot_scores(submissionList):
    grades = []
    #loops and finds grade for each group and adds to list to be plotted
    for submission in submissionList:
        if ((submission["score"] != None) and (submission["assignment"]["points_possible"])):
            score = (submission["score"] / submission["assignment"]["points_possible"]) * 100
            grades.append(score)
            
    #plots all data on a hstogram and labels all data
    plt.hist(grades)
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.title("Distribution of Grades")
    plt.show()
    
# 10) plot_grade_trends
def plot_grade_trends(submissionList):
    #initalize lists to hold scores for each assignment (max, highest, lowest)
    Maximum = []
    Lowest = []
    Highest = []
    #loops and calculates points for each of three lists
    for submission in submissionList:
        weight = submission["assignment"]["group"]["group_weight"]
        Maximum.append(100 * submission["assignment"]["points_possible"] * weight)
        if (submission["workflow_state"] == "graded"):
            Highest.append(100 * submission["score"] * weight)
            Lowest.append(100 * submission["score"] * weight)
        else:
            Highest.append(100 * submission["assignment"]["points_possible"] * weight)
            Lowest.append(0)
        #initalize lists for running sums
    Max_running_sum = 0
    Max_running_sums = []
    High_running_sum = 0
    High_running_sums = []
    Low_running_sum = 0
    Low_running_sums = []
    #running sum of maximum course grade
    for item in Maximum:
        Max_running_sum += item
        Max_running_sums.append(Max_running_sum)
    #max points for course
    maxPoints = Max_running_sum / 100
    #list to add course maximum as a percentge
    final_Max_running_sums = []
    for item in Max_running_sums:
        final_Max_running_sums.append(item / maxPoints)
    #running sum for lowest possible grade through out semster as a percentage
    for item in Lowest:
        Low_running_sum += item
        Low_running_sums.append(Low_running_sum / maxPoints)
    #running sum for highest possible grade through out semster as a percentage
    for item in Highest:
        High_running_sum += item
        High_running_sums.append(High_running_sum / maxPoints)
        
    #data for dates throughout the semester        
    dates = []
    for submission in submissionList:
        string_date = submission["assignment"]["due_at"]
        due_at = dte.datetime.strptime(string_date, "%Y-%m-%dT%H:%M:%SZ")
        dates.append(due_at)
        
    #plots all three lines to map trend in graed over the semster        
    plt.plot(dates, final_Max_running_sums, label="Maximum")
    plt.plot(dates, High_running_sums, label="Highest")
    plt.plot(dates, Low_running_sums, label="Lowest")
    plt.legend()
    plt.ylabel("Grade")
    plt.title("Grade Trend")
    plt.show()
    
    
    
# Keep any function tests inside this IF statement to ensure
# that your `test_my_solution.py` does not execute it.
if __name__ == "__main__":
    main('hermione')
    # main('ron')
    # main('harry')
    
    # https://community.canvaslms.com/docs/DOC-10806-4214724194
    # main('YOUR OWN CANVAS TOKEN (You know, if you want)')