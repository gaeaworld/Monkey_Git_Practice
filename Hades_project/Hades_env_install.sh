#!/bin/sh

project_path="/home/pi/Hades_project"
env_folder="$project_path/Hades_env"
up_folder="$project_path/upload"
fw_file="$env_folder/fw_Hades_update.sh"
www_folder="/home/pi/Hades_project/www"

echo "----------install python lib--------------"
sudo apt-get install python-pip
sudo pip install grs
echo "ok"
echo "----------------------------------------"

echo "----------create Hades_env--------------"
mkdir $env_folder
echo "ok"
echo "----------------------------------------"

echo "--------create fw upload folder---------"
mkdir $up_folder
chmod 777 $up_folder
echo "ok"
echo "----------------------------------------"

echo "--------install apache2 and PHP---------"
sudo apt-get install apache2 php5 libapache2-mod-php5
echo "ok"
echo "----------------------------------------"

echo "----------create fw script---------------"
touch $fw_file
echo "#!/bin/sh"                                                  >> $fw_file
echo "while [ 1 ]; do"                                            >> $fw_file
echo "    #echo "----- Hades FW update -----""                    >> $fw_file
echo "    if [ -f "/home/pi/upload/main.py" ]; then"              >> $fw_file
echo "        #file exist"                                        >> $fw_file
echo "        echo "file exists.""                                >> $fw_file
echo "        echo "----- fw update successfully -----""          >> $fw_file
echo "        cp /home/pi/upload/main.py /home/pi/Hades_project"  >> $fw_file
echo "        sudo chmod 777 /home/pi/Hades_project/main.py"      >> $fw_file
echo "        echo "----- delete fw file -----""                  >> $fw_file
echo "        rm -f /home/pi/upload/main.py"                      >> $fw_file
echo "    else"                                                   >> $fw_file
echo "        #file not exist"                                    >> $fw_file
echo "        #echo "file not exists.""                           >> $fw_file
echo "        continue"                                           >> $fw_file
echo "    fi"                                                     >> $fw_file
echo "done"                                                       >> $fw_file
echo "ok"
echo "----------------------------------------"

echo "--modify re.local for auto run fw_Hades_upate.sh at background--"
echo "continue..."
#echo "$fw_file &" >> /etc/rc.local
#echo "ok"
echo "----------------------------------------"

echo "--auto replace new fw and kill old fw---"
echo "continue..."
#echo "ok"
echo "----------------------------------------"

echo "------update php fw web site file-------"
echo "continue..."
echo "---create www folder---"
sudo cp $www_folder/* /var/www
#echo "ok"
echo "----------------------------------------"
