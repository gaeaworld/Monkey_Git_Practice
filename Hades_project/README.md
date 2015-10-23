# Hades_project

###modify date:20150719,21:18

### Start Hades stop:
    (1) run gen_email_info.sh to config personal email info for Hades.
    (2) run command "crontab -e" and input string as following
        00 18 * * 1-5 /home/pi/Hades_project/start_service.sh
        example mean run Hades ervery 18:00 day from mon to fri.

#
###install grs and example and step:
	sudo apt-get install python-dev
	sudp apt-get install python-pip
	sudo pip install grs
###python
	>>> from grs import Stock
	>>> Stock('2618').info
#
###version:0.03

###20150617 - version 0.01
			(1) list bone of program
###20150619 - version 0.01
			(1) search value in file sub function
###20150620 - version 0.01
			(1) gen target file to save target value
			(2) finish date and yesterday and the day before yesterday calculate
			(3) timer function
			(4) send mail function
###20150621 - version 0.01
			(1) algorithm of buy and keep
###20150622 - version 0.02
			(1) define main_process function
			(2) timer can ruting to call main_process function
			(3) create share folder for record share of stock
			(4) base algonism to auto sale out and buy in stock
			(5) record trade price file
###20150624 - versioin 0.02
			(1) run many stock in one time
			(2) Debug flag
			(3) rm "target_sdate1_val.txt"
			(4) different stock save diff csv file
###20150701 - version 0.03
			(1) use "cron" table to count day,"cron" to loop main.py, only run main.py at mon to fri
				x1. sudo su, no need do this step
				2. crontab -e
				3. 40 13 * * 1-5 /home/pi/Hades_project/main.py > /home/pi/Hades_project/syslog.txt
				4. /etc/init.d/cron restart
			(2) apach2 server as fw update interface
				1. input 192.168.1.116 into browser
				2. chose the main.py
				3. the script "fw_Hades_update.sh" will take care of replace main.py file
			(3) merge mail "keep or sale" & "trade price" into one mail
			(4) record CPU temp into mail and file(CPU_temp.txt)
###20150704 - version 0.04
			(1) two Stock should send one mail
			(2) show version in fw website

###20150707 - version 0.04
            (1) change loop to 18:00 for insure Hades can get correct csv file.
                1. crontab -e
                2. 00 18 * * 1-5 /home/pi/Hades_project/start_service.sh
            (2) fix can't auto update main.py fw from website.
                modify "fw_Hades_update.sh" line 24 and line 37to echo something

###20150714 - version 0.04
            (1) add new logic about buy and sale session
                #//5.3 if you have share of stock
                #//5.4 stage = 1:buy, 2:do not buy, 3:sale out, 4. keep
                #//5.5 use a switch to give different msg to "result_message" for mail

###20150715 - version 0.04
            (1) important!! change email account and password read rule.
                change to read local file "mail_account.txt" and "mail_password.txt"
                to fill out the python mail function.
                1.use gen_email_info.sh to gen "email_account.txt" and "email_password.txt
                2.Hades to read those two file and save to a variable
                3.put those two variable into send mail function


###Next action:
			*-* read a external file.txt which your stock list as "STOCK=" input
                1.read STOCK_list.txt to get user want monitor STOCK number.
                2.put each one stock into variable "STOCK"
                3.input how much share of stock below stock number like
                  6505
                  1000
            *-* buy price should be next day begin price and sel price should, too.
			*-* read STOCK_list.txt about share of stock and write into record share file
			*-* csv file depand on different folder to save
			*-* calculate the grow slope.
			*-* auto read STOCK number instead input manual.

