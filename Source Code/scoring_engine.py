import json
import win32com.client
import os
import time
import datetime
import balloontip
import admin_test
import tkinter
from tkinter import messagebox


# Scoring Report creation
def draw_head():
    f = open(scoreIndex, 'w+')
    f.write('<!doctype html><html><head><title>CSEW Score Report</title><meta http-equiv="refresh" content="60"></head><body style="background-color:powderblue;">''\n')
    f.write('<table align="center" cellpadding="10"><tr><td><img src="C:/CyberPatriot/CCC_logo.png"></td><td><div align="center"><H2>Cyberpatriot Scoring Engine:Windows v1.0</H2></div></td><td><img src="C:/CyberPatriot/SoCalCCCC.png"></td></tr></table><br><H2>Your Score: #TotalScore#/#PossiblePoints#</H2><H2>Vulnerabilities: #TotalVuln#/#PossibleVuln#</H2><hr>')
    f.close()


def record_hit(name, points, message):
    global total_points, possible_points
    global total_vulnerabilities, possible_vulnerabilities
    write_to_html(('<p style="color:green">' + name + ' (' + str(points) + ' points)</p>'))
    total_points += int(points)
    possible_points += int(points)
    total_vulnerabilities += 1
    possible_vulnerabilities += 1


def record_miss(name, points):
    global possible_points, possible_vulnerabilities
    possible_points += int(points)
    possible_vulnerabilities += 1
    if not save_dictionary["Main Menu"]['Silent Mode'] == 1:
        write_to_html(('<p style="color:red">MISS ' + name + ' Issue</p>'))


def record_penalty(name, points, message):
    global total_points
    write_to_html(('<p style="color:red">' + name + ' (' + str(points) + ' points)</p>'))
    total_points -= int(points)


def draw_tail():
    write_to_html('<hr><div align="center"><b>Coastline Collage</b><br>Created by Shaun Martin, Anthony Nguyen, and Minh-Khoi Do</br><br>Feedback welcome: <a href="mailto:smartin94@student.cccd.edu?Subject=CSEW Scoring Engine" target="_top">smartin94@student.cccd.edu</a></div>')
    print(str(total_points) + ' / ' + str(possible_points) + '\n' + str(total_vulnerabilities) + ' / ' + str(possible_vulnerabilities))
    replace_section(scoreIndex, '#TotalScore#', str(total_points))
    replace_section(scoreIndex, '#PossiblePoints#', str(possible_points))
    replace_section(scoreIndex, '#TotalVuln#', str(total_vulnerabilities))
    replace_section(scoreIndex, '#PossibleVuln#', str(possible_vulnerabilities))

    path = os.path.join(Desktop, 'ScoreReport.lnk')
    target = scoreIndex
    icon = os.path.join(index, 'scoring_engine_logo_windows_icon_5TN_icon.ico')
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
    shortcut.save()


# Extra Functions
def check_runas():
    if not admin_test.isUserAdmin():
        messagebox.showerror('Administrator Access Needed', 'Please make sure the scoring engine is running as admin.')
        exit(admin_test.runAsAdmin())


def check_score():
    global total_points
    global prePoints
    if total_points > prePoints:
        prePoints = total_points
        w.ShowWindow('Score Update', 'You gained points!!')
    elif total_points < prePoints:
        prePoints = total_points
        w.ShowWindow('Score Update', 'You lost points!!')
    if total_points == possible_points:
        time.sleep(5)
        w.ShowWindow('Image Completed', 'Congratulations you finished the image.')


def write_to_html(message):
    f = open(scoreIndex, 'a')
    f.write(message)
    f.close()


def replace_section(loc, search, replace):
    lines = []
    with open(loc) as file:
        for line in file:
            line = line.replace(search, replace)
            lines.append(line)
    with open(loc, 'w') as file:
        for line in lines:
            file.write(line)


# Option Check
def forensic_question():
    for idx, path in enumerate(save_dictionary["Forensic"]["Location"]):
        f = open(path, 'r')
        content = f.read().splitlines()
        for c in content:
            if 'ANSWER:' in c:
                if save_dictionary["Forensic"]["Categories"]["Answer"][idx] in c:
                    record_hit('Forensic question number ' + str(idx + 1) + ' has been answered.', save_dictionary["Forensic"]["Categories"]['Points'][idx], '')
                else:
                    record_miss('Forensic Question', save_dictionary["Forensic"]["Categories"]['Points'][idx])


