import os
import subprocess

global userinput
userinput = ''



#these values will be filled with config info
global defaultnaming
defaultnaming = False

global venvname
venvname = ''


global requirementsfilename
requirementsfilename = ''


global ownbatscriptname
ownbatscriptname = ''


global ownpythonscriptname
ownpythonscriptname = ''


def StartApp():

    config()

    getinput()







def config():
    global defaultnaming
    global venvname
    global requirementsfilename
    global ownbatscriptname
    global ownpythonscriptname

    f = open('venv-guide-config.txt','r')
    configlines = f.readlines()
    f.close()


    #default naming: if true then you never ask for venv name when creating. it will always be named venv
    defaultnamingconfig = configlines[0]
    defaultnamingconfig = defaultnamingconfig.replace('\n','')
    defaultnamingconfig = defaultnamingconfig.replace(' ','')
    defaultnamingconfigarr = defaultnamingconfig.split('=')
    defaultnamingconfig = defaultnamingconfigarr[1]


    #requirements file name:
    defaultrequirementsnameconfig = configlines[2]
    defaultrequirementsnameconfig = defaultrequirementsnameconfig.replace('\n','')
    defaultrequirementsnameconfig = defaultrequirementsnameconfig.replace(' ','')
    defaultrequirementsnameconfigarr = defaultrequirementsnameconfig.split('=')
    requirementsfilename = defaultrequirementsnameconfigarr[1]



    #own bat script name
    batchscriptnameconfig = configlines[3]
    batchscriptnameconfig = batchscriptnameconfig.replace('\n','')
    batchscriptnameconfig = batchscriptnameconfig.replace(' ','')
    batchscriptnameconfigarr = batchscriptnameconfig.split('=')
    ownbatscriptname = batchscriptnameconfigarr[1]


    #own python script name
    ownpythonscriptnameconfig = configlines[4]
    ownpythonscriptnameconfig = ownpythonscriptnameconfig.replace('\n','')
    ownpythonscriptnameconfig = ownpythonscriptnameconfig.replace(' ','')
    ownpythonscriptnameconfigarr = ownpythonscriptnameconfig.split('=')
    ownpythonscriptname = ownpythonscriptnameconfigarr[1]


    #set venv name

    if defaultnamingconfig.upper() == 'TRUE':
        defaultnaming = True
        venvname = 'venv'

    elif defaultnamingconfig.upper() == 'FALSE':
        defaultnaming = False
        #venv name: if your venv is always named something specific type it here so you are never asked to provide venv name
        defaultvenvnameconfig = configlines[1]
        defaultvenvnameconfig = defaultvenvnameconfig.replace('\n','')
        defaultvenvnameconfig = defaultvenvnameconfig.replace(' ','')
        defaultvenvnameconfig = defaultvenvnameconfig.split('=')
        defaultvenvnameconfig = defaultvenvnameconfig[1]



        if defaultvenvnameconfig.upper() == '':
            venvname = ''
        else:
            venvname = defaultvenvnameconfig







def getinput():
    global userinput
    #there is a venv-guide-config.txt file in the first line you provide the venv name. the app always checks for that. if there's nothing there it asks you for the venv folder name.
    while(userinput == ''):
        print('Welcome to venv-guide. Choose one of the options below by typing the number')
        print('')
        print('0 - provide the name of existing virtual environment')
        print('1 - create a virtual environment in this folder')
        print('2 - install requirements.txt inside the virtual environment')  #asks for venv name #the requirements.txt file should be in the same location
        print('3 - pip freeze the virtual environment') #asks for name of the requirements file you want to save it to (if in config it is empty).
        print('4 - create an autorun file for your python script in the virtual environemt')   #asks for your name preference
        print('5 - create an autorun file for your virtual environemt')
        print('6 - create an autorun file for your pip freeze command')
        print('7 - just run the virtual environment and stay in the scripts folder')
        print('8 - just run the virtual environment and come back to this directory')
        print('9 - just run my own batch script in this directory')  #checks the config if there's anything there otherwise it asks for the name of the bat script
        print('10 - just run your own python script in the virtual environemt')   #asks for your name preference if not specified in the config
        print('88 - REMOVE ALL PREFERENCES (this runs the configuration again)')
        print('')


        userchoice = input('')


        try:
            if(userchoice == '0'):
                setvenvname()

            elif(userchoice == '1'):
                createvenv()

            elif(userchoice == '2'):
                installrequirements()

            elif(userchoice == '3'):
                pipfreeze()

            elif(userchoice == '4'):
                createautorun('script','')

            elif(userchoice == '5'):
                createautorun('venv','')

            elif(userchoice == '6'):
                createautorun('pipfreeze','')

            elif(userchoice == '7'):
                runvenv()

            elif(userchoice == '8'):
                runvenvadv()

            elif(userchoice == '9'):
                runownbat()

            elif(userchoice == '10'):
                runownpythonscript()

            elif(userchoice == '88'):
                reset()





            userinput = ''

        except Exception as e:
            print('Exception was thrown. Going back to main app.')
            print(e)



