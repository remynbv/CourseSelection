from tkinter import *
from itertools import combinations
from tkinter.ttk import *
import tkinter.font as tkFont

class Course:
    def __init__(self, n, t):
        self.name = n
        self.times = t

class MasterSchedule:
    def __init__(self, f, w, r):
        self.fall = f # List of Fall Course Objects
        self.winter = w # List of Winter Course Objects
        self.required = r # List of Required Course Names (strings)

def createSchedule(courses):
    """
    Creates nested list of weekly schedule given a list of courses
    
    :param courses: Course list
    """
    sch = [[], [], [], [], []] # Mon, Tue, Wed etc.
    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            for x in courses[i].times:
                for y in courses[j].times:
                    if x[0] == y[0] and not (x[2] <= y[1] or y[2] <= x[1]):
                        return False

    for i in range(len(courses)):
        name = courses[i].name
        for (day, start, end) in courses[i].times:
            sch[day-1].append((name, start, end))
            # adds tuple (name, start, end) to day of the week
    return sch

def checkFullSchedule(f, w, required):
    """
    Confirms all required classes are included and no duplicate classes exist
    
    :param f: Fall Classes
    :param w: Winter Classes
    :param required: List of required classes
    """
    #confirm sit has all required classes
    for c in required:
        check = False
        for x in f:
            if x.name == c:
                check = True
                break
        for x in w:
            if x.name == c:
                check = True
                break
        if check==False:
            return False

    fallNames = []
    winterNames = []
    for i in f: 
        fallNames.append(i.name)
    for i in w:
        winterNames.append(i.name)
    for i in fallNames:
        for j in winterNames: 
            if i==j:
                return False
    
    return True

def generateTimes(start=830, end=2230):
    """
    Generates standard limits for schedule listing
    """
    times = []
    h, m = divmod(start, 100)
    while h * 100 + m <= end:
        times.append(h * 100 + m)
        m += 30
        if m >= 60:
            h += 1
            m -= 60
    return times

def writeOneSchedule(f, c, fw:bool):
    """
    Writes schedule as string

    :param f: Schedule nested list [[], [], [], [], []]
    :param c: List of class names
    :param x: Boolean, true=fall, false=winter
    """
    # Set of times for left column of schedule
    hours = generateTimes() 
    #Set Fall or winter schedule
    if fw == True:
        master = "Fall: \n"
    else:
        master = "Winter: \n"
    # Writes all classes at top of schedule
    mm = " - "
    for cla in c:
        mm += cla.name + " - "
    master += mm + "\n"

    master += " Time |-- Monday --|-- Tuesday -|-Wednesday -|- Thursday -|-- Friday --||\n"

    # Iterates one row at a time in schedule
    for tem in hours:
        
        teem = tem
        check = False
        if len(str(teem))==3:
               check = True
        teem = str(teem)

        teem = teem[:len(teem)-2] + ":" + teem[len(teem)-2:]
        if check:
            teem = "0" + teem

        master += teem
        master+=" |"
        
        # Iterates over entire row across the week
        for day in range(5):
            found = False
            # Check each class occuring that day
            for cla in f[day]:
                if cla[1] <= tem < cla[2]: # If class overlaps with this time, add it to the string
                    clep = cla[0]
                    if len(clep)<9:
                        clep = " " + clep + " "
                    while len(clep)<9:
                        clep = "-" + clep + "-"
                    if len(clep)<10:
                        clep += "-"
                    master += "-" + clep + "-|"
                    found = True
                    break
            if not found:
                master += "------------|"
            
        master += "|\n"
    
    return master

