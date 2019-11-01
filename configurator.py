from stat import *
from tkinter import *
import os, sys, subprocess, tkinter.messagebox, time

class ForenQuest:
    def __init__(self,name,question,answer,points,enabled):
        self.name = name
        self.question = question
        self.answer = answer
        self.points = points
        self.enabled = enabled

class Vuln:
	def __init__(self,name,layout,tip,saved):
		self.name = name        #What is the vulnerability called?
		self.lay = layout	#What to put in each box
		self.tip = tip          #Explanation of the item
		self.saved = saved

class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master=master
		pad=3
		master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))

class AutoScrollbar(Scrollbar):
	# a scrollbar that hides itself if it's not needed. only works if you use th4e grid geometry manager.
	def set(self, lo, hi):
		if float(lo) <= 0.0 and float(hi) >= 1.0:
			# grid_remove is currently missing from Tkinter!
			self.tk.call("grid", "remove", self)
		else:
			self.grid()
		Scrollbar.set(self, lo, hi)
	def pack(self, **kw):
		raise (TclError, "cannot use pack with this widget")
	def place(self, **kw):
		raise (TclError, "cannot use place with this widget")

fq01 = ForenQuest("Question1.txt","Here is my question...","myanswer","0","0")
fq02 = ForenQuest("Question2.txt","Here is my question...","myanswer","0","0")
v001 = Vuln("silentMiss","","Check this box to hide missed items (Similar to competition)",False)
v002 = Vuln("FTPServer","","Check this box to enable an FTP server to save the scores (Similar to competition)",False)
v003 = Vuln("<Select One>","","<Description>",False)
v201 = Vuln("disableGuest","","Is the guest disabled in lightdm?",False)
v202 = Vuln("disableAutoLogin","","Is there an auto logged in user in lightdm?",False)
v203 = Vuln("disableUserGreeter","","Disable the user greeter in lightdm",False)
v204 = Vuln("XXX","","'PermitRootLogin no' exists in sshd_config",False)
v205 = Vuln("checkFirewall","","Is ufw enabled?",False)
v206 = Vuln("XXX","","Has kernel been updated?",False)
v207 = Vuln("antiVirus","","Has clamav freshclam been run?",False)
v208 = Vuln("minPassAge","","Value of min password age to score is 30 (login.defs)",False)
v209 = Vuln("maxPassAge","","Value of max password age to score is 60 (login.defs)",False)
v210 = Vuln("maxLoginTries","","Value of max login retries to score is 5 (login.defs)",False)
v211 = Vuln("checkPassLength","","Value min pw length is 10 (pam.d/common-password)",False)
v212 = Vuln("checkPassHist","","Value of passwords to remember is 5 (pam.d/common-password)",False)
v213 = Vuln("checkPassCompx","","Has password complexity been implemented? (pam.d/common-password)",False)
v214 = Vuln("##updateCheckPeriod","","Has the update check period been set to daily? (apt/apt.conf.d/10periodic)",False)
v215 = Vuln("updateAutoInstall","","Automaticaly download and install security updates.",False)
v301 = Vuln("goodUser","(Users)","Lose points for removing this user (use negative number) (Can take multiple entries)",False)
v302 = Vuln("badUser","(Users)","Remove these users to score (Can take multiple entries)",False)
v303 = Vuln("newUser","(Users)","This user must be created (Can take multiple entries)",False)
v304 = Vuln("changePassword","(Users)","User who must change password (Can take multiple entries)(Set the desired passwords before submitting)",False)
v305 = Vuln("goodAdmin","(Users)","Add these users to the sudo group (Can take multiple entries)",False)
v306 = Vuln("badAdmin","(Users)","Remove these users from the sudo group (Can take multiple entries)",False)
v307 = Vuln("goodGroup","(Groups)","This group must be created (Can take multiple entries)",False)
v308 = Vuln("badGroup","(Groups)","This group must be removed (Can take multiple entries)",False)
v309 = Vuln("goodProgram","(Programs)","Score points by installing these programs (Can take multiple entries)",False)
v310 = Vuln("badProgram","(Programs)","Score points by removing these programs (Can take multiple entries)",False)
v311 = Vuln("goodService","(Services)","Service that needs to be started (Can take multiple entries)",False)
v312 = Vuln("badService","(Services)","Service that needs to be stopped (Can take multiple entries)",False)
v313 = Vuln("badFile","(Location)","Score points for deleting this file (Can take multiple entries)",False)
v314 = Vuln("XXX","(Keywords)","Words to be removed from /etc/sudoers file (Can take multiple entries)",False)
v315 = Vuln("checkHosts","(Keywords)","Check /etc/hosts for a specific string (Can take multiple entries)",False)
v316 = Vuln("checkStartup","(Keywords)","Check rc.local for a specific string (Can take multiple entries)",False)
v401 = Vuln("taskScedualer","(User)(Keyword)","Check the root crontab for a specific string (Can take multiple entries)(If using multiple users be sure to include a keyword for each)",False)
v402 = Vuln("userInGroup","(users)(Group)","Users that need to be added to a group (Can take multiple entries)(If using multiple users be sure to include a group for each)",False)
v501 = Vuln("fileContainsText1","","Custom option for requiring a word or phrase to be added to a file.(Spaces will not be counted as separate entries)",False)
v502 = Vuln("fileContainsText2","","Custom option for requiring a word or phrase to be added to a file.(Spaces will not be counted as separate entries)",False)
v503 = Vuln("fileNoLongerContains1","","Custom option for requiring a word or phrase to be removed from a file.(Spaces will not be counted as separate entries)",False)
v504 = Vuln("fileNoLongerContains2","","Custom option for requiring a word or phrase to be removed from a file.(Spaces will not be counted as separate entries)",False)