def setvenvname():
    global venvname
    print('Type the name of your python virtual environment.')
    venvname = input('')
    print('Name set.')


def createvenv():
    global defaultnaming
    global venvname

    venvnamestate = venvname


    if defaultnaming == False:

        if venvnamestate != '':
            venvname = venvnamestate
        else:
            print('virutal environment name?')
            venvname = input('')

    elif defaultnaming == True:
        venvname = 'venv'





    print('Creating a virtual environment named ' + venvname)
    print('Please do not stop this terminal.')
    f = open('venvcreator.bat','w')
    f.writelines("""python -m venv ./""" +  venvname + " \n" + """@echo The virtual environment for python was successfuly created.""" + '\n' + 'timeout 3' + ' \n' + 'exit /s' )
    f.close()

    subprocess.call(['venvcreator.bat'])
    #remove the venv creator file so no one by accident overwrites the venv
    if os.path.exists("venvcreator.bat"):
        os.remove("venvcreator.bat")












def installrequirements():
    #make a new bat file in scripts folder   activate-auto-install.bat
    #it has everything in the activate-auto.bat  but you have to append to it   cd .. cd..  and a pip install -r <requirementsfilename>
    global defaultnaming
    global venvname
    global requirementsfilename
    #check venv name
    venvnamestate = venvname


    if defaultnaming == False:

        if venvnamestate != '':
            venvname = venvnamestate
        else:
            print('Virutal environment name?')
            venvname = input('')

    elif defaultnaming == True:
        venvname = 'venv'


    if requirementsfilename == '':
        print('Full name of the requirements text file?')
        requirementsfilename = input('')

    print('Installing the requirements from ' + requirementsfilename)
    print('Please do not stop this terminal.')



    #copy activate.bat content to a new file named activate-auto-install.bat and add to the end of it
    try:
        f = open(venvname +'/scripts/activate.bat','r')
        activatebatlines = f.read()  #reads the whole text
        f.close()

        f = open(venvname +'/scripts/activate-auto-install.bat','w')
        f.write(activatebatlines)
        f.close()

        #now add the new lines.  cd .. cd ..
        f = open(venvname +'/scripts/activate-auto-install.bat','a')
        f.writelines(' \n' + 'cd ..' + ' \n' +'cd ..' + ' \n' + 'pip install -r ' + requirementsfilename + ' \n' + 'timeout 5')
        f.close()



        #make requirementsinstaller script that runs activate-auto-install.bat

        f = open('requirementsinstaller.bat','w')
        f.writelines("""cd %CD%/""" +  venvname +  '/Scripts' + ' \n' + 'activate-auto-install.bat')
        f.close()
        print('The requirements installer file is named: requirementsinstaller.bat')

        subprocess.call(['requirementsinstaller.bat'])

    #if there is no virtual environment it creates it and calls the installrequirements function again
    except FileNotFoundError:
        print('You did not have a virtual environment. Creating one for you..')
        createvenv()
        print('Virtual environment created. Name of virtual environment: ' + venvname)
        print('Now installing the requirements in the newly created virtual environment..')
        installrequirements()







