import os
import time
import json
import shutil
import traceback
import admin_test
from tkinter import *
from tkinter import ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedStyle


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
                canvas.configure(background=root.ttkStyle.lookup(".", "background"))

        canvas.bind('<Configure>', _configure_canvas)


class Config(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        vulnerability_settings.update({"Main Menu": {"Style": StringVar(), "Desktop Checkbox": IntVar(), "Desktop Entry": StringVar(), "Silent Mode": IntVar(), "Server Mode": IntVar(), "Server Name": StringVar(), "Server User Name": StringVar(), "Server Password": StringVar(), "Tally Points": StringVar()}, "Forensic": {"Enabled": IntVar(), "Categories": {"Points": [IntVar()],  "Question": [StringVar()], "Answer": [StringVar()]}, "Location": ['']},
                                       "Account Management": {"Disable Guest": {"Definition": 'Enable this to score the competitor for disabling the Guest account.',
                                                                                "Enabled": IntVar(),
                                                                                "Categories": {'Points': [IntVar()]}},
                                                              "Disable Admin": {"Definition": 'Enable this to score the competitor for disabling the Administrator account.',
                                                                                "Enabled": IntVar(),
                                                                                "Categories": {'Points': [IntVar()]}},
                                                              "Keep User": {"Definition": 'Enable this to penalize the competitor for removing a user.',
                                                                            "Modify Definition": 'This will penalize the competitor for removing a user. To add more users press the "Add" button. To remove a user press the "X" button next to the user you want to remove. Keep it one user per line. Do not make the point value negative.',
                                                                            "Enabled": IntVar(),
                                                                            "Categories": {'Points': [IntVar()], 'User Name': [StringVar()]}},
                                                              "Add Admin": {"Definition": 'Enable this to score the competitor for elevating a user to an Administrator.',
                                                                            "Modify Definition": 'This will score the competitor for elevating a user to an Administrator. To add more users press the "Add" button. To remove a user press the "X" button next to the user you want to remove. Keep it one user per line.',
                                                                            "Enabled": IntVar(),
                                                                            "Categories": {'Points': [IntVar()], 'User Name': [StringVar()]}},
                                                              "Remove Admin": {"Definition": 'Enable this to score the competitor for demoting a user to Standard user.',
                                                                               "Modify Definition": 'This will score the competitor for demoting a user to Standard user. To add more users press the "Add" button. To remove a user press the "X" button next to the user you want to remove. Keep it one user per line.',
                                                                               "Enabled": IntVar(),
                                                                               "Categories": {'Points': [IntVar()], 'User Name': [StringVar()]}},
                                                              "Add User": {"Definition": 'Enable this to score the competitor for adding a user.',
                                                                           "Modify Definition": 'This will score the competitor for adding a user. To add more users press the "Add" button. To remove a user press the "X" button next to the user you want to remove. Keep it one user per line.',
                                                                           "Enabled": IntVar(),
                                                                           "Categories": {'Points': [IntVar()], 'User Name': [StringVar()]}},
                                                              "Remove User": {"Definition": 'Enable this to score the competitor for removing a user.',
                                                                              "Modify Definition": 'This will score the competitor for removing a user. To add more users press the "Add" button. To remove a user press the "X" button next to the user you want to remove. Keep it one user per line.',
                                                                              "Enabled": IntVar(),
                                                                              "Categories": {'Points': [IntVar()], 'User Name': [StringVar()]}},
                                                              "User Change Password": {"Definition": 'Enable this to score the competitor for changing a users password.',
                                                                                       "Modify Definition": 'This will score the competitor for changing a users password. To add more users press the "Add" button. To remove a user press the "X" button next to the user you want to remove. Keep it one user per line.',
                                                                                       "Enabled": IntVar(),
                                                                                       "Categories": {'Points': [IntVar()], 'User Name': [StringVar()]}},
                                                              "Add User to Group": {"Definition": 'Enable this to score the competitor for adding a user to a group other than the Administrative group.',
                                                                                    "Modify Definition": 'This will score the competitor for adding a user to a group other than the Administrative group. To add more users press the "Add" button. To remove a user press the "X" button next to the user you want to remove. Keep it one user  and group per line.',
                                                                                    "Enabled": IntVar(),
                                                                                    "Categories": {'Points': [IntVar()], 'User Name': [StringVar()], 'Group Name': [StringVar()]}},
                                                              "Remove User from Group": {"Definition": 'Enable this to score the competitor for removing a user from a group other than the Administrative group.',
                                                                                         "Modify Definition": 'This will score the competitor for removing a user from a group other than the Administrative group. To add more users press the "Add" button. To remove a user press the "X" button next to the user you want to remove. Keep it one user and group per line.',
                                                                                         "Enabled": IntVar(),
                                                                                         "Categories": {'Points': [IntVar()], 'User Name': [StringVar()], 'Group Name': [StringVar()]}}},
                                       "Local Policy Options": {"Do Not Require CTRL_ALT_DEL": {"Definition": 'Enable this to score the competitor for disabling Do Not Require CTRL_ALT_DEL.',
                                                                                                "Enabled": IntVar(),
                                                                                                "Categories": {'Points': [IntVar()]}},
                                                                "Turn On Firewall": {"Definition": 'Enable this to score the competitor for turning on the firewall.',
                                                                                     "Enabled": IntVar(),
                                                                                     "Categories": {'Points': [IntVar()]}},
                                                                "Don't Display Last User": {"Definition": 'Enable this to score the competitor for enabling Don\'t Display Last User.',
                                                                                            "Enabled": IntVar(),
                                                                                            "Categories": {'Points': [IntVar()]}}},
                                       "Local Policy Password": {"Minimum Password Age": {"Definition": 'Enable this to score the competitor for setting the minimum password age to 30, 45, or 60.',
                                                                                          "Enabled": IntVar(),
                                                                                          "Categories": {'Points': [IntVar()]}},
                                                                 "Maximum Password Age": {"Definition": 'Enable this to score the competitor for setting the maximum password age to 60, 75, or 90.',
                                                                                          "Enabled": IntVar(),
                                                                                          "Categories": {'Points': [IntVar()]}},
                                                                 "Minimum Password Length": {"Definition": 'Enable this to score the competitor for setting the minimum password length between 10 and 20.',
                                                                                             "Enabled": IntVar(),
                                                                                             "Categories": {'Points': [IntVar()]}},
                                                                 "Maximum Login Tries": {"Definition": 'Enable this to score the competitor for setting the maximum login tries between 5 and 10.',
                                                                                         "Enabled": IntVar(),
                                                                                         "Categories": {'Points': [IntVar()]}},
                                                                 "Lockout Duration": {"Definition": 'Enable this to score the competitor for setting the lockout duration to 30.',
                                                                                      "Enabled": IntVar(),
                                                                                      "Categories": {'Points': [IntVar()]}},
                                                                 "Lockout Reset Duration": {"Definition": 'Enable this to score the competitor for setting the lockout reset duration to 30.',
                                                                                            "Enabled": IntVar(),
                                                                                            "Categories": {'Points': [IntVar()]}},
                                                                 "Password History": {"Definition": 'Enable this to score the competitor for setting the password history between 5 and 10.',
                                                                                      "Enabled": IntVar(),
                                                                                      "Categories": {'Points': [IntVar()]}},
                                                                 "Password Complexity": {"Definition": 'Enable this to score the competitor for enabling password complexity.',
                                                                                         "Enabled": IntVar(),
                                                                                         "Categories": {'Points': [IntVar()]}},
                                                                 "Reversible Password Encryption": {"Definition": 'Enable this to score the competitor for disabling reversible encryption.',
                                                                                                    "Enabled": IntVar(),
                                                                                                    "Categories": {'Points': [IntVar()]}}},
                                       "Local Policy Audit": {"Audit Account Login": {"Definition": 'Enable this to score the competitor for setting account login audit to success and failure.',
                                                                                      "Enabled": IntVar(),
                                                                                      "Categories": {'Points': [IntVar()]}},
                                                              "Audit Account Management": {"Definition": 'Enable this to score the competitor for setting account management audit to success and failure.',
                                                                                           "Enabled": IntVar(),
                                                                                           "Categories": {'Points': [IntVar()]}},
                                                              "Audit Directory Settings Access": {"Definition": 'Enable this to score the competitor for setting directory settings access audit to success and failure.',
                                                                                                  "Enabled": IntVar(),
                                                                                                  "Categories": {'Points': [IntVar()]}},
                                                              "Audit Logon Events": {"Definition": 'Enable this to score the competitor for setting login events audit to success and failure.',
                                                                                     "Enabled": IntVar(),
                                                                                     "Categories": {'Points': [IntVar()]}},
                                                              "Audit Object Access": {"Definition": 'Enable this to score the competitor for setting object access audit to success and failure.',
                                                                                      "Enabled": IntVar(),
                                                                                      "Categories": {'Points': [IntVar()]}},
                                                              "Audit Policy Change": {"Definition": 'Enable this to score the competitor for setting policy change audit to success and failure.',
                                                                                      "Enabled": IntVar(),
                                                                                      "Categories": {'Points': [IntVar()]}},
                                                              "Audit Privilege Use": {"Definition": 'Enable this to score the competitor for setting privilege use audit to success and failure.',
                                                                                      "Enabled": IntVar(),
                                                                                      "Categories": {'Points': [IntVar()]}},
                                                              "Audit Process Tracking": {"Definition": 'Enable this to score the competitor for setting process tracking audit to success and failure.',
                                                                                         "Enabled": IntVar(),
                                                                                         "Categories": {'Points': [IntVar()]}},
                                                              "Audit System Events": {"Definition": 'Enable this to score the competitor for setting system events audit to success and failure.',
                                                                                      "Enabled": IntVar(),
                                                                                      "Categories": {'Points': [IntVar()]}}},
                                       "Program Management": {"Good Program": {"Definition": 'Enable this to score the competitor for installing a program.',
                                                                               "Modify Definition": 'This will score the competitor for installing a program. To add more programs press the "Add" button. To remove a program press the "X" button next to the program you want to remove. Keep it one program per line.',
                                                                               "Enabled": IntVar(),
                                                                               "Categories": {'Points': [IntVar()], 'Program Name': [StringVar()]}},
                                                              "Bad Program": {"Definition": 'Enable this to score the competitor for uninstalling a program.',
                                                                              "Modify Definition": 'This will score the competitor for uninstalling a program. To add more programs press the "Add" button. To remove a program press the "X" button next to the program you want to remove. Keep it one program per line.',
                                                                              "Enabled": IntVar(),
                                                                              "Categories": {'Points': [IntVar()], 'Program Name': [StringVar()]}},
                                                              "Update Program": {"Definition": '(WIP)Enable this to score the competitor for updating a program.',
                                                                                 "Modify Definition": '(WIP)This will score the competitor for updating a program. To add more programs press the "Add" button. To remove a program press the "X" button next to the program you want to remove. Keep it one program per line.',
                                                                                 "Enabled": IntVar(),
                                                                                 "Categories": {'Points': [IntVar()], 'Program Name': [StringVar()]}},
                                                              "Add Feature": {"Definition": '(WIP)Enable this to score the competitor for adding a feature.',
                                                                              "Modify Definition": '(WIP)This will score the competitor for adding a feature. To add more features press the "Add" button. To remove a feature press the "X" button next to the feature you want to remove. Keep it one feature per line.',
                                                                              "Enabled": IntVar(),
                                                                              "Categories": {'Points': [IntVar()], 'Feature Name': [StringVar()]}},
                                                              "Remove Feature": {"Definition": '(WIP)Enable this to score the competitor for removing a feature.',
                                                                                 "Modify Definition": '(WIP)This will score the competitor for removing a feature. To add more features press the "Add" button. To remove a feature press the "X" button next to the feature you want to remove. Keep it one feature per line.',
                                                                                 "Enabled": IntVar(),
                                                                                 "Categories": {'Points': [IntVar()], 'Feature Name': [StringVar()]}},
                                                              "Services": {"Definition": 'Enable this to score the competitor for modifying a services run ability.',
                                                                           "Modify Definition": 'This will score the competitor for modifying a services run ability. To add more services press the "Add" button. To remove a service press the "X" button next to the service you want to remove. Keep it one service per line.',
                                                                           "Enabled": IntVar(),
                                                                           "Categories": {'Points': [IntVar()], 'Service Name': [StringVar()], 'Service Status': [StringVar()], 'Service Start Type': [StringVar()]}}},
                                       "File Management": {"Bad File": {"Definition": 'Enable this to score the competitor for deleting a file.',
                                                                        "Modify Definition": 'This will score the competitor for deleting a file. To add more files press the "Add" button. To remove a file press the "X" button next to the file you want to remove. Keep it one file per line.',
                                                                        "Enabled": IntVar(),
                                                                        "Categories": {'Points': [IntVar()], 'File Path': [StringVar()]}},
                                                           "Check Hosts": {"Definition": '(WIP)Enable this to score the competitor for clearing the hosts file.',
                                                                           "Modify Definition": '(WIP)This will score the competitor for clearing the hosts file. To add more files press the "Add" button. To remove a file press the "X" button next to the file you want to remove. Keep it one file per line.',
                                                                           "Enabled": IntVar(),
                                                                           "Categories": {'Points': [IntVar()], 'Text': [StringVar()]}},
                                                           "Add Text to File": {"Definition": 'Enable this to score the competitor for adding text to a file.',
                                                                                "Modify Definition": 'This will score the competitor for adding text to a file. To add more files press the "Add" button. To remove a file press the "X" button next to the file you want to remove. Keep it one file per line.',
                                                                                "Enabled": IntVar(),
                                                                                "Categories": {'Points': [IntVar()], 'Text to Add': [StringVar()], 'File Path': [StringVar()]}},
                                                           "Remove Text From File": {"Definition": 'Enable this to score the competitor for removing text from a file.',
                                                                                     "Modify Definition": 'This will score the competitor for removing text from a file. To add more files press the "Add" button. To remove a file press the "X" button next to the file you want to remove. Keep it one file per line.',
                                                                                     "Enabled": IntVar(),
                                                                                     "Categories": {'Points': [IntVar()], 'Text to Remove': [StringVar()], 'File Path': [StringVar()]}},
                                                           "File Permissions": {"Definition": '(WIP)Enable this to score the competitor for changing the permissions a user has on a file.',
                                                                                "Modify Definition": '(WIP)This will score the competitor for changing the permissions a user has on a file. To add more files press the "Add" button. To remove a file press the "X" button next to the file you want to remove. Keep it one file per line.',
                                                                                "Enabled": IntVar(),
                                                                                "Categories": {'Points': [IntVar()], 'Users to Modify': [StringVar()], 'Permission to Set': [StringVar()], 'File Path': [StringVar()]}}},
                                       "Miscellaneous": {"Anti-Virus": {"Definition": 'Enable this to score the competitor for installing an anti-virus. Not windows defender.',
                                                                        "Enabled": IntVar(),
                                                                        "Categories": {'Points': [IntVar()]}},
                                                         "Update Check Period": {"Definition": '(WIP)Enable this to score the competitor for setting the period windows checks for updates to once a week.',
                                                                                 "Enabled": IntVar(),
                                                                                 "Categories": {'Points': [IntVar()]}},
                                                         "Update Auto Install": {"Definition": '(WIP)Enable this to score the competitor for setting windows updates to automatically install updates.',
                                                                                 "Enabled": IntVar(),
                                                                                 "Categories": {'Points': [IntVar()]}},
                                                         "Task Scheduler": {"Definition": '(WIP)Enable this to score the competitor for removing a task from the task scheduler.',
                                                                            "Modify Definition": '(WIP)This will score the competitor for removing a task from the task scheduler. To add more tasks press the "Add" button. To remove a task press the "X" button next to the task you want to remove. Keep it one task per line.',
                                                                            "Enabled": IntVar(),
                                                                            "Categories": {'Points': [IntVar()], 'Task Name': [StringVar()]}},
                                                         "Check Startup": {"Definition": '(WIP)Enable this to score the competitor for removing or disabling a program from the startup.',
                                                                           "Modify Definition": '(WIP)This will score the competitor for removing or disabling a program from the startup. To add more programs press the "Add" button. To remove a program press the "X" button next to the program you want to remove. Keep it one program per line.',
                                                                           "Enabled": IntVar(),
                                                                           "Categories": {'Points': [IntVar()], 'Program Name': [StringVar()]}}}})
        vulnerability_settings["Main Menu"]["Tally Points"].set("Vulnerabilities: 0 Total Points: 0")

        nb = ttk.Notebook(self)
        MainPage = ttk.Frame(nb)

        ttk.Button(MainPage, text='Save', command=lambda: (save_config())).grid(sticky=EW)
        ttk.Checkbutton(MainPage, text="Check if this configurator is on the Desktop of the main account.", variable=vulnerability_settings["Main Menu"]["Desktop Checkbox"], command=lambda: (set_desktop())).grid(row=0, column=1, sticky=W, columnspan=3)
        ttk.OptionMenu(MainPage, vulnerability_settings["Main Menu"]["Style"], *themeList).grid(row=0, column=5, sticky=EW)
        ttk.Button(MainPage, text='Set', width=5, command=lambda: (change_theme())).grid(row=0, column=6)
        ttk.Button(MainPage, text='Commit', command=lambda: (commit_config())).grid(row=1, sticky=EW)
        ttk.Entry(MainPage, textvariable=vulnerability_settings["Main Menu"]["Desktop Entry"]).grid(row=1, column=1, columnspan=3, sticky=EW)
        ttk.Label(MainPage, text="Enter the user name where you want the information to goto.").grid(row=1, column=4, columnspan=3, sticky=W)
        ttk.Checkbutton(MainPage, text='Silent Miss', variable=vulnerability_settings["Main Menu"]["Silent Mode"]).grid(row=2, sticky=W)
        ttk.Label(MainPage, text='Check this box to hide missed items (Similar to competition)').grid(row=2, column=1, columnspan=5, sticky=W)
        ttk.Checkbutton(MainPage, text='Server Mode', variable=vulnerability_settings["Main Menu"]["Server Mode"], command=lambda: (serverL.configure(state='enable'), serverE.configure(state='enable'), userL.configure(state='enable'), userE.configure(state='enable'), passL.configure(state='enable'), passE.configure(state='enable'))).grid(row=3, sticky=W)
        ttk.Label(MainPage, text='Check this box to enable an FTP server to save the scores (Similar to competition)').grid(row=3, column=1, columnspan=5, sticky=W)
        serverL = ttk.Label(MainPage, text='Server Name/IP', state='disable')
        serverL.grid(row=4, sticky=E)
        serverE = ttk.Entry(MainPage, textvariable=vulnerability_settings["Main Menu"]["Server Name"], state='disable')
        serverE.grid(row=4, column=1, sticky=EW)
        userL = ttk.Label(MainPage, text='User Name', state='disable')
        userL.grid(row=4, column=2, sticky=E)
        userE = ttk.Entry(MainPage, textvariable=vulnerability_settings["Main Menu"]["Server User Name"], state='disable')
        userE.grid(row=4, column=3, sticky=EW)
        passL = ttk.Label(MainPage, text='Password', state='disable')
        passL.grid(row=4, column=4, sticky=E)
        passE = ttk.Entry(MainPage, textvariable=vulnerability_settings["Main Menu"]["Server Password"], state='disable')
        passE.grid(row=4, column=5, sticky=EW)
        ttk.Label(MainPage, textvariable=vulnerability_settings["Main Menu"]["Tally Points"], font='Verdana 10 bold', wraplength=150).grid(row=5)

        ForensicsPage = VerticalScrolledFrame(nb)
        ForensicsPageIn = ForensicsPage.interior
        ForensicsPageIn.grid_columnconfigure(1, weight=1)
        ForensicsPageIn.grid_columnconfigure(2, weight=1)
        ttk.Button(ForensicsPageIn, text="Add", command=lambda: add_row(ForensicsPageIn, vulnerability_settings["Forensic"]["Categories"], widgetDict["Forensic"], 3)).grid(row=0, column=0, sticky=EW)
        ttk.Label(ForensicsPageIn, text='This section is for scoring forensic questions. To score a forensic question be sure to check "Enable". To add more questions press the "Add" button. To remove questions press the "X" button next to the question you want to remove. \nDo note that the answers are case sensitive.').grid(row=0, column=1, rowspan=2, columnspan=3)
        ttk.Checkbutton(ForensicsPageIn, text="Enable", variable=vulnerability_settings["Forensic"]["Enabled"]).grid(row=1, column=0)
        ttk.Label(ForensicsPageIn, text="Points", font='Verdana 10 bold').grid(row=2, column=0)
        ttk.Label(ForensicsPageIn, text="Question", font='Verdana 10 bold').grid(row=2, column=1)
        ttk.Label(ForensicsPageIn, text="Answer", font='Verdana 10 bold').grid(row=2, column=2)
        ttk.Entry(ForensicsPageIn, width=5, textvariable=vulnerability_settings["Forensic"]["Categories"]["Points"][0]).grid(row=3, column=0)
        ttk.Entry(ForensicsPageIn, textvariable=vulnerability_settings["Forensic"]["Categories"]["Question"][0]).grid(row=3, column=1, sticky=EW)
        ttk.Entry(ForensicsPageIn, textvariable=vulnerability_settings["Forensic"]["Categories"]["Answer"][0]).grid(row=3, column=2, sticky=EW)
        ttk.Button(ForensicsPageIn, text='X', command=lambda: remove_row(0, vulnerability_settings["Forensic"]["Categories"], widgetDict["Forensic"])).grid(row=3, column=3)
        widgetDict["Forensic"].update({0: ForensicsPageIn.grid_slaves(row=3)})

        UserPolicyPage = VerticalScrolledFrame(nb)
        UserPolicyPageIn = UserPolicyPage.interior
        UserPolicyPageIn.grid_columnconfigure(1, weight=1)
        ttk.Label(UserPolicyPageIn, text='This section is for scoring user policies. The options that will take multiple test points can be setup by clicking the "Modify" button. Once the "Modify" button is clicked that option will automatically be enabled. Make sure the option is enabled and the points are set for the options you want scored.', padding='10 5').grid(row=0, column=0, columnspan=3)
        ttk.Label(UserPolicyPageIn, text='Account Management', font='Verdana 10').grid(row=1, column=0, stick=W)
        ttk.Label(UserPolicyPageIn, text="Points", font='Verdana 10 bold').grid(row=1, column=2, stick=W)
        for i, t in enumerate(vulnerability_settings["Account Management"].keys()):
            self.add_option(UserPolicyPageIn, vulnerability_settings["Account Management"][t], t, i + 2, nb)

        LocalPolicyPage = VerticalScrolledFrame(nb)
        LocalPolicyPageIn = LocalPolicyPage.interior
        LocalPolicyPageIn.grid_columnconfigure(1, weight=1)
        ttk.Label(LocalPolicyPageIn, text='This section is for scoring Local Security Policies. Each option has a defined range that they be testing listed in their description. Make sure the option is enabled and the points are set for the options you want scored.', padding='10 5').grid(row=0, column=0, columnspan=3)
        ttk.Label(LocalPolicyPageIn, text='Local Security Policy Password', font='Verdana 10').grid(row=1, column=0, stick=W)
        ttk.Label(LocalPolicyPageIn, text="Points", font='Verdana 10 bold').grid(row=1, column=2, stick=W)
        for i, t in enumerate(vulnerability_settings["Local Policy Password"].keys()):
            self.add_option(LocalPolicyPageIn, vulnerability_settings["Local Policy Password"][t], t, i + 2, nb)
            l = i + 3
        ttk.Label(LocalPolicyPageIn, text='Local Security Policy Audit', font='Verdana 10').grid(row=l, column=0, stick=W)
        ttk.Label(LocalPolicyPageIn, text="Points", font='Verdana 10 bold').grid(row=l, column=2, stick=W)
        for i, t in enumerate(vulnerability_settings["Local Policy Audit"].keys()):
            self.add_option(LocalPolicyPageIn, vulnerability_settings["Local Policy Audit"][t], t, i + l + 1, nb)
            l = i + l + 2
        ttk.Label(LocalPolicyPageIn, text='Local Security Policy Options', font='Verdana 10').grid(row=l, column=0, stick=W)
        ttk.Label(LocalPolicyPageIn, text="Points", font='Verdana 10 bold').grid(row=l, column=2, stick=W)
        for i, t in enumerate(vulnerability_settings["Local Policy Options"].keys()):
            self.add_option(LocalPolicyPageIn, vulnerability_settings["Local Policy Options"][t], t, i + l + 1, nb)

        ProgramFilePage = VerticalScrolledFrame(nb)
        ProgramFilePageIn = ProgramFilePage.interior
        ProgramFilePageIn.grid_columnconfigure(1, weight=1)
        ttk.Label(ProgramFilePageIn, text='This section is for scoring program and file manipulation. The options that will take multiple test points can be setup by clicking the "Modify" button. Once the "Modify" button is clicked that option will automatically be enabled. Make sure the option is enabled and the points are set for the options you want scored.', padding='10 5').grid(row=0, column=0, columnspan=3)
        ttk.Label(ProgramFilePageIn, text='Programs', font='Verdana 10').grid(row=1, column=0, stick=W)
        ttk.Label(ProgramFilePageIn, text="Modify", font='Verdana 10 bold').grid(row=1, column=2, stick=W)
        for i, t in enumerate(vulnerability_settings["Program Management"].keys()):
            self.add_option(ProgramFilePageIn, vulnerability_settings["Program Management"][t], t, i + 2, nb)
            l = i + 3
        ttk.Label(ProgramFilePageIn, text='Files', font='Verdana 10').grid(row=l, column=0, stick=W)
        ttk.Label(ProgramFilePageIn, text="Modify", font='Verdana 10 bold').grid(row=l, column=2, stick=W)
        for i, t in enumerate(vulnerability_settings["File Management"].keys()):
            self.add_option(ProgramFilePageIn, vulnerability_settings["File Management"][t], t, i + l + 1, nb)

        MiscellaneousPage = VerticalScrolledFrame(nb)
        MiscellaneousPageIn = MiscellaneousPage.interior
        MiscellaneousPageIn.grid_columnconfigure(1, weight=1)
        ttk.Label(MiscellaneousPageIn, text='This section is for scoring the options that do not fit into and of the other or multiple catagories. The options that will take multiple test points can be setup by clicking the "Modify" button. Once the "Modify" button is clicked that option will automatically be enabled. Make sure the option is enabled and the points are set for the options you want scored.', padding='10 5').grid(row=0, column=0, columnspan=3)
        ttk.Label(MiscellaneousPageIn, text='Miscellaneous', font='Verdana 10').grid(row=1, column=0, stick=W)
        ttk.Label(MiscellaneousPageIn, text="Points", font='Verdana 10 bold').grid(row=1, column=2, stick=W)
        for i, t in enumerate(vulnerability_settings["Miscellaneous"].keys()):
            self.add_option(MiscellaneousPageIn, vulnerability_settings["Miscellaneous"][t], t, i + 2, nb)

        ReportPage = VerticalScrolledFrame(nb)
        ReportPageIn = ReportPage.interior
        ttk.Button(ReportPageIn, text='Export to csv').grid(row=0, column=0, stick=EW)
        ttk.Button(ReportPageIn, text='Export to HTML').grid(row=1, column=0, stick=EW)
        ttk.Button(ReportPageIn, text='Generate', command=lambda: (self.generate_report(ReportPageIn))).grid(row=2, column=0, stick=EW)
        ttk.Label(ReportPageIn, text='This section is for reviewing the options that will be scored. To view the report press the "Generate" button. To export this report to a .csv file press the "Export to CSV" button(WIP). To export this report to a web page press the "Export to HTML" button(WIP).').grid(row=0, column=1, rowspan=3, columnspan=4)

        nb.add(MainPage, text='Main Page')
        nb.add(ForensicsPage, text='Forensics')
        nb.add(UserPolicyPage, text='User Policy')
        nb.add(LocalPolicyPage, text='Local Policy')
        nb.add(ProgramFilePage, text='Programs and Files')
        nb.add(MiscellaneousPage, text='Miscellaneous')
        nb.add(ReportPage, text='Report')

        nb.pack(expand=1, fill="both")
        load_config(ForensicsPageIn)

    def add_option(self, frame, entry, name, row, return_frame):
        ttk.Checkbutton(frame, text=name, variable=entry["Enabled"]).grid(row=row, column=0, stick=W)
        ttk.Label(frame, text=entry["Definition"]).grid(row=row, column=1, stick=W)
        if len(entry["Categories"]) > 1:
            ttk.Button(frame, text='Modify', command=lambda: self.modify_settings(name, entry, return_frame)).grid(row=row, column=2)
        else:
            ttk.Entry(frame, width=5, textvariable=entry["Categories"]["Points"][0]).grid(row=row, column=2)

    def modify_settings(self, option, entry, packing):
        self.pack_slaves()[0].pack_forget()
        modifyPage = VerticalScrolledFrame(self)
        modifyPage.pack(expand=1, fill="both")
        modifyPageIn = modifyPage.interior
        if entry["Enabled"].get() != 1:
            entry["Enabled"].set(1)
        if len(widgetDict["Modify"]) > 0:
            for i in widgetDict["Modify"]:
                for t in widgetDict["Modify"][i]:
                    t.destroy()
            widgetDict["Modify"].clear()
        ttk.Button(modifyPageIn, text="Save", command=lambda: (self.pack_slaves()[0].pack_forget(), packing.pack(expand=1, fill="both"))).grid(row=0, column=0, sticky=EW)
        ttk.Label(modifyPageIn, text=option + ' Modification', font='Verdana 15').grid(row=0, column=1, columnspan=len(entry["Categories"]))
        ttk.Button(modifyPageIn, text="Add", command=lambda: (add_row(modifyPageIn, entry["Categories"], widgetDict["Modify"], 3))).grid(row=1, column=0, sticky=EW)
        ttk.Label(modifyPageIn, text=entry["Modify Definition"], wraplength=int(self.winfo_screenwidth() * 2 / 3 - 100)).grid(row=1, column=1, columnspan=len(entry["Categories"]))
        for i, t in enumerate(entry["Categories"]):
            ttk.Label(modifyPageIn, text=t, font='Verdana 10 bold').grid(row=2, column=i)
        for i in range(len(entry["Categories"]["Points"])):
            if entry["Categories"]["Points"][i] != 0:
                for r, t in enumerate(entry["Categories"]):
                    if t == "Points":
                        ttk.Entry(modifyPageIn, width=5, textvariable=entry["Categories"]["Points"][i]).grid(row=i + 3, column=r)
                    elif t == "File Path":
                        modifyPageIn.grid_columnconfigure(r, weight=1)
                        ttk.Entry(modifyPageIn, textvariable=entry["Categories"][t][i]).grid(row=i + 3, column=r, sticky=EW)
                        ttk.Button(modifyPageIn, text='...', command=lambda: entry["Categories"][t][i].set(filedialog.askdirectory())).grid(row=i + 3, column=r + 1)
                        c = r + 2
                    elif t == "Service Status":
                        ttk.OptionMenu(modifyPageIn, entry["Categories"][t][i], *["Running", "Stopped"]).grid(row=i + 3, column=r, sticky=EW)
                        c = r + 1
                    elif t == "Service Start Type":
                        ttk.OptionMenu(modifyPageIn, entry["Categories"][t][i], *["Automatic", "Manual", "Disabled"]).grid(row=i + 3, column=r, sticky=EW)
                        c = r + 1
                    else:
                        ttk.Entry(modifyPageIn, textvariable=entry["Categories"][t][i]).grid(row=i + 3, column=r, sticky=EW)
                        c = r + 1
                ttk.Button(modifyPageIn, text='X', command=lambda: remove_row(i, entry["Categories"], widgetDict["Modify"])).grid(row=i + 3, column=c, sticky=W)
                widgetDict["Modify"].update({i: modifyPageIn.grid_slaves(row=i + 3)})

    def generate_report(self, frame):
        for i in widgetDict["Report"]:
            i.destroy()
        widgetDict["Report"] = []
        wrap = int(self.winfo_screenwidth() * 2 / 3 / 5) - 86
        final_row = 4
        for s in vulnerability_settings.keys():
            tested = False
            if s != "Main Menu":
                ttk.Separator(frame, orient=HORIZONTAL).grid(row=final_row, column=0, columnspan=5, sticky=EW)
                final_row += 1
                if s == "Forensic":
                    if vulnerability_settings[s]["Enabled"].get() == 1:
                        set_first_row = final_row
                        row_span = 0
                        for i, c in enumerate(vulnerability_settings[s]["Categories"]):
                            for srow, settings in enumerate(vulnerability_settings[s]["Categories"][c]):
                                if settings != 0:
                                    tested = True
                                    ttk.Label(frame, text=settings.get()).grid(row=srow * 2 + set_first_row + 1, column=i + 2)
                                    ttk.Separator(frame, orient=HORIZONTAL).grid(row=srow * 2 + set_first_row + 2, column=2, columnspan=3, sticky=EW)
                                    row_span = srow * 2 + 2
                            if tested:
                                ttk.Label(frame, text=c).grid(row=set_first_row, column=i + 2)
                                final_row = set_first_row + row_span
                        if tested:
                            ttk.Label(frame, text=s, wraplength=wrap).grid(row=set_first_row, column=1, rowspan=row_span)
                else:
                    set_first_row = final_row
                    row_span = 0
                    for o in vulnerability_settings[s].keys():
                        if vulnerability_settings[s][o]["Enabled"].get() == 1:
                            tested = True
                            temp_row = final_row
                            temp_count = 0
                            temp_row_span = 0
                            for i, c in enumerate(vulnerability_settings[s][o]["Categories"].keys()):
                                ttk.Label(frame, text=c, wraplength=wrap).grid(row=temp_row, column=i + 2)
                                for e, settings in enumerate(vulnerability_settings[s][o]["Categories"][c]):
                                    if settings != 0:
                                        ttk.Label(frame, text=settings.get(), wraplength=wrap).grid(row=e * 2 + temp_row + 1, column=i + 2)
                                        ttk.Separator(frame, orient=HORIZONTAL).grid(row=e * 2 + temp_row + 2, column=2, columnspan=3, sticky=EW)
                                        final_row = e * 2 + temp_row + 2
                                        temp_row_span = e + 2
                                        temp_count = e
                            row_span += temp_row_span + temp_count + 1
                            ttk.Label(frame, text=o, wraplength=wrap).grid(row=temp_row, column=1, rowspan=temp_row_span * 2 - 2)
                            ttk.Separator(frame, orient=HORIZONTAL).grid(row=temp_row - 1, column=1, columnspan=4, sticky=EW)
                            final_row += 1
                    if tested:
                        ttk.Label(frame, text=s, wraplength=wrap).grid(row=set_first_row, column=0, rowspan=row_span - 1)
                        final_row -= 1
                if not tested:
                    final_row -= 1
        for i in range(4, final_row):
            for w in frame.grid_slaves(row=i):
                widgetDict["Report"].append(w)
        tally()


def change_theme():
    root.ttkStyle.set_theme(vulnerability_settings["Main Menu"]["Style"].get())


def add_row(frame, entry, widgets, default_row):
    test = True
    rwl = 0
    while test:
        if rwl not in widgets.keys():
            test = False
        else:
            rwl += 1
    if len(widgets) > 0:
        i = 0
        for w in widgets:
            if widgets[w][0].grid_info()['row'] > i:
                tempr = widgets[w][0].grid_info()['row'] + 1
    else:
        tempr = default_row
    if rwl == len(widgets) and rwl != 0:
        for i in entry:
            if i == "Points":
                entry[i].append(IntVar())
            else:
                entry[i].append(StringVar())
    else:
        for i in entry:
            if i == "Points":
                entry[i][rwl] = IntVar()
            else:
                entry[i][rwl] = StringVar()

    for i, t in enumerate(entry):
        if t == "Points":
            ttk.Entry(frame, width=5, textvariable=entry["Points"][rwl]).grid(row=tempr, column=i)
        elif t == "File Path":
            frame.grid_columnconfigure(i, weight=1)
            ttk.Entry(frame, textvariable=entry[t][rwl]).grid(row=tempr, column=i, sticky=EW)
            ttk.Button(frame, text='...', command=lambda: entry[t][rwl].set(filedialog.askdirectory())).grid(row=tempr, column=i + 1)
            c = i + 2
        elif t == "Service Status":
            ttk.OptionMenu(frame, entry[t][rwl], *["Running", "Stopped"]).grid(row=tempr, column=i, sticky=EW)
            c = i + 1
        elif t == "Service Start Type":
            ttk.OptionMenu(frame, entry[t][rwl], *["Automatic", "Manual", "Disabled"]).grid(row=tempr, column=i, sticky=EW)
            c = i + 1
        else:
            ttk.Entry(frame, textvariable=entry[t][rwl]).grid(row=tempr, column=i, sticky=EW)
            c = i + 1
    ttk.Button(frame, text='X', command=lambda: remove_row(rwl, entry, widgets)).grid(row=tempr, column=c, sticky=W)
    widgets.update({rwl: frame.grid_slaves(row=tempr)})


def remove_row(rem, entry, widgets):
    for i in entry:
        entry[i][rem] = 0
    rem_row = widgets[rem][0].grid_info()['row']
    for w in widgets[rem]:
        w.destroy()
    for i in widgets:
        if i != rem and widgets[i][0].grid_info()['row'] > rem_row:
            tempr = widgets[i][0].grid_info()['row'] - 1
            for r in widgets[i]:
                r.grid_configure(row=tempr)
    del widgets[rem]


def create_forensic():
    qHeader = 'This is a forensics question. Answer it below\n------------------------\n'
    qFooter = '\n\nANSWER: <TypeAnswerHere>'
    if vulnerability_settings["Forensic"]["Enabled"].get() == 1:
        for i, q in enumerate(vulnerability_settings["Forensic"]["Categories"]["Question"]):
            if q != 0 and q.get() != '':
                g = open((str(vulnerability_settings["Main Menu"]["Desktop Entry"].get()) + 'Forensic Question ' + str(i + 1) + '.txt'), 'w+')
                g.write(qHeader + q.get() + qFooter)
                g.close()
                if len(vulnerability_settings["Forensic"]["Location"]) > i:
                    vulnerability_settings["Forensic"]["Location"][i] = (str(vulnerability_settings["Main Menu"]["Desktop Entry"].get()) + 'Forensic Question ' + str(i + 1) + '.txt')
                else:
                    vulnerability_settings["Forensic"]["Location"].append((str(vulnerability_settings["Main Menu"]["Desktop Entry"].get()) + 'Forensic Question ' + str(i + 1) + '.txt'))


def commit_config():
    save_config()
    if not admin_test.isUserAdmin():
        switch = messagebox.askyesno('Administrative Access Required', 'You need to be Admin to Write to Config. Do you want to relaunch the confiturator as Administrator.')
        if switch:
            sys.exit(admin_test.runAsAdmin())
        return
    output_directory = 'C:/CyberPatriot/'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    shutil.copy('CCC_logo.png', os.path.join(output_directory, 'CCC_logo.png'))
    shutil.copy('SoCalCCCC.png', os.path.join(output_directory, 'SoCalCCCC.png'))
    shutil.copy('scoring_engine_logo_windows_icon_5TN_icon.ico', os.path.join(output_directory, 'scoring_engine_logo_windows_icon_5TN_icon.ico'))
    shutil.copy('save_data.json', os.path.join(output_directory, 'save_data.json'))
    shutil.copy('scoring_engine.exe', os.path.join(output_directory, 'scoring_engine.exe'))

    r = open(r'C:\\CyberPatriot\\RunScoring.bat', 'w+')
    r.write('@echo off\ncd C:\\CyberPatriot\nstart scoring_engine.exe')
    r.close()
    s = open(r'c:\\CyberPatriot\\Repeat.bat', 'w+')
    s.write('@echo off\ntasklist /nh /fi "imagename eq scoring_engine.exe" | find /i "scoring_engine.exe" > nul || (cd C:\\CyberPatriot\nstart RunScoring.bat)')
    s.close()
    os.system('schtasks /create /SC ONSTART /TN ScoringEngine /TR C:\\CyberPatriot\\RunScoring.bat /RL HIGHEST /F')
    os.system('schtasks /create /SC MINUTE /MO 2 /TN RepeatScore /TR C:\\CyberPatriot\\Repeat.bat /RL HIGHEST /F')
    time.sleep(2)
    sys.exit()


def save_config():
    save_dictionary = {}
    # We wanna use those fancy variable lists
    set_desktop()
    if "\\Desktop\\" not in vulnerability_settings["Main Menu"]["Desktop Entry"].get() and vulnerability_settings["Main Menu"]["Desktop Entry"].get() == '':
        cwd = vulnerability_settings["Main Menu"]["Desktop Entry"].get()
        cwd = "C:\\Users\\" + cwd + "\\Desktop\\"
        vulnerability_settings["Main Menu"]["Desktop Entry"].set(cwd)
    create_forensic()
    if vulnerability_settings["Main Menu"]["Server Mode"].get() == 1:
        f = open('FTP.txt', 'w+')
        line1 = "serverName='" + vulnerability_settings["Main Menu"]["Server Name"].get() + "'\n"
        line2 = "userName='" + vulnerability_settings["Main Menu"]["Server User Name"].get() + "'\n"
        line3 = "password='" + vulnerability_settings["Main Menu"]["Server Password"].get() + "'\n"
        for line in (line1, line2, line3):
            f.write(line)
        f.close()
    for s in vulnerability_settings.keys():
        if s == "Main Menu":
            save_dictionary.update({s: {}})
            for m in vulnerability_settings[s]:
                save_dictionary[s].update({m: vulnerability_settings[s][m].get()})
        elif s == "Forensic":
            save_dictionary.update({s: {"Enabled": vulnerability_settings[s]["Enabled"].get(), "Categories": {}, "Location": vulnerability_settings[s]["Location"]}})
            for m in vulnerability_settings[s]["Categories"]:
                save_dictionary[s]["Categories"].update({m: []})
                for settings in vulnerability_settings[s]["Categories"][m]:
                    if settings != 0:
                        save_dictionary[s]["Categories"][m].append(settings.get())
        else:
            save_dictionary.update({s: {}})
            for m in vulnerability_settings[s].keys():
                save_dictionary[s].update({m: {"Enabled": vulnerability_settings[s][m]["Enabled"].get(), "Categories": {}}})
                for c in vulnerability_settings[s][m]["Categories"].keys():
                    save_dictionary[s][m]["Categories"].update({c: []})
                    for settings in vulnerability_settings[s][m]["Categories"][c]:
                        if settings != 0:
                            save_dictionary[s][m]["Categories"][c].append(settings.get())
    filename = 'save_data.json'
    with open(filename, 'w+') as f:
        json.dump(save_dictionary, f)
    tally()


def tally():
    # Set tally scores
    tally_score = 0
    tally_settings = 0
    for s in vulnerability_settings.keys():
        if s == "Forensic":
            for i, p in enumerate(vulnerability_settings[s]["Categories"]["Points"]):
                if vulnerability_settings[s]["Enabled"].get() == 1 and p != 0:
                    tally_settings += 1
                    tally_score += int(p.get())
        elif s != "Main Menu":
            for o in vulnerability_settings[s].keys():
                if vulnerability_settings[s][o]["Enabled"].get() == 1 and o != "Keep User":
                    for settings in vulnerability_settings[s][o]["Categories"]["Points"]:
                        if settings != 0:
                            tally_settings += 1
                            tally_score += int(settings.get())
        vulnerability_settings["Main Menu"]["Tally Points"].set("Vulnerabilities: {0}\nTotal Points: {1}".format(str(tally_settings), str(tally_score)))


def load_config(forensic):
    filename = 'save_data.json'
    if os.path.exists(filename):
        f = open(filename)
        save_dictionary = json.load(f)
        for s in save_dictionary.keys():
            if s == "Main Menu":
                for m in save_dictionary[s]:
                    vulnerability_settings[s][m].set(save_dictionary[s][m])
            elif s == "Forensic":
                for i in range(1, len(save_dictionary[s]["Categories"]["Points"])):
                    add_row(forensic, vulnerability_settings["Forensic"]["Categories"], widgetDict["Forensic"], 2)
                for m in save_dictionary[s]["Categories"]:
                    for i, settings in enumerate(save_dictionary[s]["Categories"][m]):
                        vulnerability_settings[s]["Categories"][m][i].set(settings)
                vulnerability_settings[s]['Location'] = save_dictionary[s]['Location']
                vulnerability_settings[s]["Enabled"].set(save_dictionary[s]["Enabled"])
            else:
                for m in save_dictionary[s].keys():
                    vulnerability_settings[s][m]["Enabled"].set(save_dictionary[s][m]["Enabled"])
                    for c in save_dictionary[s][m]["Categories"].keys():
                        for i, settings in enumerate(save_dictionary[s][m]["Categories"][c]):
                            if i == 0:
                                vulnerability_settings[s][m]["Categories"][c][i].set(settings)
                            else:
                                if c == "Points":
                                    vulnerability_settings[s][m]["Categories"][c].append(IntVar())
                                else:
                                    vulnerability_settings[s][m]["Categories"][c].append(StringVar())
                                vulnerability_settings[s][m]["Categories"][c][i].set(settings)
        f.close()
        tally()


def set_desktop():
    if vulnerability_settings["Main Menu"]["Desktop Checkbox"].get() == 1:
        cwd = os.getcwd()
        s = cwd.rfind('\\')
        a = len(cwd)
        s = a - s - 1
        cwd = cwd[:-s]
        vulnerability_settings["Main Menu"]["Desktop Entry"].set(cwd)


def show_error(self, *args):
    err = traceback.format_exception(*args)
    for i in err:
        if 'expected integer but got' in i:
            err = 'There is an integer error with one of the points'
    messagebox.showerror('Exception', err)


Tk.report_callback_exception = show_error

vulnerability_settings = {}
widgetDict = {"Forensic": {}, "Modify": {}, "Report": []}
themeList = ["aquativo", "aquativo", "black", "clearlooks", "elegance", "equilux", "keramik", "plastik", "ubuntu"]

root = Config()
root.title('Configurator')
root.geometry("{0}x{1}+{2}+{3}".format(int(root.winfo_screenwidth() * 3 / 4), int(root.winfo_screenheight() * 2 / 3), int(root.winfo_screenwidth() / 9), int(root.winfo_screenheight() / 6)))

root.ttkStyle = ThemedStyle(root.winfo_toplevel())
for theme in themeList:
    root.ttkStyle.set_theme(theme)
root.ttkStyle.set_theme(vulnerability_settings["Main Menu"]["Style"].get())
root.ttkStyle.theme_settings(themename="aquativo", settings={".": {"configure": {"background": '#eff0f1'}}, "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}}, "TNotebook.Tab": {"configure": {"width": int(root.winfo_screenwidth() * 3 / 4 / 7), "anchor": 'center'}}, "TLabel": {"configure": {"padding": '5 0', "justify": 'center', "wraplength": int(root.winfo_screenwidth() * 3 / 4 - 140)}}, "TEntry": {"map": {"fieldbackground": [('disabled', '#a9acb2')]}}, "TButton": {"configure": {"anchor": 'center', "width": '13'}}})
root.ttkStyle.theme_settings(themename="black", settings={"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}}, "TNotebook.Tab": {"configure": {"width": int(root.winfo_screenwidth() * 3 / 4 / 7), "anchor": 'center'}}, "TLabel": {"configure": {"padding": '5 0', "justify": 'center', "wraplength": int(root.winfo_screenwidth() * 3 / 4 - 145)}}, "TEntry": {"map": {"fieldbackground": [('disabled', '#868583')]}}, "TButton": {"configure": {"anchor": 'center', "width": '13'}}})
root.ttkStyle.theme_settings(themename="clearlooks", settings={"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}}, "TNotebook.Tab": {"configure": {"width": int(root.winfo_screenwidth() * 3 / 4 / 7), "anchor": 'center'}}, "TLabel": {"configure": {"padding": '5 0', "justify": 'center', "wraplength": int(root.winfo_screenwidth() * 3 / 4 - 145)}}, "TEntry": {"map": {"fieldbackground": [('disabled', '#b0aaa4')]}}, "TButton": {"configure": {"anchor": 'center', "width": '13'}}})
root.ttkStyle.theme_settings(themename="elegance", settings={"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}}, "TNotebook.Tab": {"configure": {"width": int(root.winfo_screenwidth() * 3 / 4 / 7), "anchor": 'center'}}, "TLabel": {"configure": {"font": '8', "padding": '5 0', "justify": 'center', "wraplength": int(root.winfo_screenwidth() * 3 / 4 - 145)}}, "TButton": {"configure": {"anchor": 'center', "width": '13'}}})
root.ttkStyle.theme_settings(themename="equilux", settings={"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}}, "TNotebook.Tab": {"configure": {"width": int(root.winfo_screenwidth() * 3 / 4 / 7), "anchor": 'center'}}, "TLabel": {"configure": {"padding": '5 0', "justify": 'center', "wraplength": int(root.winfo_screenwidth() * 3 / 4 - 145)}, "map": {"foreground": [('disabled', '#5b5b5b')]}}, "TButton": {"configure": {"anchor": 'center', "width": '13'}}})
root.ttkStyle.theme_settings(themename="keramik", settings={"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}}, "TNotebook.Tab": {"configure": {"width": int(root.winfo_screenwidth() * 3 / 4 / 7), "anchor": 'center'}}, "TLabel": {"configure": {"padding": '5 0', "justify": 'center', "wraplength": int(root.winfo_screenwidth() * 3 / 4 - 145)}}, "TButton": {"configure": {"anchor": 'center', "width": '13'}}})
root.ttkStyle.theme_settings(themename="plastik", settings={"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}}, "TNotebook.Tab": {"configure": {"width": int(root.winfo_screenwidth() * 3 / 4 / 7), "anchor": 'center'}}, "TLabel": {"configure": {"padding": '5 0', "justify": 'center', "wraplength": int(root.winfo_screenwidth() * 3 / 4 - 145)}}, "TButton": {"configure": {"anchor": 'center', "width": '13'}}})
root.ttkStyle.theme_settings(themename="ubuntu", settings={"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}}, "TNotebook.Tab": {"configure": {"width": int(root.winfo_screenwidth() * 3 / 4 / 7), "anchor": 'center'}}, "TLabel": {"configure": {"padding": '5 0', "justify": 'center', "wraplength": int(root.winfo_screenwidth() * 3 / 4 - 170)}, "map": {"foreground": [('disabled', '#c2c2c2')]}}, "TButton": {"configure": {"anchor": 'center', "width": '13'}}})

root.mainloop()
