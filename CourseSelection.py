from tkinter import *
from tkinter import filedialog
from itertools import combinations
from tkinter.ttk import *
import tkinter.font as tkFont
import json

class Course:
    def __init__(self, n, t, i):
        self.name = n
        self.times = t
        self.id = i
        self.label = None
        self.deleteButton = None

class MasterSchedule:
    def __init__(self, f, w, r, i):
        self.fall = f # List of Fall Course Objects
        self.winter = w # List of Winter Course Objects
        self.required = r # List of Required Course Names (strings)
        self.idCounter = i
        # self.labelList = []

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

    menu = Menu(top)
    top.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Save Schedule", command=lambda: saveScheduleToFile(st))
    
    T = Label(top, text=st, font=tkFont.Font(family="Courier", size=9))
    T.pack()

def displayWindows(root, master, num, combine):
    """
    Calls functions to display fall and winter schedules, keeping track of the window count
    """
    count = 1
    if combine: 
        count += displayCombinedScheduleWindows(root, master, num, count)
    else:
        count += displaySingleScheduleWindows(root, master.fall, num, count, True)
        count += displaySingleScheduleWindows(root, master.winter, num, count, False)
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
    return count

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
    return count

def checkRequired(master):
    existingNames = {c.name for c in master.fall + master.winter}
    master.required = [name for name in master.required if name in existingNames]

def rebuildClassList(frame, master, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton):

    # Clear existing rows
    for widget in frame.winfo_children():
        widget.destroy()

    row = 0

    for course in master.fall + master.winter:
        text = course.name
        if course in master.fall:
            text += " (Fall)"
        else:
            text += " (Winter)"
        if course.name in master.required:
            text += " (Required)"

        lbl = Label(frame, text=text)
        lbl.grid(row=row, column=1, sticky=W)

        btn = Button(frame, text="-", width=2, 
                     command=lambda cid=course.id: deleteClass(cid, master, frame, classNumLabel, classNumBox, combineButton,createSchedulesButton, saveCourseSetButton, loadCourseSetButton))
        btn.grid(row=row, column=0, sticky=W)

        course.label = lbl
        course.deleteButton = btn
        row += 1

def addClass(root, master, classList, addClassButtonSpace, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton):
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

    cl = Course("", [], -1)
    
    timeDisplay = StringVar() # Display of time slots
    timeDisplay.set("")

    displayTimes = Label(top, textvariable=timeDisplay)
    displayTimes.grid(row=8, sticky=W)

    addTimeSlotButton = Button(top, text = "Add Time Slot", width = 15, command=lambda: addClassTime(top, master, cl, timeDisplay, addClassButtonSpace)).grid(row=7, padx=75, sticky=W)

    finishClassButton = Button(top, text = "Submit Class", width = 20, command=lambda: submitClass(
        root, top, master, cl, nem.get(), req, fw, classList, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton)).grid(row=addClassButtonSpace.get(), padx=60, sticky=W)

    top.grab_set()
    top.wait_window()

def submitClass(root, top, master, cl, nem, req, fw, classList, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton):
    """
    Submits class to masterlist, deletes toplevel
    """
    if len(nem.strip())>10:
        till = Toplevel()
        till.title("Error")
        till.geometry("200x50")
        Label(till, text="Error: Name is too long").pack()
        till.grab_set()
        till.wait_window()
        return # Name is too long
    if len(nem.strip())==0:
        till = Toplevel()
        till.title("Error")
        till.geometry("200x50")
        Label(till, text="Error: Name cannot be empty").pack()
        till.grab_set()
        till.wait_window()
        return # Name cannot be empty
    cl.name = nem
    if len(cl.times)==0:
        till = Toplevel()
        till.title("Error")
        till.geometry("200x50")
        Label(till, text="Error: No time slots added").pack()
        till.grab_set()
        till.wait_window()
        return # No time slots added

    if req.get() == 1 and cl.name not in master.required: # Add class to required list
        master.required.append(cl.name)

    if fw.get() == 1:
        master.fall.append(cl)
    elif fw.get()==2:
        master.winter.append(cl)
    if req.get() == 1 and cl.name not in master.required:
        master.required.append(cl.name)
    
    cl.id = master.idCounter
    master.idCounter += 1

    rebuildClassList(classList, master, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton)

    checkRequired(master)

    top.destroy()

def deleteClass(classID, master, classList, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton):
    """
    Deletes class from master and remove buttons/labels from root toplevel
    """
    index = -1
    col = None
    fw = None
    for i in range(len(master.fall)):
        if master.fall[i].id == classID:
            col = master.fall[i]
            index = i
            fw = True
            break
    for i in range(len(master.winter)):
        if master.winter[i].id == classID:
            col = master.winter[i]
            index = i
            fw = False
            break
    
    if fw == True:
        master.fall.pop(index)
    else:
        master.winter.pop(index)

    checkRequired(master)

    rebuildClassList(classList, master, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton)

def getTimesStringList():
    tems = []
    for i in range(8, 22): # Create list of possible times
        tems.append(str(i)+":00")
        tems.append(str(i)+":30")
    return tems