def pipfreeze():
    #make a new bat file in scripts folder   autopipfreeze.bat
    #it has everything in the activate-auto.bat  but you have to append to it   cd .. cd..  and a pip install -r <requirementsfilename>
    global defaultnaming
    global venvname
    global requirementsfilename
    #check venv name
    venvnamestate = venvname


    if defaultnaming == False:

        if venvnamestate != '':
            venvname = venvnamestate
        else:
            print('Virutal environment name?')
            venvname = input('')

    elif defaultnaming == True:
        venvname = 'venv'


    if requirementsfilename == '':
        print('Full name of the distination requirements text file?')
        requirementsfilename = input('')

    print('Running pip freeze command on your environment ' + venvname)
    print('Please do not stop this terminal.')



    #copy activate.bat content to a new file named activate-auto-install.bat and add to the end of it

    try:
        f = open(venvname +'/scripts/activate.bat','r')
        activatebatlines = f.read()  #reads the whole text
        f.close()

        f = open(venvname +'/scripts/autopipfreeze.bat','w')
        f.write(activatebatlines)
        f.close()

        #now add the new lines.  cd .. cd ..
        f = open(venvname +'/scripts/autopipfreeze.bat','a')
        f.writelines(' \n' + 'cd ..' + ' \n' +'cd ..' + ' \n' + 'pip freeze > ' + requirementsfilename + '  \n' + """@echo Results of the pip freeze command are now saved in """ +  requirementsfilename + ' file'  + ' \n' + 'timeout 5')
        f.close()



        #make pipfreeze.bat script that runs the autopipfreeze.bat
        f = open('pipfreeze.bat','w')
        f.writelines("""cd %CD%/""" +  venvname +  '/Scripts' + ' \n' + 'start autopipfreeze.bat')
        f.close()

        print('The pip freeze script is named pipfreeze.bat')
        subprocess.call(['pipfreeze.bat'])

    #if there is no virtual environment it creates it and calls the installrequirements function again
    except FileNotFoundError:
        print('You do not have a virtual environment. Creating one for you..')
        createvenv()
        print('Virtual environment created. Now installing your requirements..')
        installrequirements()
        print('Now running pip freeze command..')
        pipfreeze()

