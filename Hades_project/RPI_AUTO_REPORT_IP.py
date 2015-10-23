#!/usr/bin/python

#//-----------------------------
#//          lib
#//-----------------------------
import sys
import csv
import datetime
from time import gmtime, strftime, strptime
import smtplib
import time
import subprocess
import os

#//---------------------------------
#// send mail function
#// http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email
#//---------------------------------
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

#//------------------------------
#//          main
#//------------------------------
#// 1. call linux system cmd - ifconfig and save data into file
#subprocess.call("ifconfig>rpi_ip.txt".split())
os.system("ifconfig>./rpi_ip.txt")

#// 2. open ip data file and mail the ip data
fd = file("./rpi_ip.txt", 'r')
ip_data = fd.read()
fd.close()
print ip_data

print 'start send mail...'
sendemail(from_addr    = 'python@RC.net',
          to_addr_list = ['tef2323@gmail.com'],
          cc_addr_list = [''],
          subject      = 'I am raspberry, Confessions RPI self IP address',
          message      = ip_data,
          login        = 'your mail',
          password     = 'your mail password')

print "\nsend mail done!\n"

#// 3. del rpi_ip.txt
os.system("rm ./rpi_ip.txt")