vulns = [v001,v002,v201,v202,v203,v204,v205,v206,v207,v208,v209,v210,v211,v212,v213,v214,v215,v301,v302,v303,v304,v305,v306,v307,v308,v309,v310,v311,v312,v313,v314,v315,v316,v401,v402,v501,v502,v503,v504]
dontCheck = [ "silentMiss","<Select One>","Remove" ]
vulnNames2 = [ "disableGuest","disableAutoLogin","disableUserGreeter","disableSshRootLogin","checkFirewall","checkKernel","avUpdated","minPassAge","maxPassAge","maxLoginTries","checkPassHist","checkPassCompx","updateCheckPeriod","updateAutoInstall","Remove" ]
vulnNames3 = [ "goodUser","badUser","newUser","changePassword","goodAdmin","badAdmin","goodGroup","badGroup","goodProgram","badProgram","goodService","badService","badFile","secureSudoers","checkHosts","checkStartup","Remove" ]
vulnNames4 = [ "badCron","userInGroup","Remove" ]
vulnNames5 = [ "fileContainsText1","fileNoLongerContains1","Remove" ]


def addOptionMenu(loc, bRow, bColumn, list, optSet):
	eSave = len(all_entries)
	entry_select.append('')
	entry_select[eSave] = StringVar()
	entry_select[eSave].set(optSet) # default value
	entryOption = OptionMenu(loc, entry_select[eSave], *list, command=setEntry)
	entryOption.config(width=17)
	entryOption.grid(row=bRow, column=bColumn, sticky=W)

def addTextBox(loc, bRow, bColumn, size):
	global entry_textBox_count
	entry_textBox_count = entry_textBox_count + 1
	entry_textBox.append('')
	entry_textBox[entry_textBox_count] = StringVar()
	Entry(loc, textvariable=entry_textBox[entry_textBox_count],width=size).grid(row=bRow, column=bColumn, sticky=W)
	return entry_textBox_count

def addTextLable(loc, des, bRow, bColumn):
	global entry_lable_count
	entry_lable_count = entry_lable_count + 1
	entry_lable.append('')
	entry_lable[entry_lable_count] = StringVar()
	entry_lable[entry_lable_count].set(des)
	Label(loc, textvariable=entry_lable[entry_lable_count]).grid(row=bRow, column=bColumn, padx=10)
	return entry_lable_count


def addToFrame2(optSet):
	global entry_frame2_count
	entry_frame2_count = entry_frame2_count + 1
	frame2 = Frame(canvas)
	frame2.grid(row=100, column=0, sticky=W)
	
	ent1 = 2
	addOptionMenu(frame2, 1, 0, vulnNames2, optSet)
	
	ent2 = addTextBox(frame2, 1, 1, 5)
	
	ent3 = -1
	
	ent4 = -1
	
	ent5 = -1
	
	ent6 = -1
	
	ent7 = addTextLable(frame2, "<Description>", 1, 2)
	
	all_entries.append((ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame2))
	positionFrames()

def addToFrame3(optSet):
	global entry_frame3_count
	entry_frame3_count = entry_frame3_count + 1
	frame3 = Frame(canvas)
	frame3.grid(row=1000, column=0, sticky=W)
	
	ent1 = 3
	addOptionMenu(frame3, 1, 0, vulnNames3, optSet)
	
	ent2 = addTextBox(frame3, 1, 1, 5)
	
	ent3 = addTextBox(frame3, 1, 2, 20)
	
	ent4 = -1
	
	ent5 = -1
	
	ent6 = addTextLable(frame3, "<Content>", 1, 3)
	
	ent7 = addTextLable(frame3, "<Description>", 1, 4)
	
	all_entries.append((ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame3))
	positionFrames()

def addToFrame4(optSet):
	global entry_frame4_count
	entry_frame4_count = entry_frame4_count + 1
	frame4 = Frame(canvas)
	frame4.grid(row=1000, column=0, sticky=W)
	
	ent1 = 4
	addOptionMenu(frame4, 1, 0, vulnNames4, optSet)
	
	ent2 = addTextBox(frame4, 1, 1, 5)
	
	ent3 = addTextBox(frame4, 1, 2, 20)
	
	ent4 = addTextBox(frame4, 1, 3, 20)
	
	ent5 = -1
	
	ent6 = addTextLable(frame4, "<Content>", 1, 4)
	
	ent7 = addTextLable(frame4, "<Description>", 1, 5)
	
	all_entries.append((ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame4))
	positionFrames()

def addToFrame5(optSet):
	global entry_frame5_count
	entry_frame5_count = entry_frame5_count + 1
	frame5 = Frame(canvas)
	frame5.grid(row=1000, column=0, sticky=W)
	
	ent1 = 5
	addOptionMenu(frame5, 1, 0, vulnNames5, optSet)
	
	ent2 = addTextBox(frame5, 1, 1, 5)
	
	ent3 = addTextBox(frame5, 1, 2, 20)
	
	ent4 = addTextBox(frame5, 1, 3, 20)
	
	ent5 = addTextBox(frame5, 1, 4, 20)
	
	ent6 = -1
	
	ent7 = addTextLable(frame5, "<Description>", 1, 6)
	
	all_entries.append((ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame5))
	positionFrames()

