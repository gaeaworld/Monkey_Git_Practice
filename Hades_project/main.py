#!/usr/bin/python
# coding=UTF-8
#http://tech.marsw.tw/blog/2014/09/03/getting-started-with-python-in-ten-minute
#https://www.youtube.com/watch?v=MSOlZeDN3qc
#

#//-----------------------------
#//          lib
#//-----------------------------
import sys
import csv
import datetime
from time import gmtime, strftime, strptime
import smtplib
import time
#// 2. catch a stock value, like get 3231 value
from grs import Stock
import os

#//-----------------------------
#//          Debug
#//-----------------------------
TURN_ON = 1
TURN_OFF = 0
DEBUG = TURN_OFF
DEBUG_MAIL = TURN_ON

#//-----------------------------
#//          Variable
#//-----------------------------
Project_Path = "/home/pi/Hades_project/"

#//-----------------------------
#//          function
#// http://www.qttc.net/201209207.html
#//-----------------------------
#// create folder
def mkdir(path):

    path = path.strip()
    path = path.rstrip("/")

    isExists = os.path.exists(path)

    if not isExists:
        print path+' create ok!!'
        os.makedirs(path)
        return True
    else:
        #print path+' folder already exist!!'
        return False

#// search value in file
def search_s_e_h_l_fun(w_val, file_name):
    file_in_target = file(file_name, 'r')
    for row in csv.DictReader(file_in_target, ["data", "total_val", "unknow1", "start_val", "highest_val", "lowest_val", "end_val", "range_val", "unknow2"]):
        get_value = row[w_val]
        #print (w_val+':  '+ get_value)
    file_in_target.close()
    return get_value

#//---------------------------------
#// test day avaliable
#// find the specific date data
#// ok = 0, not ok = 1
#//---------------------------------
def test_day_avaliable(target_date, source_file):
    res_tmp = 0
    file_in = file(source_file, 'r')
    for line in file_in:
        str = line
        res = str.find(target_date)
        if(res > 0):
            res_tmp = 1
    if(res_tmp == 1):
        value = 0
    else:
        #print (target_date + " is holiday... stock market not open")
        value = 1
    file_in.close()
    return value

#//---------------------------------
#// gen target file
#// find the specific date data
#//---------------------------------
def gen_target_file(target_date, source_file, target_file):
    res_tmp = 0
    file_in = file(source_file, 'r')
    file_in_target = file(target_file, 'w')
    for line in file_in:
        str = line
        res = str.find(target_date)
        if(res > 0):
            res_tmp = 1
            #print line
            file_in_target.write(line)
    if(res_tmp == 1):
        #print line
        value = 0
    else:
        #print (target_date + " is holiday... stock market not open")
        value = 1
    file_in.close()
    file_in_target.close()
    return value

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

def init_record_trade_price_file(stock_number):

    #// 8.1 create trade folder and create trade file
    folder_name="/home/pi/Hades_project/trade_record"
    mkdir(folder_name)
    file_name = '/home/pi/Hades_project/trade_record/' + stock_number + '_tr_price.txt'

    isExists = os.path.exists(file_name)

    if not isExists:
        tr_file = open(file_name, 'w')
        tr_file.write("date              buy_price              sale_price\n")
        tr_file.close()
        return True
    else:
        #print path+' folder already exist!!'
        return False

#//---------------------------------
#// send mail function
#// 8. record file for record buy or sale price
# date        buy_price        sale_price
#2015/06/18   22.5
#2015/06/19                    30.5
#//---------------------------------
def record_trade_price(stock_number, price, motion):
    #// 8.2 write "date", "buy_price", "sale_price" into trade file
    file_name = '/home/pi/Hades_project/trade_record/' + stock_number + '_tr_price.txt'
    tr_file = open(file_name, 'a')
    today_date = datetime.date.today()
    today_date = str(today_date)
    if(motion == 'buy'):
        price_msg = today_date + '        ' + price + '\n'
    elif (motion == 'sale'):
        price_msg = today_date + '                               ' + price + '\n'
    tr_file.write(price_msg)
    tr_file.close()

#//---------------------------------
#// clean garbage file
#//---------------------------------
def clean_garbage_file(file_name):
    file = 'rm ' + file_name
    os.system(file)