def addClassTime(top, master, cl, timeDisplay, addClassButtonSpace):
    """
    Create new toplevel to add a time slot to the current class 
    """
    tip = Toplevel()
    tip.title("Time Slot")
    tip.geometry("250x200")
            
    Label(tip, text="Day:").grid(row=1, column=0, sticky=W) # Decide what day
    day = StringVar()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    Radiobutton(tip, text = "Monday", variable = day, value = "Monday").grid(row = 2, column=0, sticky=W)
    Radiobutton(tip, text = "Tuesday", variable = day, value = "Tuesday").grid(row = 3, column=0, sticky=W)
    Radiobutton(tip, text = "Wednesday", variable = day, value = "Wednesday").grid(row = 4, column=0, sticky=W)
    Radiobutton(tip, text = "Thursday", variable = day, value = "Thursday").grid(row = 5, column=0, sticky=W)
    Radiobutton(tip, text = "Friday", variable = day, value = "Friday").grid(row = 6, column=0, sticky=W)
    #dayCombo = Combobox(tip, values=days, state='readonly', textvariable = day)
    #dayCombo.grid(row=0, column=1)
            
    tems = getTimesStringList()
    
    Label(tip, text="Start Time:").grid(row=0, column=0, sticky=W) # Decide start time
    startTime = StringVar()
    startTimeCombo = Combobox(tip, values=tems, state='readonly', textvariable = startTime)
    startTimeCombo.grid(row=0, column=1)

    Label(tip, text="Class Length:").grid(row=1, column=1, sticky=W)
    classLength = StringVar()
    lengthOptions = ["30 minutes", "1 hour", "1 hour 30 minutes", "2 hours", "2 hours 30 minutes", "3 hours"]
    Radiobutton(tip, text = "30 minutes", variable = classLength, value = "30 minutes").grid(row = 2, column=1, sticky=W)
    Radiobutton(tip, text = "1 hour", variable = classLength, value = "1 hour").grid(row = 3, column=1, sticky=W)
    Radiobutton(tip, text = "1 hour 30 minutes", variable = classLength, value = "1 hour 30 minutes").grid(row = 4, column=1, sticky=W)
    Radiobutton(tip, text = "2 hours", variable = classLength, value = "2 hours").grid(row = 5, column=1, sticky=W)
    Radiobutton(tip, text = "2 hours 30 minutes", variable = classLength, value = "2 hours 30 minutes").grid(row = 6, column=1, sticky=W)
    Radiobutton(tip, text = "3 hours", variable = classLength, value = "3 hours").grid(row = 7, column=1, sticky=W)
    #classLengthCombo = Combobox(tip, values=lengthOptions, state='readonly', textvariable = classLength)
    #classLengthCombo.grid(row=3, column=1)
    
    day.set("Monday")
    startTimeCombo.set("")
    classLength.set("1 hour")

    submitTimeSlotButton = Button(tip, text = "Submit Class Time", width = 20, command=lambda: submitClassTime(tip, master, cl, day, startTime, classLength, timeDisplay, addClassButtonSpace)).grid(row=8, column=0, columnspan=2)

    tip.grab_set()
    tip.wait_window()
    #makes window to add a time slot to the class