def setEntry(event):
	vulnNames2Rem = []
	vulnNames2RemD = []
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
		if entry_select[number].get() in vulnNames2Rem:
			vulnNames2RemD.append(entry_select[number].get())
		if entry_select[number].get() in vulnNames2:
			vulnNames2Rem.append(entry_select[number].get())
			frame.config(bg=root.cget('bg'))
			error.grid_remove()
			errorFree = True
			dupFree = True
		if entry_select[number].get() == "Remove":
			frame.grid_remove()
		for vuln in vulns:
			if vuln.name == entry_select[number].get():
				entry_lable[ent6].set(vuln.lay)
				entry_lable[ent7].set(vuln.tip)
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
		if entry_select[number].get() in vulnNames2RemD:
			frame.config(bg='red')
			error.grid(row=2,column=3)
			errorFree = False
			dupFree = False

def positionFrames():
	frame2_pos = 2
	count2 = 1
	frame3_pos = 3
	count3 = 0
	f3_entries = []
	frame4_pos = 4
	count4 = 0
	f4_entries = []
	frame5_pos = 5
	count5 = 0
	f5_entries = []
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
		if ent1 == 2:
			count2 = count2 + 1
			frame2_pos = entry_frame2_count + count2
			frame.grid(row=frame2_pos, column=0, sticky=W)
			frame3.grid(row=frame2_pos + 1, column=0, sticky=W)
			if len(f3_entries) == 0:
				frame4.grid(row=frame2_pos + 2, column=0, sticky=W)
				frame5.grid(row=frame2_pos + 3, column=0, sticky=W)
		if ent1 == 3:
			f3_entries.append((ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame))
		if ent1 == 4:
			f4_entries.append((ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame))
		if ent1 == 5:
			f5_entries.append((ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame))
		if entry_select[number].get() == "Remove":
			frame.grid_remove()
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(f3_entries):
		count3 = count3 + 1
		frame3_pos = frame2_pos + entry_frame3_count + count3
		frame.grid(row=frame3_pos, column=0, sticky=W)
		frame4.grid(row=frame3_pos + 1, column=0, sticky=W)
		if len(f4_entries) == 0:
			frame5.grid(row=frame3_pos + 2, column=0, sticky=W)
		if entry_select[number].get() == "Remove":
			frame.grid_remove()
	if len(f3_entries) == 0:
		frame3_pos = frame2_pos + 1
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(f4_entries):
		count4 = count4 + 1
		frame4_pos = frame3_pos + entry_frame4_count + count4
		frame.grid(row=frame4_pos, column=0, sticky=W)
		frame5.grid(row=frame4_pos + 1, column=0, sticky=W)
		if entry_select[number].get() == "Remove":
			frame.grid_remove()
	if len(f4_entries) == 0:
		frame4_pos = frame3_pos + 1
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(f5_entries):
		count5 = count5 + 1
		frame5_pos = frame4_pos + entry_frame5_count + count5
		frame.grid(row=frame5_pos, column=0, sticky=W)
		if entry_select[number].get() == "Remove":
			frame.grid_remove()

def Mbox(title, text):
    messagebox.showwarning(title, text)

#Create the forensics questions and add answers to csel.cfg
def saveForQ():
	qHeader='This is a forensics question. Answer it below\n------------------------\n'
	qFooter='\n\nANSWER: <TypeAnswerHere>'
	f = open('csel.txt','a')  
	line1a = 'forensicsPath1=('+str(usrDsktp.get())+'Question1.txt)\n'
	line1b = 'forensicsAnswer1=('+fqans01.get()+')\n'
	line1c = 'checkForensicsQuestion1Value=('+str(fqpts01.get())+')\n'
	line1d = 'forensicsQuestion1='+fquest01.get()+'\n'
	line2a = 'forensicsPath2=('+str(usrDsktp.get())+'Question2.txt)\n'
	line2b = 'forensicsAnswer2=('+fqans02.get()+')\n'
	line2c = 'checkForensicsQuestion2Value=('+str(fqpts02.get())+')\n'
	line2d = 'forensicsQuestion2='+fquest02.get()+'\n'
	if fqcb01.get() != 0:
		for line in (line1a,line1b,line1c,line1d):
			f.write(line)
		g = open((str(usrDsktp.get())+'Question1.txt'),'w+')
		g.write(qHeader+fquest01.get()+qFooter)
		g.close()
	if fqcb02.get() != 0:
		for line in (line2a,line2b,line2c,line2d):
			f.write(line)
		h = open((str(usrDsktp.get())+'Question2.txt'),'w+')
		h.write(qHeader+fquest02.get()+qFooter)
		h.close()
	f.close()
	