#//---------------------------------
#// write CPU data into file
#//---------------------------------
def write_cpu_temp_file(cpu_temp):
    CPU_TEMP = cpu_temp

    #//save cpu temp into file
    file_name = '/home/pi/Hades_project/CPU_temperature.txt'
    isExists = os.path.exists(file_name)

    if not isExists:
        tr_file = open(file_name, 'w')
        print 'open new file\n'
    else:
        tr_file = open(file_name, 'a')
        print 'open old file\n'

    today_date = datetime.date.today()
    today_date = str(today_date)
    cpu_msg = today_date + '  CPU:' + CPU_TEMP + '\n'
    tr_file.write(cpu_msg)
    tr_file.close()
    print 'done!\n'

#//---------------------------------
#// get CPU temperture
#//---------------------------------
def get_cpu_temp():
    #//run get cpu cmd
    os.system("vcgencmd measure_temp > /home/pi/Hades_project/CPU_temperature.txt")
    file_name = '/home/pi/Hades_project/CPU_temperature.txt'
    fd = open(file_name, 'r')
    CPU_TEMP = fd.read()
    fd.close()
    CPU_TEMP = str(CPU_TEMP)
    print "now CPU " + CPU_TEMP
    return CPU_TEMP

#//---------------------------------
#// detect file exist or not
#//---------------------------------
def detect_file(file_name):
    isExists = os.path.exists(file_name)

    if not isExists:
        return 1
    else:
        return 0

#//---------------------------------
#// write mail file - mail_msg.txt
#//---------------------------------
def write_mail_msg(msg):
    filename = Project_Path + "mail_msg.txt"
    #10.1 open "mail_msg.txt"
    fd = open(filename, 'a')
    #10.2 write msg into file
    fd.write(msg)
    #10.3 close file
    fd.close()

#//---------------------------------
#// read mail file - mail_msg.txt
#//---------------------------------
def read_mail_msg():
    filename = Project_Path + "mail_msg.txt"
    #11.1 open "mail_msg.txt"
    fd = open(filename, 'r')
    #11.2 write msg into file
    res = fd.read()
    #11.3 close file
    fd.close()
    #11.4 return msg content
    return res

#//---------------------------------
#// clear mail file - mail_msg.txt
#//---------------------------------
def clear_mail_msg():
    filename = Project_Path + "mail_msg.txt"
    clear_msg = ''
    #13.1 open "mail_msg.txt"
    fd = open(filename, 'w')
    #13.2 write msg into file
    fd.write(clear_msg)
    #13.3 close file
    fd.close()

#//---------------------------------
#// 11.2 read account and password file
#// email_account.txt, email_password.txt
#//---------------------------------
def read_AP_file(file_choice):

    if(file_choice == 1):
        filename = Project_Path + "email_account.txt"
    elif(file_choice == 2):
        filename = Project_Path + "email_password.txt"
    else:
        print "file_choice error..."

    fd = open(filename, 'r')
    res = fd.read()
    fd.close()
    return res

#//---------------------------------
#// SEND MAIL function
#//---------------------------------
def SEND_MAIL_msg(MSG):
        #11.1 read email account and password from email_account.txt and email_password.txt
        MAIL_ACCOUNT = read_AP_file(1)
        MAIL_PASSWORD = read_AP_file(2)
        sendemail(from_addr    = 'python@RC.net',
                  to_addr_list = ['tef2323@gmail.com'],
                  cc_addr_list = [''],
                  subject      = 'Make money machine letter',
                  message      = MSG,
                  login        = MAIL_ACCOUNT,
                  password     = MAIL_PASSWORD)