def createautorun(type,thescriptname):

    global defaultnaming
    global venvname
    global requirementsfilename
    #check venv name
    venvnamestate = venvname


    if defaultnaming == False:

        if venvnamestate != '':
            venvname = venvnamestate
        else:
            print('Virutal environment name?')
            venvname = input('')

    elif defaultnaming == True:
        venvname = 'venv'


    if type == 'script':
        if thescriptname == '':
            print('Type the fullname of the python script')
            scriptname = input('')
        else:
            scriptname = thescriptname
        scriptnamewithoutextension = scriptname.replace('.','-')

        try:
            f = open(venvname +'/scripts/activate.bat','r')
            activatebatlines = f.read()  #reads the whole text
            f.close()

            f = open(venvname +'/scripts/activate-auto-' + scriptnamewithoutextension  + '.bat','w')
            f.write(activatebatlines)
            f.close()

            #now add the new lines.  cd .. cd ..
            f = open(venvname +'/scripts/activate-auto-' + scriptnamewithoutextension + '.bat','a')
            f.writelines(' \n' + 'cd ..' + ' \n' +'cd ..' + ' \n' + 'py ' + scriptname + '  \n' + 'pause' +  ' \n' + """cmd /k""")
            f.close()



            #make pipfreeze.bat script that runs the autopipfreeze.bat
            f = open('runscript-' + scriptnamewithoutextension + '.bat','w')
            autorunpythonscriptname = 'runscript-' + scriptnamewithoutextension + '.bat'
            f.writelines("""cd %CD%/""" +  venvname +  '/Scripts' + ' \n' + 'start activate-auto-' + scriptnamewithoutextension + '.bat')
            f.close()

            print('The autorun batch file is named: ' + autorunpythonscriptname)
            print('Opening this batch file runs' + scriptname + ' inside the virtual environment.')
            answer = ''

            ask = True
            while((answer.upper() != 'N' or answer.upper() != 'Y') and ask == True):
                print('Do you want to run the autorun batch file? y/n')
                answer = input('')

                if answer.upper() == 'Y':
                    print('Running the batch file.')
                    subprocess.call([autorunpythonscriptname])
                    ask = False

                elif answer.upper() == 'N':
                    print('Getting back to the main application..')
                    ask = False

        #if there is no virtual environment it creates it and calls the installrequirements function again
        except FileNotFoundError:
            print('You do not have a virtual environment. Creating one for you..')
            createvenv()
            print('Virtual environment created. Now installing your requirements..')
            installrequirements()
            print('Now creating the autorun script for the python code..')
            createautorun('script',scriptname)




    elif type == 'venv':
        if thescriptname == '':
            print('Type the fullname of the auto venv runner file you want to create. ')
            print('The name should end with .bat extension  e.g venvrunner.bat')
            print('')
            scriptname = input('')
        else:
            scriptname = thescriptname

        scriptnamewithoutextension = scriptname.replace('.','-')

        try:
            f = open(venvname +'/scripts/activate.bat','r')
            activatebatlines = f.read()  #reads the whole text
            f.close()

            f = open(venvname +'/scripts/activate-auto-' + scriptnamewithoutextension  + '.bat','w')
            f.write(activatebatlines)
            f.close()

            #now add the new lines.  cd  .. cd ..
            f = open(venvname +'/scripts/activate-auto-' + scriptnamewithoutextension + '.bat','a')
            f.writelines(' \n' + 'cd ..' + ' \n' +'cd ..')
            f.close()

            #make vevnrunner .bat script that runs the activate.bat
            f = open(scriptname,'w')
            f.writelines("""cd %CD%/""" +  venvname +  '/Scripts' + ' \n' + 'start activate-auto-' + scriptnamewithoutextension + '.bat')
            f.close()

            print('The auto venv runner batch file is named: ' + scriptname)
            print('Opening this batch file runs your virtual environment named ' + venvname + '.')
            answer = ''

            ask = True
            while((answer.upper() != 'N' or answer.upper() != 'Y') and ask == True):
                print('Do you want to run the venv runner batch file? y/n')
                answer = input('')

                if answer.upper() == 'Y':
                    print('Running the batch file.')
                    subprocess.call([scriptname])
                    ask = False

                elif answer.upper() == 'N':
                    print('Getting back to the main application..')
                    ask = False

        #if there is no virtual environment it creates it and calls the create auto run function again
        except FileNotFoundError:
            print('You do not have a virtual environment. Creating one for you..')
            createvenv()
            print('Virtual environment created. Now installing your requirements..')
            installrequirements()
            print('Now creating the autorun venv runner script for the virtual environment..')
            createautorun('venv',scriptname)


    elif type == 'pipfreeze':
        if thescriptname == '':
            print('Type the fullname of the auto pip freeze file you want to create. ')
            print('The name should end with .bat extension  e.g pipfreeze.bat')
            print('')
            scriptname = input('')
        else:
            scriptname = thescriptname

        scriptnamewithoutextension = scriptname.replace('.','-')

        try:
            f = open(venvname +'/scripts/activate.bat','r')
            activatebatlines = f.read()  #reads the whole text
            f.close()

            f = open(venvname +'/scripts/activate-auto-' + scriptnamewithoutextension  + '.bat','w')
            f.write(activatebatlines)
            f.close()

            #now add the new lines.  cd  .. cd ..

            if requirementsfilename == '':
                requirementsfilename = venvname + '-' + 'requirements.txt'
            f = open(venvname +'/scripts/activate-auto-' + scriptnamewithoutextension + '.bat','a')
            f.writelines(' \n' + 'cd ..' + ' \n' +'cd ..' + ' \n' + 'pip freeze > ' + requirementsfilename + '  \n' + """@echo Results of the pip freeze command are now saved in """ +  requirementsfilename + ' file'  + ' \n' + 'timeout 5')
            f.close()

            #make pipfreeze.bat script that runs the autopipfreeze.bat
            f = open(scriptname,'w')
            f.writelines("""cd %CD%/""" +  venvname +  '/Scripts' + ' \n' + 'start activate-auto-' + scriptnamewithoutextension + '.bat')
            f.close()

            print('The autorun pipfreeze batch file is named: ' + scriptname)
            print('Opening this batch file runs pip freeze inside the virtual environment named ' + venvname + '.')
            answer = ''

            ask = True
            while((answer.upper() != 'N' or answer.upper() != 'Y') and ask == True):
                print('Do you want to run the pip freeze batch file? y/n')
                answer = input('')

                if answer.upper() == 'Y':
                    print('Running the batch file.')
                    subprocess.call([scriptname])
                    ask = False

                elif answer.upper() == 'N':
                    print('Getting back to the main application..')
                    ask = False

        #if there is no virtual environment it creates it and calls the installrequirements function again
        except FileNotFoundError:
            print('You do not have a virtual environment. Creating one for you..')
            createvenv()
            print('Virtual environment created. Now installing your requirements..')
            installrequirements()
            print('Now creating the autorun pipfreeze script for the virtual environment..')
            createautorun('pipfreeze',scriptname)

def runvenv():
    global defaultnaming
    global venvname

    venvnamestate = venvname


    if defaultnaming == False:

        if venvnamestate != '':
            venvname = venvnamestate
        else:
            print('virutal environment name?')
            venvname = input('')

    elif defaultnaming == True:
        venvname = 'venv'





    print('Running the virtual environment ' + venvname)
    print('Please do not stop this terminal.')
    f = open('runvenv.bat','w')
    f.writelines("""cd %CD%/""" +  venvname +  '/Scripts' + ' \n' + 'start activate.bat')
    f.close()

    print('The venv runner file is named: runvenv.bat ')
    subprocess.call(['runvenv.bat'])