def createForQ():
	qHeader='This is a forensics question. Answer it below\n------------------------\n'
	qFooter='\n\nANSWER: <TypeAnswerHere>'
	f = open('csel.cfg','a')  
	line1a = 'forensicsPath1=('+str(usrDsktp.get())+'Question1.txt)\n'
	line1b = 'forensicsAnswer1=('+fqans01.get()+')\n'
	line1c = 'checkForensicsQuestion1Value=('+str(fqpts01.get())+')\n'
	line2a = 'forensicsPath2=('+str(usrDsktp.get())+'Question2.txt)\n'
	line2b = 'forensicsAnswer2=('+fqans02.get()+')\n'
	line2c = 'checkForensicsQuestion2Value=('+str(fqpts02.get())+')\n'
	if fqcb01.get() != 0:
		for line in (line1a,line1b,line1c):
			f.write(line)
		g = open((str(usrDsktp.get())+'Question1.txt'),'w+')
		g.write(qHeader+fquest01.get()+qFooter)
		g.close()
	if fqcb02.get() != 0:
		for line in (line2a,line2b,line2c):
			f.write(line)
		h = open((str(usrDsktp.get())+'Question2.txt'),'w+')
		h.write(qHeader+fquest02.get()+qFooter)
		h.close()
	f.close()

#What happens when you click Submit?
def writeToConfig(name,points,keywords,keywordsExtra,message):
	f = open('csel.cfg','a')
	if name == 'changePassword':
		v = open('passGet.sh','w+')
		## Fix to Windows
		v.write("#!/bin/bash\n\nnames=\'"+keywords+"\'\necho '' > name.txt\nIFS=\' \'\nread -ra NAME <<< \"$names\"\nfor i in \"${NAME[@]}\"; do\ngetent shadow | grep \"$i\" >> name.txt\ndone")
		v.close()
		## fix this to windows version
		# os.chmod('passGet.sh', 0777)
		subprocess.call(['./passGet.sh'])
		with open('name.txt') as t:
			content = t.read().splitlines()
		t.close()
		passwdO = ''
		for cont in content:
			if cont != '':
				passwd = cont.split(':')
				if passwdO != '':
					passwdO = passwdO + ' ' + passwd[1]
				else:
					passwdO = passwd[1]
		keywordsExtra = passwdO.replace('$','\$')
		os.remove('passGet.sh')
		os.remove('name.txt')
	f.write(name+'=(y)\n')
	f.write(name+'Value=('+str(points)+')\n')
	if keywords != '':
		f.write(name+'Keywords=('+str(keywords)+')\n')
	if keywordsExtra != '':
		f.write(name+'ExtraKeywords=('+str(keywordsExtra)+')\n')
	if message != '':
		f.write(name+'Message=('+str(message)+')\n')
	f.close()

