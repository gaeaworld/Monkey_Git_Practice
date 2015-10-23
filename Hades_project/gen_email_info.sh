#!/bin/sh

echo "hi, welcome to Hades gen email info tool"

read -p "Please input email account, ex:abc@gmail.com : " user_account
read -p "please input email password : " user_password
echo $user_account > email_account.txt
echo $user_password > email_password.txt

echo "create done!"