def disable_guest():
    f = open('user.txt', 'r', encoding='utf-16-le')
    content = f.read().splitlines()
    f.close()
    for c in content:
        if 'Guest' in c:
            if ' True' in c:
                record_hit('The guest account haas been disabled.', save_dictionary["Account Management"]["Disable Guest"]["Categories"]['Points'][0], '')
            else:
                record_miss('User Management', save_dictionary["Account Management"]["Disable Guest"]["Categories"]['Points'][0])


def disable_admin():
    f = open('user.txt', 'r', encoding='utf-16-le')
    content = f.read().splitlines()
    f.close()
    for c in content:
        if 'Administrator' in c:
            if ' True' in c:
                record_hit('The default administrator account has been disabled.', save_dictionary["Account Management"]["Disable Admin"]["Categories"]['Points'][0], '')
            else:
                record_miss('User Management', save_dictionary["Account Management"]["Disable Admin"]["Categories"]['Points'][0])


def turn_on_firewall():
    with open('status.txt') as t:
        content = t.read().splitlines()
    t.close()
    for cont in content:
        if 'State' in cont:
            if 'ON' in cont:
                record_hit('Firewall has been turned on.', save_dictionary["Local Policy Options"]["Turn On Firewall"]["Categories"]['Points'][0], '')
            else:
                record_miss('Policy Management', save_dictionary["Local Policy Options"]["Turn On Firewall"]["Categories"]['Points'][0])
            return