def submitCallback():
    #We wanna use those fancy variable lists 
	if os.geteuid() != 0:
		Mbox('Error', 'You need to be root to Write to Config. Please relaunch the confiturator with sudo.')
		return
	errorFree = True
	errorMessage = 'Please complete the following:'
	if not dupFree:
		errorFree = False
		errorMessage = errorMessage + '\n  Remove any duplicates in the first section.'
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
		frame.config(bg=root.cget('bg'))
		error.grid_remove()
		if entry_select[number].get() not in dontCheck:
			if entry_textBox[ent2].get() == '':
				errorFree = False
				frame.config(bg='red')
				error.grid(row=2,column=3)
				errorMessage = errorMessage + '\n  Fill in the points catagory for: ' + entry_select[number].get()
			if ent3 > 0 and entry_textBox[ent3].get() == '':
				errorFree = False
				frame.config(bg='red')
				error.grid(row=2,column=3)
				errorMessage = errorMessage + '\n  Fill in the keywords catagory for: ' + entry_select[number].get()
			if ent4 > 0 and entry_textBox[ent4].get() == '':
				errorFree = False
				frame.config(bg='red')
				error.grid(row=2,column=3)
				errorMessage = errorMessage + '\n  Fill in the extra keywords catagory for: ' + entry_select[number].get()
			if ent5 > 0 and entry_textBox[ent5].get() == '':
				errorFree = False
				frame.config(bg='red')
				error.grid(row=2,column=3)
				errorMessage = errorMessage + '\n  Fill in the message catagory for: ' + entry_select[number].get()
			if entry_select[number].get() in vulnNames4:
				entry3Test = entry_textBox[ent3].get()
				entry3Test = entry3Test.split(' ')
				entry4Test = entry_textBox[ent4].get()
				entry4Test = entry4Test.split(' ')
				if len(entry3Test) != len(entry4Test):
					errorFree = False
					frame.config(bg='red')
					error.grid(row=2,column=3)
					errorMessage = errorMessage + '\n  Enter an equal number of entries in each catagory for: ' + entry_select[number].get()
			if entry_select[number].get() in vulnNames5:
				entry3Test = entry_textBox[ent3].get()
				entry3Test = entry3Test.split(' ')
				entry4Test = entry_textBox[ent4].get()
				entry4Test = entry4Test.split(' ')
				entry5Test = entry_textBox[ent5].get()
				entry5Test = entry5Test.split(' ')
				if len(entry3Test) != len(entry4Test) or len(entry3Test) != len(entry5Test):
					errorFree = False
					frame.config(bg='red')
					error.grid(row=2,column=3)
					errorMessage = errorMessage + '\n  Enter an equal number of entries in each catagory for: ' + entry_select[number].get()
	if not errorFree:
		Mbox('Error', errorMessage)
	if errorFree:
		f = open('csel.cfg','w+')
		## Fix for a different code
		configHeader="#!/bin/bash\n#This config file was generated by configurator.py\n\n"
		f.write(configHeader)
		if silentMode.get() == 1:
			f.write('silentMiss=(y)\n')
		if ftpMode.get() == 1:
			f.write('FTPServer=(y)\n')
		f.close()
		createForQ()
		save_entry = []
		buff_entry = []
		for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
			for vuln in vulns:
				if vuln.name == entry_select[number].get() and entry_select[number].get() not in dontCheck:
					if not vuln.saved:
						s1 = vuln.name
						s2 = entry_textBox[ent2].get()
						s3 = ''
						s4 = ''
						s5 = ''
						if ent3 > -1:
							if entry_textBox[ent3].get() != '':
								kt = entry_textBox[ent3].get().split(' ')
								if len(kt) > 1:
									for t in range(1, len(kt)):
										s2 = s2 + ' ' + entry_textBox[ent2].get()
								s3 = entry_textBox[ent3].get()
						if ent4 > -1:
							if entry_textBox[ent4].get() != '':
								s4 = entry_textBox[ent4].get()
						if ent5 > -1:
							if entry_textBox[ent5].get() != '':
								s5 = entry_textBox[ent5].get()
						vuln.saved = True
						save_entry.append((s1, s2, s3, s4, s5))
					else:
						buff_entry = []
						for n, (s1, s2, s3, s4, s5) in enumerate(save_entry):
							if vuln.name == s1:
								s2 = s2 + ' ' + entry_textBox[ent2].get()
								if s3 != '':
									if entry_textBox[ent3].get() != '':
										kt = entry_textBox[ent3].get().split(' ')
										if len(kt) > 1:
											for t in range(1, len(kt)):
												s2 = s2 + ' ' + entry_textBox[ent2].get()
										s3 = s3 + ' ' + entry_textBox[ent3].get()
								if s4 != '':
									if entry_textBox[ent4].get() != '':
										s4 = s4 + ' ' + entry_textBox[ent4].get()
								if s5 != '':
									if entry_textBox[ent5].get() != '':
										s5 = s5 + ' ' + entry_textBox[ent5].get()
							buff_entry.append((s1, s2, s3, s4, s5))
						save_entry = buff_entry
		for n, (s1, s2, s3, s4, s5) in enumerate(save_entry):
			writeToConfig(s1, s2, s3, s4, s5)
		for vuln in vulns:
			vuln.saved = False
		f = open('csel.cfg','a')
		## Fix for Windows
		configFooter="index=(/usr/local/bin/ScoreReport.html)\nindexD=("+usrDsktp.get()+")\nindexR=(/usr/local/bin)\n#These values will change during install\nimageScore=0\nposPoints=0\nrelease=\"\"\ninitialKernel=(%KERNEL%)\ninstallDate=(%INSTALLDATE%)\n"
		f.write(configFooter)
		f.close()
		subprocess.Popen(['./install.sh'])
		time.sleep(2)
		exit()
		
	
def saveConfig():
	#We wanna use those fancy variable lists
	if userLoc.get() == 1:
		cwd = os.getcwd()
		cwd = cwd.replace("CSEW-master", "")
		usrDsktp.set(cwd)
	elif "/Desktop/" not in usrDsktp.get():
		cwd = usrDsktp.get()
		cwd = "C:/Users/"+cwd+"/Desktop/"
		usrDsktp.set(cwd)
	scoreLoc.set(usrDsktp.get())
	f = open('csel.txt','w+')
	f.write('Desktop='+usrDsktp.get()+'\n')
	if silentMode.get() ==1:
		f.write('silentMiss=(y)\n')
	if ftpMode.get() == 1:
		f.write('FTPServer=(y)\n')
	f.close()
	saveForQ()
	if ftpMode.get() == 1:
		f = open('FTP.txt','w+')
		line1 = 'serverName='+serverName.get()+'\n'
		line2 = 'userName='+userName.get()+'\n'
		line3 = 'password='+password.get()+'\n'
		for line in (line1,line2,line3):
			f.write(line)
		f.close()
	save_entry = []
	buff_entry = []
	f = open('csel.txt','a')
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
		for vuln in vulns:
			if vuln.name == entry_select[number].get() and vuln.name != "<Select One>":
				if not vuln.saved:
					s1 = vuln.name
					s2 = vuln.name + 'Value=(' + entry_textBox[ent2].get()
					s3 = ''
					s4 = ''
					s5 = ''
					if ent3 > -1:
						if entry_textBox[ent3].get() != '':
							kt = entry_textBox[ent3].get().split(' ')
							if len(kt) > 1:
								for t in range(1, len(kt)):
									s2 = s2 + ' ' + entry_textBox[ent2].get()
							s3 = vuln.name + 'Keywords=(' + entry_textBox[ent3].get()
					if ent4 > -1:
						if entry_textBox[ent4].get() != '':
							s4 = vuln.name + 'ExtraKeywords=(' + entry_textBox[ent4].get()
					if ent5 > -1:
						if entry_textBox[ent5].get() != '':
							s5 = vuln.name + 'Message=(' + entry_textBox[ent5].get()
					vuln.saved = True
					save_entry.append((s1, s2, s3, s4, s5))
				else:
					buff_entry = []
					for n, (s1, s2, s3, s4, s5) in enumerate(save_entry):
						if vuln.name == s1:
							s2 = s2 + ' ' + entry_textBox[ent2].get()
							if s3 != '':
								if entry_textBox[ent3].get() != '':
									kt = entry_textBox[ent3].get().split(' ')
									if len(kt) > 1:
										for t in range(1, len(kt)):
											s2 = s2 + ' ' + entry_textBox[ent2].get()
									s3 = s3 + ' ' + entry_textBox[ent3].get()
							if s4 != '':
								if entry_textBox[ent4].get() != '':
									s4 = s4 + ' ' + entry_textBox[ent4].get()
							if s5 != '':
								if entry_textBox[ent5].get() != '':
									s5 = s5 + ' ' + entry_textBox[ent5].get()
						buff_entry.append((s1, s2, s3, s4, s5))
					save_entry = buff_entry
	for n, (s1, s2, s3, s4, s5) in enumerate(save_entry):
		f.write(s1 + '=(y)\n')
		f.write(s2 + ')\n')
		if s3 != '':
			f.write(s3 + ')\n')
		if s4 != '':
			f.write(s4 + ')\n')
		if s5 != '':
			f.write(s5 + ')\n')
	for vuln in vulns:
		vuln.saved = False
			
	f.close()
	tally()
	