def writeCombineSchedule(f, w, n:list):
    """
    Writes schedule as string

    :param f: Schedule nested list [[], [], [], [], []]
    :param c: List of class names
    :param x: Boolean, true=fall, false=winter
    """
    # Set of times for left column of schedule
    hours = generateTimes() 
    #Set Fall or winter schedule
    master = "Fall/Winter Schedule: \n"
    # Writes all classes at top of schedule
    mm = " - "
    for cla in n:
        mm += cla + " - "
    master += mm + "\n"

    master += " Time |-- Monday --|-- Tuesday -|-Wednesday -|- Thursday -|-- Friday --||   -   -   -   |-- Monday --|-- Tuesday -|-Wednesday -|- Thursday -|-- Friday --||\n"

    # Iterates one row at a time in schedule
    for tem in hours:
        
        teem = tem
        check = False
        if len(str(teem))==3:
               check = True
        teem = str(teem)

        teem = teem[:len(teem)-2] + ":" + teem[len(teem)-2:]
        if check:
            teem = "0" + teem

        master += teem
        master+=" |"
        
        # Iterates over entire row across the week
        for day in range(5):
            found = False
            # Check each class occuring that day
            for cla in f[day]:
                if cla[1] <= tem < cla[2]: # If class overlaps with this time, add it to the string
                    clep = cla[0]
                    if len(clep)<9:
                        clep = " " + clep + " "
                    while len(clep)<9:
                        clep = "-" + clep + "-"
                    if len(clep)<10:
                        clep += "-"
                    master += "-" + clep + "-|"
                    found = True
                    break
            if not found:
                master += "------------|"

        master += "|   -   -   -   |"

        # Do it again for winter
        for day in range(5):
            found = False
            # Check each class occuring that day
            for cla in w[day]:
                if cla[1] <= tem < cla[2]: # If class overlaps with this time, add it to the string
                    clep = cla[0]
                    if len(clep)<9:
                        clep = " " + clep + " "
                    while len(clep)<9:
                        clep = "-" + clep + "-"
                    if len(clep)<10:
                        clep += "-"
                    master += "-" + clep + "-|"
                    found = True
                    break
            if not found:
                master += "------------|"
            
        master += "|\n"
    
    return master

def makeTopLevel(root, count, st, fw, combine):
    """
    Create a new toplevel to display a schedule

    :param root: Root TopLevel
    :param count: Current window number
    :param st: Nested list of class times
    :param names: List of names of classes
    :param fw: Boolean, true if fall, false if winter
    """
    top = Toplevel()
    nem = ""
    if combine: 
        nem = "Combined"
    elif fw == True:
        nem = "Fall"
    else:
        nem = "Winter"

    top.title(nem + " Schedule #" + str(count))
    
    T = Label(top, text=st, font=tkFont.Font(family="Courier", size=9))
    T.pack()

def displayWindows(root, master, num, combine):
    """
    Calls functions to display fall and winter schedules, keeping track of the window count
    """
    count = 1
    if combine: 
        displayCombinedScheduleWindows(root, master, num, count)
    else:
        displaySingleScheduleWindows(root, master.fall, num, count, True)
        displaySingleScheduleWindows(root, master.winter, num, count, False)
    if count == 1:
        till = Toplevel()
        till.title("No Schedules Found")
        till.geometry("200x50")
        Label(till, text="No valid schedules could be created").pack()

def displaySingleScheduleWindows(root, classes, num, count, fw):
    """
    For each valid combination of classes in one term, create a schedule
    """
    for combo in combinations(classes, num):
        classNames = [c.name for c in combo]

        if len(set(classNames)) != len(classNames):
            continue
        schedule = createSchedule(combo)
        if schedule == False:
            continue
        
        scheduleString = writeOneSchedule(schedule, combo, fw)
        makeTopLevel(root, count, scheduleString, fw, False)

        count+=1

def displayCombinedScheduleWindows(root, master, num, count):
    """
    For each valid combination of classes, create a combined schedule
    """
    for fallCombo in combinations(master.fall, num):
        # Check fallCombo
        fallClassNames = [c.name for c in fallCombo]
        if len(set(fallClassNames)) != len(fallClassNames):
            continue
        fallSchedule = createSchedule(fallCombo)
        if fallSchedule == False:
            continue
        
        for winterCombo in combinations(master.winter, num):
            # Check winterCombo
            winterClassNames = [c.name for c in winterCombo]
            if len(set(winterClassNames)) != len(winterClassNames):
                continue
            winterSchedule = createSchedule(winterCombo)
            if winterSchedule == False:
                continue
            
            if checkFullSchedule(fallCombo, winterCombo, master.required):
                #scheduleString = writeOneSchedule(fallSchedule, fallCombo, True) + "\n\n" + writeOneSchedule(winterSchedule, winterCombo, False)
                allnames = fallClassNames + winterClassNames
                scheduleString = writeCombineSchedule(fallSchedule, winterSchedule, allnames)
                makeTopLevel(root, count, scheduleString, False, True)
                count+=1