#//---------------------------------
#// main_process
#//---------------------------------
def main_process(stock_number):
    global PIECE
    global sim_day
    global cdate1
    global cdate2
    global cdate3
    global sdate1
    global sdate2
    global sdate3
    cdate1 = datetime.date.today()
    cdate2 = datetime.date.today()
    cdate3 = datetime.date.today()
    sdate1 = '0'
    sdate2 = '0'
    sdate3 = '0'

    stock_wis = Stock(stock_number)
    #// 3. create folder for save csv data
    mkpath="/home/pi/Hades_project/csv_repository"
    mkdir(mkpath)
    get_date = datetime.date.today()
    get_sdate = str(get_date)
    csv_file = "/home/pi/Hades_project/csv_repository/" + stock_number + '_' + get_sdate + '.csv'
    stock_wis.out_putfile(csv_file)
    #// 3.1 create share of stock folder
    mkpath="/home/pi/Hades_project/share_stock"
    mkdir(mkpath)
    #// 3.2 record share of stock file
    filepath = '/home/pi/Hades_project/share_stock/' + stock_number + '.txt'
    isExists = os.path.exists(filepath)

    if not isExists:
        fd = open(filepath, 'w')
        piece_num = '0'
        fd.write(piece_num)
        fd.close
        PIECE = '0'
        print filepath+' create ok!!'
    else:        #print filepath+' folder already exist!!'
        fd = open(filepath, 'r')
        PIECE = fd.read()
        fd.close
        PIECE = PIECE.rstrip('\n')

    #// 4. filter highest, lower, end, start of value and show thos value
    # http://swaywang.blogspot.tw/2012/05/pythoncsv.html
    # http://www.lfhacks.com/tech/python-read-specific-column-csv
    #//---------------------------------
    #// get time function
    #//---------------------------------
    #sdate1 = strftime("%D")
    #ssdate1 = sdate1[0:5]
    #cdate1 = datetime.date.today() + (datetime.timedelta(days=sim_day))
    #cdate1 = datetime.date.today() + (datetime.timedelta(days=-4))
    #cdate2 = cdate1 + (datetime.timedelta(days=-1))
    #cdate3 = cdate1 + (datetime.timedelta(days=-2))

    #//current date,6/20
    check_done = 0
    delta_day = 0
    while(check_done == 0):
        cdate1 = datetime.date.today() + (datetime.timedelta(days=delta_day))
        sdate1 = str(cdate1)
        sdate1 = sdate1[5:10]
        sdate1 = sdate1.replace('-','/')
        res = test_day_avaliable(sdate1, csv_file)
        if(res == 0):
            #print sdate1
            #print "find a right day1!"
            check_done = 1
            #print "---------------"
        else:
            #print "can't find match day1!"
            delta_day = (delta_day - 1)

    #//yesterday,6/19
    check_done = 0
    delta_day = -1
    while(check_done == 0):
        cdate2 = cdate1 + (datetime.timedelta(days=delta_day))
        sdate2 = str(cdate2)
        sdate2 = sdate2[5:10]
        sdate2 = sdate2.replace('-','/')
        res = test_day_avaliable(sdate2, csv_file)
        if(res == 0):
            #print sdate2
            #print "find a right day2!"
            check_done = 1
            #print "---------------"
        else:
            #print "can't find match day2!"
            delta_day = (delta_day - 1)


    #//the day before yesterday,6/18
    check_done = 0
    delta_day = -1
    while(check_done == 0):
        cdate3 = cdate2 + (datetime.timedelta(days=delta_day))
        sdate3 = str(cdate3)
        sdate3 = sdate3[5:10]
        sdate3 = sdate3.replace('-','/')
        res = test_day_avaliable(sdate3, csv_file)
        if(res == 0):
            #print sdate3
            #print "find a right day3!"
            check_done = 1
            #print "---------------"
        else:
            #print "can't find match day3!"
            delta_day = (delta_day - 1)

    #//---------------------------------
    #//find the specific date data
    #//---------------------------------
    #print sdate1
    res1 = gen_target_file(sdate1, csv_file, '/home/pi/Hades_project/csv_repository/target_sdate1_val.txt')
    if(res1 == 0):
    #//day1,current date
    #//     4.1 hishest value
        day1_h = search_s_e_h_l_fun('highest_val', '/home/pi/Hades_project/csv_repository/target_sdate1_val.txt')
    #//     4.2 lower value
        day1_l = search_s_e_h_l_fun('lowest_val', '/home/pi/Hades_project/csv_repository/target_sdate1_val.txt')
    #//     4.3 end value
        day1_e = search_s_e_h_l_fun('end_val', '/home/pi/Hades_project/csv_repository/target_sdate1_val.txt')
    #//     4.4 start value
        day1_s = search_s_e_h_l_fun('start_val', '/home/pi/Hades_project/csv_repository/target_sdate1_val.txt')
        #print 'h:'+day1_h
        #print 'l:'+day1_l
        #print 'e:'+day1_e
        #print 's:'+day1_s
        clean_garbage_file('/home/pi/Hades_project/csv_repository/target_sdate1_val.txt')
    else:
        print "Error :day1 not avaible~"
        return 1
    #print "---------------"

    #print sdate2
    res2 = gen_target_file(sdate2, csv_file, '/home/pi/Hades_project/csv_repository/target_sdate2_val.txt')
    #//day2,yesterday
    if(res2 == 0):
        day2_h = search_s_e_h_l_fun('highest_val', '/home/pi/Hades_project/csv_repository/target_sdate2_val.txt')
        day2_l = search_s_e_h_l_fun('lowest_val', '/home/pi/Hades_project/csv_repository/target_sdate2_val.txt')
        day2_e = search_s_e_h_l_fun('end_val', '/home/pi/Hades_project/csv_repository/target_sdate2_val.txt')
        day2_s = search_s_e_h_l_fun('start_val', '/home/pi/Hades_project/csv_repository/target_sdate2_val.txt')
        #print 'h:'+day2_h
        #print 'l:'+day2_l
        #print 'e:'+day2_e
        #print 's:'+day2_s
        clean_garbage_file('/home/pi/Hades_project/csv_repository/target_sdate2_val.txt')
    else:
        print "Error :day2 not avaible~"
        return 1
    #print "---------------"

    #print sdate3
    res3 = gen_target_file(sdate3, csv_file, '/home/pi/Hades_project/csv_repository/target_sdate3_val.txt')
    #//day3,the day before yesterday
    if(res3 == 0):
        day3_h = search_s_e_h_l_fun('highest_val', '/home/pi/Hades_project/csv_repository/target_sdate3_val.txt')
        day3_l = search_s_e_h_l_fun('lowest_val', '/home/pi/Hades_project/csv_repository/target_sdate3_val.txt')
        day3_e = search_s_e_h_l_fun('end_val', '/home/pi/Hades_project/csv_repository/target_sdate3_val.txt')
        day3_s = search_s_e_h_l_fun('start_val', '/home/pi/Hades_project/csv_repository/target_sdate3_val.txt')
        #print 'h:'+day3_h
        #print 'l:'+day3_l
        #print 'e:'+day3_e
        #print 's:'+day3_s
        clean_garbage_file('/home/pi/Hades_project/csv_repository/target_sdate3_val.txt')
    else:
        print "Error :day3 not avaible~"
        return 1
    #print "---------------"
    #// 5. algorithm to compare value bigger or lower

    #// 5.3 if you have share of stock, if you have 1 PIECE go to sale session,
    #//     otherwise go to buy session
    if(PIECE == '0'): #// share of stock is none
        #// 5.1 three day detection algorithm, buy in
        #// 5.4 stage = 1 -> buy, 2 -> do not buy
        print "+++++ BUY Session ++++"
        if(day1_h > day3_h):
            print (sdate1+" is high than "+sdate3+", BUY!")
            stage = 1
            print "buy in share of 1000"
            PIECE = 1000
            fd = open(filepath, 'w')
            piece_num = '1000'
            fd.write(piece_num)
            fd.close
            record_trade_price(stock_number, day1_h, 'buy')
        else:
            print (sdate1+" is high than "+sdate3+", DO NOT BUY!")
            stage = 2
    elif(PIECE == '1000'): #// share of stock is 1
        #// 5.2 three day detection algorithm, sale out
        #// 5.4 stage = 3 ->sale out, 4 -> keep
        print "+++++ SALE Session ++++"
        if(day1_e < day3_e):
            print (sdate1+" is lower than "+sdate3+", SALE OUT!")
            stage = 3
            print "sale out share of 1000"
            PIECE = 0
            fd = open(filepath, 'w')
            piece_num = '0'
            fd.write(piece_num)
            fd.close
            record_trade_price(stock_number, day1_e, 'sale')
        else:
            print sdate1+" is higher or equal than "+sdate3+", KEEP!"
            stage = 4
    else:
        print "something wrong about share of stock..."

    #// 9. CPU record
    cpu_tempertrue_value = get_cpu_temp()
    #cpu_tempertrue_value = str(40)
    write_cpu_temp_file(cpu_tempertrue_value)
    cpu_tempertrue_value = "now CPU " + str(cpu_tempertrue_value)

    today_date = datetime.date.today()
    today_date = str(today_date)
    #// 5.5 use a switch to give different msg to "result_message" for mail
    if(stage == 1):
        result_message = today_date+"  "+stock_number+" \nmachine say:  "+" BUY!!\n"+"today final price: "+day1_e+"\n"+cpu_tempertrue_value
    elif(stage == 2):
        result_message = today_date+"  "+stock_number+" \nmachine say:  "+" DO NOT BUY!!\n"+"today final price: "+day1_e+"\n"+cpu_tempertrue_value
    elif(stage == 3):
        result_message = today_date+"  "+stock_number+" \nmachine say:  "+" SALE OUT!!\n"+"today final price: "+day1_e+"\n"+cpu_tempertrue_value
    elif(stage == 4):
        result_message = today_date+"  "+stock_number+" \nmachine say:  "+" KEEP!!\n"+"today final price: "+day1_e+"\n"+cpu_tempertrue_value
    else:
        print "stage going wrong..."

    #// 6. send mail to notice user
    #// issue: cc wouldn't work!
    #// to_addr_list = ['tef2323@gmail.com','williamultra@gmail.com']
    #if(DEBUG == TURN_OFF):
    if(DEBUG_MAIL == TURN_ON):
        #sendemail(from_addr    = 'python@RC.net',
        #          to_addr_list = ['tef2323@gmail.com'],
        #          cc_addr_list = [''],
        #          subject      = 'Make money machine letter',
        #          message      = result_message,
        #          login        = 'tef2323@gmail.com',
        #          password     = '1QAZ@wsx')
        deal_result_message = result_message
        #//read trade record file
        file_name = '/home/pi/Hades_project/trade_record/' + stock_number + '_tr_price.txt'
        tr_file = open(file_name, 'r')
        trade_result_message = tr_file.read()
        result_message = deal_result_message + '\n' +  trade_result_message
        tr_file.close()

        write_mail_msg(result_message)
        between_line = "\n--------------------------------------------------------\n"
        write_mail_msg(between_line)