def loadSave():
	content = []
	if os.path.exists('csel.txt'):
		with open('csel.txt') as f:
			content = f.read().splitlines()
		f.close()
	for cont in content:
		if 'Desktop=' in cont:
			usrDsktp.set(cont.replace('Desktop=',''))
		if 'silentMiss=(y)' in cont:
			silentMode.set(1)
		if 'FTPServer=(y)' in cont:
			ftpMode.set(1)
			getFTPInfo()
		if 'forensicsAnswer1=(' in cont:
			fqA1 = cont.replace('forensicsAnswer1=(','')
			fqA1 = fqA1.replace(')','')
			fqans01.set(fqA1)
			cont = fqA1
		if 'checkForensicsQuestion1Value=(' in cont:
			fqP1 = cont.replace('checkForensicsQuestion1Value=(','')
			fqP1 = fqP1.replace(')','')
			fqpts01.set(fqP1)
			fqcb01.set(1)
			cont = fqP1
		if 'forensicsQuestion1=' in cont:
			fQ1 = cont.replace('forensicsQuestion1=','')
			fquest01.set(fQ1)
			cont = fQ1
		if 'forensicsAnswer2=(' in cont:
			fqA2 = cont.replace('forensicsAnswer2=(','')
			fqA2 = fqA2.replace(')','')
			fqans02.set(fqA2)
			cont = fqA2
		if 'checkForensicsQuestion2Value=(' in cont:
			fqP2 = cont.replace('checkForensicsQuestion2Value=(','')
			fqP2 = fqP2.replace(')','')
			fqpts01.set(fqP2)
			fqcb02.set(1)
			cont = fqP2
		if 'forensicsQuestion2=' in cont:
			fQ2 = cont.replace('forensicsQuestion2=','')
			fquest02.set(fQ2)
			cont = fQ2
	for cont in content:
		for vuln in vulns:
			if vuln.name+'=(y)' in cont:
				if vuln.name in vulnNames2:
					addToFrame2(vuln.name)
				elif vuln.name in vulnNames3:
					addToFrame3(vuln.name)
				elif vuln.name in vulnNames4:
					addToFrame4(vuln.name)
				elif vuln.name in vulnNames5:
					addToFrame5(vuln.name)
			elif vuln.name+'Value=(' in cont:
				points = cont.replace(vuln.name+'Value=(','')
				points = points.replace(')','')
				points = points.split(' ')
				value = []
				for x in points:
					if x not in value:
						value.append(x)
				for v in range(1, len(value)):
						if vuln.name in vulnNames3:
							addToFrame3(vuln.name)
						elif vuln.name in vulnNames4:
							addToFrame4(vuln.name)
						elif vuln.name in vulnNames5:
							addToFrame5(vuln.name)
				for v in value:
					test = True
					for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
						if vuln.name == entry_select[number].get():
							if entry_textBox[ent2].get() == v:
								test = False
					if test:
						for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
							if vuln.name == entry_select[number].get():
								if entry_textBox[ent2].get() == '':
									entry_textBox[ent2].set(v)
									break
			elif vuln.name+'Keywords=(' in cont:
				keyWd = cont.replace(vuln.name+'Keywords=(','')
				keyWd = keyWd.replace(')','')
				keyWd = keyWd.split(' ')
				for p in range(len(points)):
					for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
						if vuln.name == entry_select[number].get():
							if points[p] == entry_textBox[ent2].get():
								key = entry_textBox[ent3].get()
								if key == '':
									key = keyWd[p]
								else:
									key = key + ' ' + keyWd[p]
								entry_textBox[ent3].set(key)
			elif vuln.name+'ExtraKeywords=(' in cont:
				exKeyWd = cont.replace(vuln.name+'ExtraKeywords=(','')
				exKeyWd = exKeyWd.replace(')','')
				exKeyWd = exKeyWd.split(' ')
				for p in range(len(points)):
					for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
						if vuln.name == entry_select[number].get():
							if points[p] == entry_textBox[ent2].get():
								key = entry_textBox[ent4].get()
								if key == '':
									key = exKeyWd[p]
								else:
									key = key + ' ' + exKeyWd[p]
								entry_textBox[ent4].set(key)
			elif vuln.name+'Message=(' in cont:
				msg = cont.replace(vuln.name+'Message=(','')
				msg = msg.replace(')','')
				msg = msg.split(' ')
				for p in range(len(points)):
					for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
						if vuln.name == entry_select[number].get():
							if points[p] == entry_textBox[ent2].get():
								key = entry_textBox[ent5].get()
								if key == '':
									key = msg[p]
								else:
									key = key + ' ' + msg[p]
								entry_textBox[ent5].set(key)
	setEntry('')
	tally()