def addClass(root, master, classDisplay, submitAllClassesButtonSpace, addClassButtonSpace):
    """
    Creates new toplevel to add a new class to the schedule
    """
    top = Toplevel() # Create toplevel
    top.title("Add Class")
    top.geometry("250x300")

    Label(top, text = "Class Name:").grid(row=0, sticky = W) #Name of class
    nem = Entry(top) #formerly e1
    nem.grid(row=0, padx=70, sticky = W)

    req = IntVar() #Whether it is required
    Checkbutton(top, text="Required? (combined schedules only)", variable = req).grid(row=1, sticky = W)

    fw = IntVar() #Fall or winter
    fw.set(1)
    Radiobutton(top, text = "Fall", variable = fw, value = 1).grid(row = 2, sticky=W)
    Radiobutton(top, text = "Winter", variable = fw, value = 2).grid(row = 3, sticky=W)

    txt = Message(top, text = "If a class has more than one set of time slots, please make a separate entry with the same class name").grid(row=4, sticky=W)

    cl = Course("", [])
    
    timeDisplay = StringVar() # Display of time slots
    timeDisplay.set("")

    displayTimes = Label(top, textvariable=timeDisplay)
    displayTimes.grid(row=8, sticky=W)

    addTimeSlotButton = Button(top, text = "Add Time Slot", width = 15, command=lambda: addClassTime(top, master, cl, timeDisplay, addClassButtonSpace)).grid(row=7, padx=75, sticky=W)

    finishClassButton = Button(top, text = "Submit Class", width = 20, command=lambda: submitClass(top, master, cl, nem.get(), req, fw, classDisplay, submitAllClassesButtonSpace)).grid(row=addClassButtonSpace.get(), padx=60, sticky=W)

    top.grab_set()
    top.wait_window()

def submitClass(top, master, cl, nem, req, fw, classDisplay, submitAllClassesButtonSpace):
    """
    Submits class to masterlist, deletes toplevel
    """
    if len(nem.strip())>10:
        till = Toplevel()
        till.title("Error")
        till.geometry("200x50")
        Label(till, text="Error: Name is too long").pack()
        return # Name is too long
    if len(nem.strip())==0:
        till = Toplevel()
        till.title("Error")
        till.geometry("200x50")
        Label(till, text="Error: Name cannot be empty").pack()
        return # Name cannot be empty
    cl.name = nem
    if len(cl.times)==0:
        till = Toplevel()
        till.title("Error")
        till.geometry("200x50")
        Label(till, text="Error: No time slots added").pack()
        return # No time slots added
    submitAllClassesButtonSpace.set(submitAllClassesButtonSpace.get()+1) # Push submit button down a row

    if req.get() == 1: # Add class to required list
        master.required.append(cl.name)
    if fw.get() == 1: # Add to Fall or Winter schedules
        master.fall.append(cl)
        classDisplay.set(classDisplay.get() + str(cl.name) + " " + "(Fall)") # Add to display of classlist on root toplevel
    elif fw.get()==2:
        master.winter.append(cl)
        classDisplay.set(classDisplay.get() + str(cl.name) + " " + "(Winter)")
    if req.get() == 1:
        classDisplay.set(classDisplay.get() + " (Required)")
    classDisplay.set(classDisplay.get() + "\n")
    top.destroy()
    # error-check the class then add to appropriate list

def addClassTime(top, master, cl, timeDisplay, addClassButtonSpace):
    """
    Create new toplevel to add a time slot to the current class 
    """
    tip = Toplevel()
    tip.title("Time Slot")
    tip.geometry("250x125")
            
    Label(tip, text="Day:").grid(row=0, column = 0) # Decide what day
    day = StringVar()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    dayCombo = Combobox(tip, values=days, state='readonly', textvariable = day)
    dayCombo.grid(row=0, column=1)
            
    tems = []
    for i in range(8, 22): # Create list of possible times
        tems.append(str(i)+":00")
        tems.append(str(i)+":30")
    
    Label(tip, text="Start Time:").grid(row=1, column = 0) # Decide start time
    startTime = StringVar()
    startTimeCombo = Combobox(tip, values=tems, state='readonly', textvariable = startTime)
    startTimeCombo.grid(row=1, column=1)

    Label(tip, text="End Time:").grid(row=3, column = 0)
    endTime = StringVar()
    endTimeCombo = Combobox(tip, values=tems, state='readonly', textvariable = endTime)
    endTimeCombo.grid(row=3, column=1)
            
    dayCombo.set("")
    startTimeCombo.set("")
    endTimeCombo.set("")
    
    submitTimeSlotButton = Button(tip, text = "Submit Class Time", width = 20, command=lambda: submitClassTime(tip, master, cl, day, startTime, endTime, timeDisplay, addClassButtonSpace)).grid(row=4, column = 1)
    
    tip.grab_set()
    tip.wait_window()
    #makes window to add a time slot to the class