#runs the venv but two times cd..
def runvenvadv():
    global defaultnaming
    global venvname

    venvnamestate = venvname


    if defaultnaming == False:

        if venvnamestate != '':
            venvname = venvnamestate
        else:
            print('virutal environment name?')
            venvname = input('')

    elif defaultnaming == True:
        venvname = 'venv'





    print('Running the virtual environment ' + venvname)
    print('Please do not stop this terminal.')
    #copy activate.bat content to a new file named activate-adv.bat and add to the end of it

    f = open(venvname +'/scripts/activate.bat','r')
    activatebatlines = f.read()  #reads the whole text
    f.close()

    f = open(venvname +'/scripts/activate-adv.bat','w')
    f.write(activatebatlines)
    f.close()

    #now add the new lines.  cd .. cd ..
    f = open(venvname +'/scripts/activate-adv.bat','a')
    f.writelines(' \n' + 'cd ..' + ' \n' +'cd ..')
    f.close()



    #make runvenvadv script
    f = open('runvenvadv.bat','w')
    f.writelines("""cd %CD%/""" +  venvname +  '/Scripts' + ' \n' + 'start activate-adv.bat')
    f.close()

    print('The venv runner file that does cd .. to the main directory is named: runvenvadv.bat ')
    subprocess.call(['runvenvadv.bat'])


def runownbat():
    global ownbatscriptname
    if ownbatscriptname == '':
            print('Type the fullname of your own bat script which is in this directory. ')
            print('The name should end with .bat extension  e.g mybatscript.bat')
            print('')
            ownbatscriptname = input('')


    if os.path.exists(ownbatscriptname):
        print('Running your batch script named: ' + ownbatscriptname)
        subprocess.call([ownbatscriptname])

    else:
        print('There is no batch file named: ' + ownbatscriptname + ' in this directory.')
        print('Going back to the main application')








def runownpythonscript():
    global ownpythonscriptname
    global scriptnamewithoutextension

    if ownpythonscriptname == '':
            print('Type the fullname of your own python script which is in this directory. ')
            print('The name should end with .py extension  e.g testscript.py')
            print('')
            scriptname = input('')
            ownpythonscriptname = scriptname
            scriptnamewithoutextension = scriptname.replace('.','-')
    else:
        scriptname = ownpythonscriptname
        scriptnamewithoutextension = scriptname.replace('.','-')


    if os.path.exists(scriptname):
        print('Running your python script named: ' + scriptname)

        try:
            f = open(venvname +'/scripts/activate.bat','r')
            activatebatlines = f.read()  #reads the whole text
            f.close()

            f = open(venvname +'/scripts/activate-auto-' + scriptnamewithoutextension  + '.bat','w')
            f.write(activatebatlines)
            f.close()

            #now add the new lines.  cd .. cd ..
            f = open(venvname +'/scripts/activate-auto-' + scriptnamewithoutextension + '.bat','a')
            f.writelines(' \n' + 'cd ..' + ' \n' +'cd ..' + ' \n' + 'py ' + scriptname + '  \n' + 'pause' +  ' \n' + """cmd /k""")
            f.close()



            #make script runner .bat script that runs the bat script in scripts folder
            f = open('runscript-' + scriptnamewithoutextension + '.bat','w')
            autorunpythonscriptname = 'runscript-' + scriptnamewithoutextension + '.bat'
            f.writelines("""cd %CD%/""" +  venvname +  '/Scripts' + ' \n' + 'start activate-auto-' + scriptnamewithoutextension + '.bat')
            f.close()

            print('The autorun batch file is named: ' + autorunpythonscriptname)
            print('Opening this batch file runs' + scriptname + ' inside the virtual environment.')
            answer = ''

            print('Running the python script in the virtual environment..')
            subprocess.call([autorunpythonscriptname])




        #if there is no virtual environment it creates it and calls the installrequirements function again
        except FileNotFoundError:
            print('You do not have a virtual environment. Creating one for you..')
            createvenv()
            print('Virtual environment created. Now installing your requirements..')
            installrequirements()
            print('Now running your python script..')
            runownpythonscript()




    else:
        print('There is no python file named: ' + scriptname + ' in this directory.')
        print('Going back to the main application')









def reset():
    global defaultnaming
    defaultnaming = False

    global venvname
    venvname = ''


    global requirementsfilename
    requirementsfilename = ''


    global ownbatscriptname
    ownbatscriptname = ''


    global ownpythonscriptname
    ownpythonscriptname = ''

    config()


#program

StartApp()