def tally():
	#Set tally scores
	tallyScore = 0
	tallyVuln = 0
	for number, (ent1, ent2, ent3, ent4, ent5, ent6, ent7, frame) in enumerate(all_entries):
	#We do not want to count the points from the goodUser catagory and include the silentMiss
		for vuln in vulns:
			if vuln.name == entry_select[number].get():
				if vuln.name != 'goodUser' and vuln.name not in dontCheck:
					if not ent3 == -1:
						multivuln = entry_textBox[ent3].get()
						multivuln = multivuln.split(' ')
						for mtv in multivuln:
							tallyVuln = tallyVuln + 1
							tallyScore = tallyScore + int(entry_textBox[ent2].get())
					else:
						tallyVuln = tallyVuln + 1
						tallyScore = tallyScore + int(entry_textBox[ent2].get())
	scoreTotal.set("Vulnerablilities: {0}\nTotal Points: {1}".format(str(tallyVuln),str(tallyScore)))

def getFTPInfo():
	if os.path.exists('FTP.txt'):
		with open('FTP.txt') as f:
			content = f.read().splitlines()
		f.close()
		serverName.set(content[0].replace('serverName=', ''))
		userName.set(content[1].replace('userName=', ''))
		password.set(content[2].replace('password=', ''))
	if ftpMode.get() == 1:
		servL.config(state='normal')
		servE.config(state='normal')
		userL.config(state='normal')
		userE.config(state='normal')
		passL.config(state='normal')
		passE.config(state='normal')
	else:
		servL.config(state='disable')
		servE.config(state='disable')
		userL.config(state='disable')
		userE.config(state='disable')
		passL.config(state='disable')
		passE.config(state='disable')

# Global Variables Initiation
all_entries = []
entry_frame2_count = 0
entry_frame3_count = 0
entry_frame4_count = 0
entry_frame5_count = 0
errorFree = True
dupFree = True
all_errors = []
vulnNames2Rem = []
vulnNames2RemD = []
entry_errors = []
entry_select = []
entry_textBox = []
entry_textBox_count = -1
entry_lable = []
entry_lable_count = -1
root = Tk()
root.title('CSEL Setup Tool')
userLoc = IntVar()
usrDsktp = StringVar()
silentMode = IntVar()
ftpMode = IntVar()
ftpFrames = ''
serverName = StringVar()
userName = StringVar()
password = StringVar()
scoreLoc = StringVar()
scoreTotal = StringVar()
scoreTotal.set("Vulnerablilities: 0\nTotal Points: 0")
# Forensic Question stuff
fqcb01 = IntVar()
fqpts01 = IntVar()
fquest01 = StringVar()
fqans01 = StringVar()
fqcb02 = IntVar()
fqpts02 = IntVar()
fquest02 = StringVar()
fqans02 = StringVar()

# GUI Creation
vscrollbar = AutoScrollbar(root)
vscrollbar.grid(row=0, column=1, sticky=N+S)
hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
hscrollbar.grid(row=1, column=0, sticky=E+W)

