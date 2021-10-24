# +visor
an auto-advisor that help you creating a schedule
remember the annoying process you'll have to go through every semester?
now with +visor all you need is one click!

How to use:
  1.feed it with CRN data (crn_data.csv)
    this file should contain all the crn data from your registration page
    you can manually input it OR grab it from the website
    +visor will use it to compute a rating for that class
  2.tell +visor your needs (CS_major.csv)
    this file can be generated from other input files or manually typed
    to generate the file, all you need to do is write a .csv file that has all the required classes for your major
  3.tell +visor your start point (student.csv)
    in our sample case, we start as freshman
    but after your registration, you only need to append classes you have registerd to the end of the file to use +visor again
    this has to be done manually because too many things can happen in one semester (withdraw, gapyear, F, etc.)
  4.now +visor has all the data he needs! simply run the python code and get a list of CRN to register!