def submitClassTime(tip, master, cl, day, startTime, endTime, timeDisplay, addClassButtonSpace):
    """
    Adds formatted list of time slot to class times nested list
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for i in range(5):
        if days[i]==day.get():
            start = int(startTime.get().replace(':', ''))
            end = int(endTime.get().replace(':', ''))
            if start>=end:
                till = Toplevel()
                till.title("Error")
                Label(till, text="Error: Start time must be before end time").pack()
                return # Invalid time slot
            else:
                cl.times.append((i+1, start, end))
    
    for i in range(len(cl.times)):
        for j in range(len(cl.times)):
            if not i == j:
                x = cl.times[i]
                y = cl.times[j]
                if x[0] == y[0] and not (x[2] <= y[1] or y[2] <= x[1]):
                    till = Toplevel()
                    till.title("Error")
                    Label(till, text="Error: Time slots overlap").pack()
                    cl.times.pop() # Remove last added time slot
                    return # Overlapping time slots

    timeDisplay.set(timeDisplay.get() + day.get() +" "+startTime.get()+" "+endTime.get()+"\n")

    addClassButtonSpace.set(addClassButtonSpace.get()+1)
    tip.destroy()

def createTestMasterSchedule():
    """
    Creates sample MasterSchedule for testing
    """
    fallCourses = [Course("MATH 101", [(2, 1100, 1230), (4, 1100, 1230)]),
                   Course("CISC 101", [(1, 900, 1030), (3, 900, 1030)]),
                   Course("HIST 101", [(1, 1100, 1230), (3, 1100, 1230)]),
                   Course("BIOL 101", [(2, 1000, 1130), (4, 1000, 1130)])]

    winterCourses = [Course("MATH 101", [(1, 900, 1030), (3, 900, 1030)]),
                     Course("CISC 102", [(2, 1100, 1230), (4, 1100, 1230)]),
                     Course("HIST 102", [(1, 1100, 1230), (3, 1100, 1230)]),
                     Course("CHEM 101", [(2, 1000, 1130), (4, 1000, 1130)])]

    requiredCourses = ["MATH 101", "CISC 102"]

    return MasterSchedule(fallCourses, winterCourses, requiredCourses)

def testSuite(root, master):
    """
    Runs test suite to confirm functions work properly
    """
    displayWindows(root, master, 3, True)
    displayWindows(root, master, 3, False)

def main():
    root = Tk()
    root.title("Course Selection")
    root.geometry("300x300")
    
    classDisplay = StringVar()
    classDisplay.set("")

    addClassButtonSpace = IntVar()
    addClassButtonSpace.set(9)

    submitAllClassesButtonSpace = IntVar()
    submitAllClassesButtonSpace.set(5)

    master = MasterSchedule([], [], [])
    
    tittle = Label(root, text="Select 'Add Class' to add your classes for fall and winter \nterms, then click 'Submit'")
    tittle.grid(row=0, sticky=W)

    addClassButton = Button(root, text = "Add Class", width = 20, command=lambda: addClass(root, master, classDisplay, submitAllClassesButtonSpace, addClassButtonSpace))
    addClassButton.grid(row=2, padx=85, sticky = W)

    displayClasses = Label(root, textvariable=classDisplay)
    displayClasses.grid(row=3, sticky=W)

    classNumLabel = Label(root, text = "How many Classes/term?")
    classNumLabel.grid(row=submitAllClassesButtonSpace.get(), sticky = W)
    classNum = IntVar()
    classNum.set(5)
    classNumBox = Combobox(root, values=[2,3,4,5,6,7,8], state='readonly', textvariable = classNum)
    classNumBox.grid(row=submitAllClassesButtonSpace.get(), padx=140)

    combine = IntVar()
    combineButton = Checkbutton(root, text="Create Combined Fall/Winter Schedules?", variable = combine)
    combineButton.grid(row=submitAllClassesButtonSpace.get()+1, sticky = W)

    createSchedulesButton = Button(root, text = "Submit my Classes", width = 20, command=lambda: displayWindows(root, master, classNum.get(), combine.get()))
    createSchedulesButton.grid(row=(submitAllClassesButtonSpace.get()+2), padx=75, sticky=W)

    #"""
    if __name__ == "__main__":
        testButton = Button(root, text = "Example (3-Class)", width = 16, command=lambda: testSuite(root, createTestMasterSchedule()))
        testButton.grid(row=(submitAllClassesButtonSpace.get()+4), padx=85, sticky=W)\
    #"""
    
    root.mainloop()

main()
