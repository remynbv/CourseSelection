# Course Selection
Displays all possible schedule combinations of a given list of classes and their time slots for university scheduling. Allows individual term or combined schedules and checks combined schedules to ensure all required courses are included. 

### Where to Start

To run the program without any dependencies, navigate to dist/CourseSelection & run CourseSelection.exe. A windows terminal window and the root window will appear; feel free to minimize the windows terminal (but do not close it; that will terminate the program). 

To add a class to your possible schedules, click 'Add Class." This will open a new window, prompting you to input a class name (maximum 10 characters), whether it is a required class for the year (this is only relevant for combined schedules: see below), and which term (fall or winter) it is available (feel free to imagine this as any term 1/term 2 combination which applies to you). 

Then, you may input time slots where this class has lecture or tutorial times: click 'Add Time Slot' to open a new window, then select the day of the week and start/end of the class, then submit to add the time slot to the class. Once all desired time slots have been added, click 'Submit Class' to add the class to the list. 

Once submitted, classes cannot be modified, but they can be deleted and replaced using the [-] button to the left of its name. 

Once you are satisfied with the class list, select how many classes you wish to have added to each term (default is 5), and whether to make individual term schedules or combined fall/winter schedule. Then, click submit and let the program work its magic; a window will be created displaying each possible valid combination of classes. 

Importantly, if a class has multiple possible options (i.e. you can take MATH 101 Monday and Wednesday or Tuesday and Thursday), input it as a separate class but with the same name. The program will recognize them as the same class and only ever give schedules with one option included. Likewise, if a class is in two parts (over fall and winter), they should be inputted as two separate classes in each term (i.e. MATH 101A in Fall, MATH 101B in winter). 

### Combined Schedules

By default, the program will create independent fall and winter schedules, creating all possibilities of fall schedules and all possible winter schedules without comparing them; you can then match them as you wish to decide your desired schedule (or only see options for one term if desired). 

If you select 'Create Combined Fall/Winter Schedules', the program will instead attempt to create valid full-year schedules. It will still create all of those independent fall and winter schedules, then check each combination between them; if there is no overlapping class between them and that all required classes are included in at least one of them. For each valid combination it finds, it will output the combined schedule. Note that as the number of classes increases, the number of possible combinations will increase exponentially (especially when there are not many required classes). 

### Saving Schedules

Once your course options list has been created, you can save it as a JSON file that can be loaded into the program later, saving you the trouble of re-inputing your classes if you want to take another look at your options. 

Similarly, an individual schedule can be saved as a text file: go to File -> Save Schedule on the schedule<s window. 

### Error Reports

If any errors or apparently unintended behaviour is exhibited, please let me know at remynbv@gmail.com, prefereably with explanantions and/or screenshots. I will do my best to rectify any bugs or unintended behaviour. 