def submitClassTime(tip, master, cl, day, startTime, classLength, timeDisplay, addClassButtonSpace):
    """
    Adds formatted list of time slot to class times nested list
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    if day.get() not in days:
        till = Toplevel()
        till.title("Error")
        till.geometry("200x50")
        Label(till, text="Error: Invalid day selected").pack()
        till.grab_set()
        till.wait_window()
        return # Invalid day selected
    
    if startTime.get() not in getTimesStringList():
        till = Toplevel()
        till.title("Error")
        till.geometry("200x50")
        Label(till, text="Error: Invalid start time selected").pack()
        till.grab_set()
        till.wait_window()
        return # Invalid start time selected

    lengthMap = {
        "30 minutes": 30,
        "1 hour": 100,
        "1 hour 30 minutes": 90,
        "2 hours": 200,
        "2 hours 30 minutes": 130,
        "3 hours": 300
    }

    if classLength.get() not in lengthMap:
        till = Toplevel()
        till.title("Error")
        Label(till, text="Error: Invalid class length").pack()
        return # Invalid class length
    length = lengthMap[classLength.get()]
    if length % 100 >= 60:
        length += 40 # Adjust for minutes overflow

    for i in range(5):
        if days[i]==day.get():
            start = int(startTime.get().replace(':', ''))
            end = int(start + length)
            if end % 100 >= 60:
                end += 40 # Adjust for minutes overflow
            cl.times.append((i+1, start, end))

    endTime = str(end)[:-2] + ":" + str(end)[-2:]

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
                    till.grab_set()
                    till.wait_window()
                    return # Overlapping time slots

    timeDisplay.set(timeDisplay.get() + day.get() +" "+startTime.get()+" - "+endTime +"\n")

    addClassButtonSpace.set(addClassButtonSpace.get()+1)
    tip.destroy()

def turnMasterToDict(master):
    """
    Converts MasterSchedule to dictionary for saving

    :param master: MasterSchedule object
    :return: Dictionary representation of MasterSchedule
    """
    masterDict = {
        "fall": [],
        "winter": [],
        "required": master.required
    }
    for course in master.fall:
        courseDict = {"name": course.name, "times": course.times}
        masterDict["fall"].append(courseDict)
    for course in master.winter:
        courseDict = {"name": course.name, "times": course.times}
        masterDict["winter"].append(courseDict)
    return masterDict

def saveCourseloadToFile(master):
    """
    Saves Course objects to a json file

    :param master: Nested triple-list of Course objects
    """
    # Remember to include error checking for file operations
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if not filename:
        return  # User cancelled the save dialog
    
    save = turnMasterToDict(master)
    save = json.dumps(save)

    with open(filename, 'w') as file:
        file.write(save)
    file.close()

def loadCourseloadFromFile(root, master, classList, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton):
    """
    Loads schedules from a text file and updates the display

    :master: Nested triple-list of Course objects
    :return: List of Course objects
    """
    # empty master and load from file
    load = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if not load:
        return  # User cancelled the open dialog
    with open(load, 'r') as file:
        data = file.read()
    file.close()
    loadDict = json.loads(data)

    master.fall = []
    master.winter = []
    master.required = loadDict["required"]
    master.idCounter = 1

    for course in loadDict["fall"]:
        col = Course(course["name"], course["times"], master.idCounter)
        master.fall.append(col)
        master.idCounter += 1
    
    for course in loadDict["winter"]:
        col = Course(course["name"], course["times"], master.idCounter)
        master.winter.append(col)
        master.idCounter += 1

    rebuildClassList(classList, master, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton)

    checkRequired(master)

def saveScheduleToFile(scheduleString):
    """
    Saves a single schedule to a text file

    :param scheduleString: Schedule string to save
    """
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file is None: # User cancelled the save dialog
        return
    with open(file.name, 'w') as f:
        f.write(scheduleString)
    f.close()
  
def main():
    root = Tk()
    root.title("Course Selection")
    root.geometry("300x400") # make height a variable based on number of classes? or add automatical scroll bar somehow
    
    classContainer = Frame(root)
    classContainer.grid(row=5, column=0, sticky="nsew")

    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)

    classContainer.grid_rowconfigure(0, weight=1)
    classContainer.grid_columnconfigure(0, weight=1)

    classCanvas = Canvas(classContainer, height=300)
    classCanvas.grid(row=0, column=0, sticky="nsew")

    scrollBar = Scrollbar(classContainer, orient="vertical", command=classCanvas.yview)
    scrollBar.grid(row=0, column=1, sticky="ns")

    classCanvas.configure(yscrollcommand=scrollBar.set)

    classList = Frame(classCanvas)
    classCanvas.create_window((0,0), window=classList, anchor="nw")
    #classList.grid(row=5, column=0, sticky=W)

    def updateScrollRegion(event):
        classCanvas.configure(scrollregion=classCanvas.bbox("all"))
    
    classList.bind("<Configure>", updateScrollRegion)

    def _on_mousewheel(event):
        classCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    classCanvas.bind_all("<MouseWheel>", _on_mousewheel)

    controls = Frame(root)
    controls.grid(row=10, sticky=W, pady=12)

    addClassButtonSpace = IntVar()
    addClassButtonSpace.set(9)

    master = MasterSchedule([], [], [], 1)
    
    tittle = Label(root, text="Select 'Add Class' to add your classes for fall and winter \nterms, then click 'Submit'")
    tittle.grid(row=0, sticky=W)

    classNumLabel = Label(root, text = "How many Classes/term?")
    classNumLabel.grid(in_=controls, row=0, sticky = W)
    classNum = IntVar()
    classNum.set(5)
    classNumBox = Combobox(root, values=[2,3,4,5,6,7,8], state='readonly', textvariable = classNum)
    classNumBox.grid(in_=controls, row=0, padx=140)

    combine = IntVar()
    combineButton = Checkbutton(root, text="Create Combined Fall/Winter Schedules?", variable = combine)
    combineButton.grid(in_=controls, row=1, sticky = W)

    createSchedulesButton = Button(root, text = "Submit my Classes", width = 30, command=lambda: displayWindows(root, master, classNum.get(), combine.get()))
    createSchedulesButton.grid(in_=controls, row=2, padx=55, sticky=W)

    saveCourseSetButton = Button(root, text = "Save Course Set", width = 14, command=lambda: saveCourseloadToFile(master))
    saveCourseSetButton.grid(in_=controls, row=3, padx=55, sticky=W)

    loadCourseSetButton = Button(root, text = "Load Course Set", width = 14, command=lambda: loadCourseloadFromFile(root, master, classList, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton))
    loadCourseSetButton.grid(in_=controls, row=3, padx=150, sticky=W)

    addClassButton = Button(root, text = "Add Class", width = 20, command=lambda: addClass(root, master, classList, addClassButtonSpace, classNumLabel, classNumBox, combineButton, createSchedulesButton, saveCourseSetButton, loadCourseSetButton))
    addClassButton.grid(row=2, padx=85, sticky = W)
    
    root.mainloop()

main()