def local_group_policy():
    p = open('group-policy.txt', 'r', encoding='utf-16-le')
    content = p.read().splitlines()
    p.close()
    for i in content:
        if 'MinimumPasswordAge' in i:
            if save_dictionary["Local Policy Password"]["Minimum Password Age"]["Enabled"] == 1:
                if i.endswith(('30', '45', '60')):
                    record_hit('Minimum password age is set to 30-60.', save_dictionary["Local Policy Password"]["Minimum Password Age"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Minimum Password Age"]["Categories"]['Points'][0])
        elif 'MaximumPasswordAge ' in i:
            if save_dictionary["Local Policy Password"]["Maximum Password Age"]["Enabled"] == 1:
                if i.endswith(('60', '75', '90')):
                    record_hit('Maximum password age is set to 60-90.', save_dictionary["Local Policy Password"]["Maximum Password Age"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Maximum Password Age"]["Categories"]['Points'][0])
        elif 'LockoutBadCount' in i:
            if save_dictionary["Local Policy Password"]["Maximum Login Tries"]["Enabled"] == 1:
                if i.endswith(('5', '6', '7', '8', '9', '10')):
                    record_hit('Maximum login tries is set to 5-10.', save_dictionary["Local Policy Password"]["Maximum Login Tries"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Maximum Login Tries"]["Categories"]['Points'][0])
        elif 'LockoutDuration' in i:
            if save_dictionary["Local Policy Password"]["Lockout Duration"]["Enabled"] == 1:
                if i.endswith('30'):
                    record_hit('Lockout duration set is set to 30.', save_dictionary["Local Policy Password"]["Lockout Duration"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Lockout Duration"]["Categories"]['Points'][0])
        elif 'ResetLockoutCount' in i:
            if save_dictionary["Local Policy Password"]["Lockout Reset Duration"]["Enabled"] == 1:
                if i.endswith('30'):
                    record_hit('Lockout counter reset is set to 30.', save_dictionary["Local Policy Password"]["Lockout Reset Duration"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Lockout Reset Duration"]["Categories"]['Points'][0])
        elif 'MinimumPasswordLength' in i:
            if save_dictionary["Local Policy Password"]["Minimum Password Length"]["Enabled"] == 1:
                if i.endswith(('10', '11', '12', '13', '14', '15', '16' '17', '18', '19', '20')):
                    record_hit('Minimum password length is set to 10-29.', save_dictionary["Local Policy Password"]["Minimum Password Length"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Minimum Password Length"]["Categories"]['Points'][0])
        elif 'PasswordHistorySize' in i:
            if save_dictionary["Local Policy Password"]["Password History"]["Enabled"] == 1:
                if i.endswith(('5', '6', '7', '8', '9', '10')):
                    record_hit('Password history size is set to 5-10.', save_dictionary["Local Policy Password"]["Password History"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Password History"]["Categories"]['Points'][0])
        elif 'PasswordComplexity' in i:
            if save_dictionary["Local Policy Password"]["Password Complexity"]["Enabled"] == 1:
                if i.endswith('1'):
                    record_hit('Password complexity has been enabled.', save_dictionary["Local Policy Password"]["Password Complexity"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Password Complexity"]["Categories"]['Points'][0])
        elif 'ClearTextPassword' in i:
            if save_dictionary["Local Policy Password"]["Reversible Password Encryption"]["Enabled"] == 1:
                if i.endswith('0'):
                    record_hit('Reversible password encryption has been Disabled.', save_dictionary["Local Policy Password"]["Reversible Password Encryption"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Password"]["Reversible Password Encryption"]["Categories"]['Points'][0])
        elif 'AuditAccountLogon' in i:
            if save_dictionary["Local Policy Audit"]["Audit Account Login"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit Account Login set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit Account Login"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit Account Login"]["Categories"]['Points'][0])
        elif 'AuditAccountManage' in i:
            if save_dictionary["Local Policy Audit"]["Audit Account Management"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit Account Manage set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit Account Management"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit Account Management"]["Categories"]['Points'][0])
        elif 'AuditDSAccess' in i:
            if save_dictionary["Local Policy Audit"]["Audit Directory Settings Access"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit Directory Service Access set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit Directory Settings Access"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit Directory Settings Access"]["Categories"]['Points'][0])
        elif 'AuditLogonEvents' in i:
            if save_dictionary["Local Policy Audit"]["Audit Logon Events"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit Logon Events set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit Logon Events"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit Logon Events"]["Categories"]['Points'][0])
        elif 'AuditObjectAccess' in i:
            if save_dictionary["Local Policy Audit"]["Audit Object Access"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit Object Access set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit Object Access"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit Object Access"]["Categories"]['Points'][0])
        elif 'AuditPolicyChange' in i:
            if save_dictionary["Local Policy Audit"]["Audit Policy Change"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit Policy Change set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit Policy Change"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit Policy Change"]["Categories"]['Points'][0])
        elif 'AuditPrivilegeUse' in i:
            if save_dictionary["Local Policy Audit"]["Audit Privilege Use"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit Privilege Use set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit Privilege Use"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit Privilege Use"]["Categories"]['Points'][0])
        elif 'AuditProcessTracking' in i:
            if save_dictionary["Local Policy Audit"]["Audit Process Tracking"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit Process Tracking set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit Process Tracking"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit Process Tracking"]["Categories"]['Points'][0])
        elif 'AuditSystemEvents' in i:
            if save_dictionary["Local Policy Audit"]["Audit System Events"]["Enabled"] == 1:
                if i.endswith('3'):
                    record_hit('Audit System Events set to Success and Failure.', save_dictionary["Local Policy Audit"]["Audit System Events"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Audit"]["Audit System Events"]["Categories"]['Points'][0])
        elif 'DisableCAD' in i:
            if save_dictionary["Local Policy Options"]["Do Not Require CTRL_ALT_DEL"]["Enabled"] == 1:
                if i.endswith('0'):
                    record_hit('Do not require CTRL + ALT + DEL has been disabled.', save_dictionary["Local Policy Options"]["Do Not Require CTRL_ALT_DEL"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Options"]["Do Not Require CTRL_ALT_DEL"]["Categories"]['Points'][0])
        elif 'DontDisplayLastUserName' in i:
            if save_dictionary["Local Policy Options"]["Don't Display Last User"]["Enabled"] == 1:
                if i.endswith('1'):
                    record_hit('Don\'t Display Last User Name has been enabled.', save_dictionary["Local Policy Options"]["Don't Display Last User"]["Categories"]['Points'][0], '')
                else:
                    record_miss('Policy Management', save_dictionary["Local Policy Options"]["Don't Display Last User"]["Categories"]['Points'][0])


def keep_user():
    with open('users.txt') as t:
        content = t.read()
    t.close()
    for idx, name in enumerate(save_dictionary["Account Management"]["Keep User"]["Categories"]['User Name']):
        if name.lower() not in content.lower():
            record_penalty(name + ' was removed.', save_dictionary["Account Management"]["Keep User"]["Categories"]['Points'][idx], '')


def add_user():
    with open('users.txt') as t:
        content = t.read()
    t.close()
    for idx, name in enumerate(save_dictionary["Account Management"]["Add User"]["Categories"]['User Name']):
        if name.lower() in content.lower():
            record_hit(name + ' has been added', save_dictionary["Account Management"]["Add User"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["Add User"]["Categories"]['Points'][idx])


def remove_user():
    with open('users.txt') as t:
        content = t.read()
    t.close()
    for idx, name in enumerate(save_dictionary["Account Management"]["Remove User"]["Categories"]['User Name']):
        if name.lower() not in content.lower():
            record_hit(name + ' has been removed.', save_dictionary["Account Management"]["Remove User"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["Remove User"]["Categories"]['Points'][idx])


def add_admin():
    with open('admins.txt') as t:
        content = t.read()
    t.close()
    for idx, name in enumerate(save_dictionary["Account Management"]["Add Admin"]["Categories"]['User Name']):
        if name.lower() in content.lower():
            record_hit(name + ' has been promoted to administrator.', save_dictionary["Account Management"]["Add Admin"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["Add Admin"]["Categories"]['Points'][idx])


def remove_admin():
    with open('admins.txt') as t:
        content = t.read()
    t.close()
    for idx, name in enumerate(save_dictionary["Account Management"]["Remove Admin"]["Categories"]['User Name']):
        if name.lower() not in content.lower():
            record_hit(name + ' has been demoted to standard user.', save_dictionary["Account Management"]["Remove Admin"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["Remove Admin"]["Categories"]['Points'][idx])


def add_user_to_group():
    for idx, name in enumerate(save_dictionary["Account Management"]['Add User to Group']["Categories"]['Group Name']):
        with open(name.lower() + '_add_groups.txt') as t:
            content = t.read()
        t.close()
        if save_dictionary["Account Management"]['Add User to Group']["Categories"]['User Name'][idx].lower() in content.lower():
            record_hit(save_dictionary["Account Management"]['Add User to Group']["Categories"]['User Name'][idx] + ' is in the ' + name + ' group.', save_dictionary["Account Management"]['Add User to Group']["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]['Add User to Group']["Categories"]['Points'][idx])


def remove_user_from_group():
    for idx, name in enumerate(save_dictionary["Account Management"]['Remove User from Group']["Categories"]['Group Name']):
        with open(name.lower() + '_rem_groups.txt') as t:
            content = t.read()
        t.close()
        if save_dictionary["Account Management"]['Remove User from Group']["Categories"]['User Name'][idx].lower() not in content.lower():
            record_hit(save_dictionary["Account Management"]['Remove User from Group']["Categories"]['User Name'][idx] + ' is no longer in the ' + name + ' group.', save_dictionary["Account Management"]['Remove User from Group']["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]['Remove User from Group']["Categories"]['Points'][idx])


def user_change_password():
    for idx, name in enumerate(save_dictionary["Account Management"]["User Change Password"]["Categories"]['User Name']):
        f = open('user_' + name.lower() + '.txt')
        content = f.read().splitlines()
        f.close()
        for c in content:
            if 'Password last set' in c:
                s = c.split(' ')
                for t in s:
                    if '/' in t:
                        c = ''
                        t = t.split('/')
                        for p, d in enumerate(t):
                            if int(d) < 10:
                                temp = '0' + d
                            else:
                                temp = d
                            if p < 2:
                                c = c + temp + '/'
                            else:
                                c = c + d
                if datetime.datetime.now().strftime('%m/%d/%Y') == c:
                    record_hit(name + '\'s password was changed.', save_dictionary["Account Management"]["User Change Password"]["Categories"]['Points'][idx], '')
                else:
                    record_miss('Policy Management', save_dictionary["Account Management"]["User Change Password"]["Categories"]['Points'][idx])


def check_startup():
    f = open('startup.txt', 'r', encoding='utf-16-le')
    content = f.read().splitlines()
    f.close()
    for k in save_dictionary["Miscellaneous"]["Check Startup"]["Categories"]['Program Name']:
        if k in content:
            record_hit('Program Removed from Startup', save_dictionary["Miscellaneous"]["Check Startup"]["Categories"]['Points'][0], '')
        else:
            record_miss('Program Management', save_dictionary["Miscellaneous"]["Check Startup"]["Categories"]['Points'][0])


def add_text_to_file():
    for idx, item in enumerate(save_dictionary["File Management"]["Add Text to File"]["Categories"]['File Path']):
        f = open(item, 'r')
        content = f.read().splitlines()
        for c in content:
            if save_dictionary["File Management"]["Add Text to File"]["Categories"]['Text to Add'][idx] in c:
                record_hit(save_dictionary["File Management"]["Add Text to File"]["Categories"]['Text to Add'][idx] + ' has been added to ' + item, save_dictionary["File Management"]["Add Text to File"]["Categories"]['Points'][idx], '')
            else:
                record_miss('File Management', save_dictionary["File Management"]["Add Text to File"]["Categories"]['Points'][idx])


def remove_text_from_file():
    for idx, item in enumerate(save_dictionary["File Management"]["Remove Text From File"]["Categories"]['File Path']):
        f = open(item, 'r')
        content = f.read().splitlines()
        for c in content:
            if save_dictionary["File Management"]["Remove Text From File"]["Categories"]['Text to Remove'][idx] not in c:
                record_hit(save_dictionary["File Management"]["Remove Text From File"]["Categories"]['Text to Remove'][idx] + ' has been removed from ' + item, save_dictionary["File Management"]["Remove Text From File"]["Categories"]['Points'][idx], '')
            else:
                record_miss('File Management', save_dictionary["File Management"]["Remove Text From File"]["Categories"]['Points'][idx])


def services():
    p = open('services.txt', 'r', encoding='utf-16-le')
    content = p.read().splitlines()
    p.close()
    for c in content:
        for idx, bs in save_dictionary["Program Management"]["Service"]["Categories"]['Service Name']:
            if bs in c:
                if save_dictionary["Program Management"]["Service"]["Categories"]['Service Status'][idx] in c and save_dictionary["Program Management"]["Service"]["Categories"]['Service Start Type'][idx] in c:
                    record_hit(bs + ' has been ' + save_dictionary["Program Management"]["Service"]["Categories"]['Service Status'][idx] + ' and set to ' + save_dictionary["Program Management"]["Service"]["Categories"]['Service Start Type'][idx], save_dictionary["Program Management"]["Service"]["Categories"]['Points'][idx], '')
                else:
                    record_miss('Program Management', save_dictionary["Program Management"]["Service"]["Categories"]['Points'][idx])


def programs(option):
    k = open('programs.txt', 'r', encoding='utf-16-le')
    content = k.read().splitlines()
    k.close()
    if option == 'good_program':
        for idx, gp in save_dictionary["Program Management"]["Good Program"]["Categories"]['Program Name']:
            installed = False
            for c in content:
                if gp in c:
                    installed = True
            if installed:
                record_hit(gp + ' is installed', save_dictionary["Program Management"]["Good Program"]["Categories"]['Points'][idx], '')
            else:
                record_miss('Program Management', save_dictionary["Program Management"]["Good Program"]["Categories"]['Points'][idx])
    if option == 'bad_program':
        for idx, bp in save_dictionary["Program Management"]["Bad Program"]["Categories"]['Program Name']:
            installed = False
            for c in content:
                if bp in c:
                    installed = True
            if not installed:
                record_hit(bp + ' is uninstalled', save_dictionary["Program Management"]["Bad Program"]["Categories"]['Points'][idx], '')
            else:
                record_miss('Program Management', save_dictionary["Program Management"]["Bad Program"]["Categories"]['Points'][idx])


def anti_virus():
    z = open('security.txt', 'r', encoding='utf-16-le')
    content = z.read()
    z.close()
    if 'Real-time Protection Status : Enabled' in content:
        record_hit('Virus & threat protection enabled.', save_dictionary["Miscellaneous"]["Anti-Virus"]["Categories"]['Points'][0], '')
    else:
        record_miss('Security', save_dictionary["Miscellaneous"]["Anti-Virus"]["Categories"]['Points'][0])


def bad_file():
    for idx, item in enumerate(save_dictionary["File Management"]["Bad File"]["Categories"]['File Path']):
        if not os.path.exists(item):
            record_hit('The item ' + item + ' has been removed.', save_dictionary["File Management"]["Bad File"]["Categories"]['Points'][idx], '')
        else:
            record_miss('File Management', save_dictionary["File Management"]["Bad File"]["Categories"]['Points'][idx])


def load_config():
    global save_dictionary
    filename = 'save_data.json'
    if os.path.exists(filename):
        f = open(filename)
        save_dictionary = json.load(f)
        f.close()
    else:
        messagebox.showerror('Save Error', 'You are missing the configuration file. Please notify a mentor or re-extract the VM.')


def ps_create():
    m = open('check.ps1', 'w+')
    if save_dictionary["Account Management"]["Disable Guest"]["Enabled"] == 1 or save_dictionary["Account Management"]["Disable Admin"]["Enabled"] == 1:
        m.write('Get-WmiObject -Class Win32_UserAccount -Filter "LocalAccount=\'$true\'"|Select-Object Name,Disabled|Format-Table -AutoSize > user.txt\n')
    if save_dictionary["Program Management"]["Services"]["Enabled"] == 1:
        m.write('Get-Service | Select-Object Name,status,startType | Format-Table -AutoSize > services.txt\n')
    if save_dictionary["Program Management"]["Bad Program"]["Enabled"] == 1 or save_dictionary["Program Management"]["Good Program"]["Enabled"] == 1:
        m.write('Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize > programs.txt\n')
    if save_dictionary["Miscellaneous"]["Check Startup"]["Enabled"] == 1:
        m.write('Get-CimInstance -ClassName Win32_StartupCommand | Select-Object -Property Command, Description, User, Location | Format-Table -AutoSize > startup.txt\n')
    if save_dictionary["Miscellaneous"]["Anti-Virus"]["Enabled"] == 1:
        m.write('function Get-AntiVirusProduct {\n[CmdletBinding()]\nparam (\n[parameter(ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$true)]\n[Alias(\'name\')]\n$computername=$env:computername\n\n)\n\n#$AntivirusProducts = Get-WmiObject -Namespace "root\\SecurityCenter2" -Query $wmiQuery  @psboundparameters # -ErrorVariable myError -ErrorAction \'SilentlyContinue\' # did not work\n$AntiVirusProducts = Get-WmiObject -Namespace "root\\SecurityCenter2" -Class AntiVirusProduct  -ComputerName $computername\n\n$ret = @()\nforeach($AntiVirusProduct in $AntiVirusProducts){\n#Switch to determine the status of antivirus definitions and real-time protection.\n#The values in this switch-statement are retrieved from the following website: http://community.kaseya.com/resources/m/knowexch/1020.aspx\nswitch ($AntiVirusProduct.productState) {\n"262144" {$defstatus = "Up to date" ;$rtstatus = "Disabled"}\n"262160" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}\n"266240" {$defstatus = "Up to date" ;$rtstatus = "Enabled"}\n"266256" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}\n"393216" {$defstatus = "Up to date" ;$rtstatus = "Disabled"}\n"393232" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}\n"393488" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}\n"397312" {$defstatus = "Up to date" ;$rtstatus = "Enabled"}\n"397328" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}\n"397584" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}\ndefault {$defstatus = "Unknown" ;$rtstatus = "Unknown"}\n}\n\n#Create hash-table for each computer\n$ht = @{}\n$ht.Computername = $computername\n$ht.Name = $AntiVirusProduct.displayName\n$ht.\'Product GUID\' = $AntiVirusProduct.instanceGuid\n$ht.\'Product Executable\' = $AntiVirusProduct.pathToSignedProductExe\n$ht.\'Reporting Exe\' = $AntiVirusProduct.pathToSignedReportingExe\n$ht.\'Definition Status\' = $defstatus\n$ht.\'Real-time Protection Status\' = $rtstatus\n\n#Create a new object for each computer\n$ret += New-Object -TypeName PSObject -Property $ht \n}\nReturn $ret\n} \nGet-AntiVirusProduct > security.txt\n')
    m.close()
    m = open('check.bat', 'w+')
    m.write('echo > trigger.cfg\n')
    if save_dictionary["Account Management"]["Keep User"]["Enabled"] == 1 or save_dictionary["Account Management"]["Remove User"]["Enabled"] == 1 or save_dictionary["Account Management"]["Add User"]["Enabled"] == 1:
        m.write('net users > users.txt\n')
    if save_dictionary["Account Management"]["User Change Password"]["Enabled"] == 1:
        for name in save_dictionary["Account Management"]["User Change Password"]["Categories"]['User Name']:
            m.write('net user ' + name.lower() + ' > user_' + name.lower() + '.txt\n')
    if save_dictionary["Account Management"]["Add Admin"]["Enabled"] == 1 or save_dictionary["Account Management"]["Remove Admin"]["Enabled"] == 1:
        m.write('net localgroup Administrators > admins.txt\n')
    if save_dictionary["Account Management"]["Add User to Group"]["Enabled"] == 1:
        for item in save_dictionary["Account Management"]['Add User to Group']["Categories"]['Group Name']:
            m.write('net localgroup ' + item.lower() + ' > ' + item.lower() + '_add_groups.txt\n')
    if save_dictionary["Account Management"]["Remove User from Group"]["Enabled"] == 1:
        for item in save_dictionary["Account Management"]['Remove User from Group']["Categories"]['Group Name']:
            m.write('net localgroup ' + item.lower() + ' > ' + item.lower() + '_rem_groups.txt\n')
    if save_dictionary["Local Policy Options"]["Turn On Firewall"]["Enabled"] == 1:
        m.write('netsh advfirewall show private > status.txt\nnetsh advfirewall show public >> status.txt\n')
    if save_dictionary["Local Policy Password"]["Minimum Password Age"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Maximum Password Age"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Maximum Login Tries"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Lockout Duration"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Lockout Reset Duration"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Minimum Password Length"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Password History"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Password Complexity"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Reversible Password Encryption"]["Enabled"] == 1 or save_dictionary["Local Policy Options"]["Do Not Require CTRL_ALT_DEL"]["Enabled"] == 1 or save_dictionary["Local Policy Options"]["Don't Display Last User"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Account Login"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Account Management"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Directory Settings Access"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Logon Events"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Object Access"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Policy Change"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Privilege Use"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Process Tracking"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit System Events"]["Enabled"] == 1:
        m.write('secedit /export /cfg group-policy.txt\n')
    if save_dictionary["File Management"]["Bad File"]["Enabled"] == 1 or save_dictionary["Account Management"]["Disable Guest"]["Enabled"] == 1 or save_dictionary["Account Management"]["Disable Admin"]["Enabled"] == 1 or save_dictionary["Program Management"]["Services"]["Enabled"] == 1 or save_dictionary["Program Management"]["Good Program"]["Enabled"] == 1 or save_dictionary["Miscellaneous"]["Check Startup"]["Enabled"] == 1 or save_dictionary["Miscellaneous"]["Anti-Virus"]["Enabled"] == 1:
        m.write('Powershell.exe -Command "& {Start-Process Powershell.exe -ArgumentList \'-ExecutionPolicy Bypass -File "check.ps1"\' -Verb RunAs -Wait -WindowStyle Hidden}"\n')
    m.write('timeout 60')
    m.close()
    f = open('invisible.vbs', 'w+')
    f.write('CreateObject("Wscript.Shell").Run """" & WScript.Arguments(0) & """", 0, False')
    f.close()
    os.system('wscript.exe "invisible.vbs" "check.bat"')
    '''
    if save_dictionary["Miscellaneous"]["Task Scheduler"]["Enabled"] == 1:
        ''taskscheduler()''
    if save_dictionary['checkHosts']["Enabled"] == 1:
        ''checkhosts()''
    if save_dictionary["Miscellaneous"]["Update Auto Install"]["Enabled"] == 1:
        ''updateautoinstall()''
    '''


def user_management():
    write_to_html('<H3>USER MANAGEMENT</H3>')
    if save_dictionary["Account Management"]["Keep User"]["Enabled"] == 1:
        keep_user()
    if save_dictionary["Account Management"]["Remove User"]["Enabled"] == 1:
        remove_user()
    if save_dictionary["Account Management"]["Add User"]["Enabled"] == 1:
        add_user()
    if save_dictionary["Account Management"]["User Change Password"]["Enabled"] == 1:
        user_change_password()
    if save_dictionary["Account Management"]["Add Admin"]["Enabled"] == 1:
        add_admin()
    if save_dictionary["Account Management"]["Remove Admin"]["Enabled"] == 1:
        remove_admin()
    if save_dictionary["Account Management"]["Add User to Group"]["Enabled"] == 1:
        add_user_to_group()
    if save_dictionary["Account Management"]["Remove User from Group"]["Enabled"] == 1:
        remove_user_from_group()


def security_policies():
    write_to_html('<H3>SECURITY POLICIES</H3>')
    if save_dictionary["Account Management"]["Disable Guest"]["Enabled"] == 1:
        disable_guest()
    if save_dictionary["Account Management"]["Disable Admin"]["Enabled"] == 1:
        disable_admin()
    if save_dictionary["Local Policy Options"]["Turn On Firewall"]["Enabled"] == 1:
        turn_on_firewall()
    if save_dictionary["Local Policy Password"]["Minimum Password Age"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Maximum Password Age"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Maximum Login Tries"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Lockout Duration"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Lockout Reset Duration"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Minimum Password Length"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Password History"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Password Complexity"]["Enabled"] == 1 or save_dictionary["Local Policy Password"]["Reversible Password Encryption"]["Enabled"] == 1 or save_dictionary["Local Policy Options"]["Do Not Require CTRL_ALT_DEL"]["Enabled"] == 1 or save_dictionary["Local Policy Options"]["Don't Display Last User"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Account Login"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Account Management"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Directory Settings Access"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Logon Events"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Object Access"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Policy Change"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Privilege Use"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit Process Tracking"]["Enabled"] == 1 or save_dictionary["Local Policy Audit"]["Audit System Events"]["Enabled"] == 1:
        local_group_policy()


def program_management():
    write_to_html('<H3>PROGRAMS</H3>')
    if save_dictionary["Program Management"]["Good Program"]["Enabled"] == 1:
        programs('good_Program')
    if save_dictionary["Program Management"]["Bad Program"]["Enabled"] == 1:
        programs('bad_Program')
    if save_dictionary["Program Management"]["Services"]["Enabled"] == 1:
        services()


def file_management():
    write_to_html('<H3>FILE MANAGEMENT</H3>')
    if save_dictionary["Forensic"]["Enabled"] == 1:
        forensic_question()
    if save_dictionary["File Management"]["Bad File"]["Enabled"] == 1:
        bad_file()
    if save_dictionary["File Management"]['Check Hosts']["Enabled"] == 1:
        '''checkhosts()'''
    if save_dictionary["File Management"]["Add Text to File"]["Enabled"] == 1:
        add_text_to_file()
    if save_dictionary["File Management"]["Remove Text From File"]["Enabled"] == 1:
        remove_text_from_file()


def miscellaneous():
    write_to_html('<H3>MISCELLANEOUS</H3>')
    if save_dictionary["Miscellaneous"]["Check Startup"]["Enabled"] == 1:
        check_startup()
    if save_dictionary["Miscellaneous"]["Task Scheduler"]["Enabled"] == 1:
        '''taskscheduler()'''
    if save_dictionary["Miscellaneous"]["Anti-Virus"]["Enabled"] == 1:
        anti_virus()
    if save_dictionary["Miscellaneous"]["Update Auto Install"]["Enabled"] == 1:
        '''updateautoinstall()'''


def show_error(self, *args):
    err = tkinter.traceback.format_exception(*args)
    messagebox.showerror('Exception', err)


load_config()
possible_points = 0
possible_vulnerabilities = 0
total_points = 0
total_vulnerabilities = 0
prePoints = 0
Desktop = save_dictionary["Main Menu"]["Desktop Entry"]
index = 'C:/CyberPatriot/'
scoreIndex = index + 'ScoreReport.html'

tkinter.Tk.report_callback_exception = show_error
# --------- Main Loop ---------#
w = balloontip.WindowsBalloonTip()
check_runas()
ps_create()
while True:
    if not os.path.exists('trigger.cfg'):
        ps_create()
    else:
        os.remove('trigger.cfg')
    time.sleep(60)
    possible_points = 0
    possible_vulnerabilities = 0
    total_points = 0
    total_vulnerabilities = 0
    draw_head()
    user_management()
    security_policies()
    file_management()
    miscellaneous()
    check_score()
    draw_tail()
    time.sleep(30)

# TODO add Functions:
#  updatecheckperiod    ["Miscellaneous"]["Update Check Period"]
#  updateautoinstall    ["Miscellaneous"]["Update Auto Install"]
#  checkhosts           ["File Management"]["Check Hosts"]
#  taskscheduler        ["Miscellaneous"]["Task Scheduler"]
#  checkstartup         ["Miscellaneous"]["Check Startup"]