canvas = Canvas(root, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
canvas.config(scrollregion=canvas.bbox("all"))
vscrollbar.config(command=canvas.yview)
hscrollbar.config(command=canvas.xview)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Frame
frame = Frame(canvas)
frame.grid(row=0, column=0, sticky=W)
# Frame1
frame1 = Frame(canvas)
frame1.grid(row=1, column=0, sticky=W)
# Frame2
frame2 = Frame(canvas)
frame2.grid(row=2, column=0, sticky=W)
# Frame3
frame3 = Frame(canvas)
frame3.grid(row=3, column=0, sticky=W)
# Frame4
frame4 = Frame(canvas)
frame4.grid(row=4, column=0, sticky=W)
# Frame5
frame5 = Frame(canvas)
frame5.grid(row=5, column=0, sticky=W)
# Frame Interface
Button(frame,text='Save',command=saveConfig).grid(row=0,column=1)
Checkbutton(frame,text="Check if this configurator is on the Desktop of the main account.",variable=userLoc).grid(row=0,column=2,sticky=W,columnspan=4)
Button(frame,text='Write to Config',command=submitCallback).grid(row=1,column=1)
Entry(frame,textvariable=usrDsktp).grid(row=1,column=2,columnspan=3,sticky=EW)
Label(frame,text="Enter the user name where\nyou want the information to goto.").grid(row=1,column=4,columnspan=2,sticky=W)
Checkbutton(frame,text=v001.name,variable=silentMode).grid(row=2,column=1,sticky=W)
Label(frame,text=v001.tip).grid(row=2,column=2,columnspan=5,sticky=W)
Checkbutton(frame,text=v002.name,variable=ftpMode,command=getFTPInfo).grid(row=3,column=1,sticky=W)
Label(frame,text=v002.tip).grid(row=3,column=2,columnspan=5,sticky=W)
servL = Label(frame,text='Server Name/IP',state='disable')
servL.grid(row=4,column=1,sticky=E)
servE = Entry(frame,textvariable=serverName,state='disable')
servE.grid(row=4,column=2,sticky=W)
userL = Label(frame,text='User Name',state='disable')
userL.grid(row=4,column=3,sticky=E)
userE = Entry(frame,textvariable=userName,state='disable')
userE.grid(row=4,column=4,sticky=W)
passL = Label(frame,text='Password',state='disable')
passL.grid(row=4,column=5,sticky=E)
passE = Entry(frame,textvariable=password,state='disable')
passE.grid(row=4,column=6,sticky=W)
error = Label(frame,text='Please correct the errors\nbefore proceding',fg='red')
Label(frame,textvariable=scoreTotal,font=('Verdana',10,'bold')).grid(row=5,column=1,sticky=W)
# Frame1 Interface
Label(frame1,text="Create?",font=('Verdana',10,'bold')).grid(row=0,column=1)
Label(frame1,text="Points",font=('Verdana',10,'bold')).grid(row=0,column=2)
Label(frame1,text="Question",font=('Verdana',10,'bold')).grid(row=0,column=3)
Label(frame1,text="Answer",font=('Verdana',10,'bold')).grid(row=0,column=4,sticky=W)
Checkbutton(frame1,text=fq01.name,variable=fqcb01).grid(row=5,column=1,sticky=W)
Entry(frame1,width=5,textvariable=fqpts01).grid(row=5,column=2,sticky=W)
Entry(frame1,textvariable=fquest01).grid(row=5,column=3,sticky=W)
Entry(frame1,textvariable=fqans01).grid(row=5,column=4,sticky=W)
Checkbutton(frame1,text=fq02.name,variable=fqcb02).grid(row=6,column=1,sticky=W)
Entry(frame1,width=5,textvariable=fqpts02).grid(row=6,column=2,sticky=W)
Entry(frame1,textvariable=fquest02).grid(row=6,column=3,sticky=W)
Entry(frame1,textvariable=fqans02).grid(row=6,column=4,sticky=W)
# Frame2 Interface
Button(frame2, text='<Add Entry>', command=lambda: addToFrame2("<Select One>"),width=19).grid(row=0,column=0,sticky=W)
Label(frame2,text="Points",font=('Verdana',10,'bold')).grid(row=0,column=1,sticky=W,padx=5)
Label(frame2,text="Explanation",font=('Verdana',10,'bold')).grid(row=0,column=2,sticky=W)
# Frame3 Interface
Button(frame3, text='<Add Entry>', command=lambda: addToFrame3("<Select One>"),width=19).grid(row=0,column=0,sticky=W)
Label(frame3,text="Points",font=('Verdana',10,'bold')).grid(row=0,column=1,sticky=W,padx=5)
Label(frame3,text="Keywords/Values",font=('Verdana',10,'bold'),width=15).grid(row=0,column=2,sticky=W)
Label(frame3,text="Contents",font=('Verdana',10,'bold'),width=13).grid(row=0,column=3,sticky=W)
Label(frame3,text="Explanation (Add a space in between entries)",font=('Verdana',10,'bold')).grid(row=0,column=4,sticky=W)
# Frame4 Interface
Button(frame4, text='<Add Entry>', command=lambda: addToFrame4("<Select One>"),width=19).grid(row=0,column=0,sticky=W)
Label(frame4,text="Points",font=('Verdana',10,'bold')).grid(row=0,column=1,sticky=W,padx=5)
Label(frame4,text="Keywords/Values",font=('Verdana',10,'bold'),width=15).grid(row=0,column=2,sticky=W)
Label(frame4,text="Keywords/Values",font=('Verdana',10,'bold'),width=20).grid(row=0,column=3,sticky=W)
Label(frame4,text="Contents",font=('Verdana',10,'bold'),width=13).grid(row=0,column=4,sticky=W)
Label(frame4,text="Explanation (Add a space in between entries)",font=('Verdana',10,'bold')).grid(row=0,column=5,sticky=W)
# Frame5 Interface
Button(frame5, text='<Add Entry>', command=lambda: addToFrame5("<Select One>"),width=19).grid(row=0,column=0,sticky=W)
Label(frame5,text="Points",font=('Verdana',10,'bold')).grid(row=0,column=1,sticky=W,padx=5)
Label(frame5,text="Keywords/Values",font=('Verdana',10,'bold'),width=20).grid(row=0,column=2,sticky=W)
Label(frame5,text="Completion Message",font=('Verdana',10,'bold'),width=18).grid(row=0,column=3,sticky=W)
Label(frame5,text="File Location",font=('Verdana',10,'bold'),width=15).grid(row=0,column=4,sticky=W)
# Label(frame5,text="Contents",font=('Verdana',10,'bold'),width=13).grid(row=0,column=5,sticky=W)
Label(frame5,text="Explanation ",font=('Verdana',10,'bold')).grid(row=0,column=6,sticky=W)

loadSave()

frame.update_idletasks()
frame1.update_idletasks()
frame2.update_idletasks()
frame3.update_idletasks()
frame4.update_idletasks()
frame5.update_idletasks()

root.mainloop()
