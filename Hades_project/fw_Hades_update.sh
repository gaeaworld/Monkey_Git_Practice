#!/bin/sh

PID=0
while [ 1 ]; do
    #echo "----- Hades FW update -----"
    if [ -f "/home/pi/Hades_project/upload/main.py" ]; then
        #file exist
        echo "file exists."
        echo "----- fw update successfully -----"
        cp /home/pi/Hades_project/upload/main.py /home/pi/Hades_project
        sudo chmod 777 /home/pi/Hades_project/main.py
        echo "----- delete fw file -----"
        rm -f /home/pi/Hades_project/upload/main.py
	#PID=echo pgrep main.py
        #echo $PID
        #echo "kill old main.py fw"
        #sudo kill -9 $PID
        #echo "restart fw"
        #/home/pi/start_release_Hades.sh
    else
        #file not exist
        #echo "file not exists."
        #continue
        echo ""
    fi
    if [ -f "/home/pi/Hades_project/upload/index.html" ]; then
        #file exist
        echo "file exists."
        echo "----- fw update html successfully -----"
        sudo cp /home/pi/Hades_project/upload/index.html /home/pi/Hades_project/www
        echo "----- delete fw file -----"
        sudo rm -f /home/pi/Hades_project/upload/index.html
    else
        #file not exist
        #echo "file not exists."
        #continue
        echo ""
    fi
done