#//------------------------------
#//          main
#//------------------------------
#// 1. show program start
print "===================================================="
print '\n##### Welcome to Make Money Machine World ##### \n'
print "===================================================="
#//share of stock
PIECE = 0

#//MUST DO! : your stock number
STOCK_1 =  '6505'
STOCK_2 =  '2823'
STOCK_3 =  '2345'
STOCK_4 =  '1444'
STOCK_5 =  '3576'
STOCK_6 =  '4915'
STOCK_7 =  '3682'
STOCK_8 =  '2887'
STOCK_9 =  '3016'
STOCK_10 = '2911'
#//MUST DO! : create record trade price file
init_record_trade_price_file(STOCK_1)
init_record_trade_price_file(STOCK_2)
init_record_trade_price_file(STOCK_3)
init_record_trade_price_file(STOCK_4)
init_record_trade_price_file(STOCK_5)
init_record_trade_price_file(STOCK_6)
init_record_trade_price_file(STOCK_7)
init_record_trade_price_file(STOCK_8)
init_record_trade_price_file(STOCK_9)
init_record_trade_price_file(STOCK_10)

#// 7. timer, ruting to run this
print "start ticking..."
forever = 10

tStart = time.time()
if(DEBUG == TURN_ON):
    #//use for simulate the day
    sim_day = -8
    forever = 1
    while (forever > 0):
        tEnd = time.time()
        #1day=(24*(60*60))
        if((tEnd-tStart) >= (5)):
            print "time up..."
            today = datetime.date.today()
            today = str(today)
            print 'today is : ' + today
            clear_mail_msg()
            main_process(STOCK_1)
            print "---------------"
            main_process(STOCK_2)
            print "---------------"

            MAIL_MSG = read_mail_msg()
            #print MAIL_MSG
            SEND_MAIL_msg(MAIL_MSG)

            print "\n send mail done!\n"

            print "now, share of " + STOCK_1 + ":" + str(PIECE)
            print "now, share of " + STOCK_2 + ":" + str(PIECE)
            tStart = time.time() #//restart timer
            print "start ticking..."
            sim_day = -7
            print "===================================================="
            forever = (forever - 1 )

else:
    print "time up..."
    today = datetime.date.today()
    today = str(today)
    print 'today is : ' + today
    clear_mail_msg()
    print "---------------"
    main_process(STOCK_1)
    print "---------------"
    main_process(STOCK_2)
    print "---------------"
    main_process(STOCK_3)
    print "---------------"
    main_process(STOCK_4)
    print "---------------"
    main_process(STOCK_5)
    print "---------------"
    main_process(STOCK_6)
    print "---------------"
    main_process(STOCK_7)
    print "---------------"
    main_process(STOCK_8)
    print "---------------"
    main_process(STOCK_9)
    print "---------------"
    main_process(STOCK_10)
    print "---------------"


    MAIL_MSG = read_mail_msg()
    #//print MAIL_MSG
    SEND_MAIL_msg(MAIL_MSG)

    print "\n send mail done!\n"

    #print "now, share of " + STOCK_1 + ":" + str(PIECE)
    #print "now, share of " + STOCK_2 + ":" + str(PIECE)
    print "start ticking..."
    print "===================================================="
print "end~"

