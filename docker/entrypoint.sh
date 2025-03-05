#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo $DIR
cd $DIR
cd ..
mkdir run-log
mv reboot.log run-log/"$(date +"old-%m-%d-%y--%T.%N")".log
date > reboot.log
echo DIR=$DIR | tee -a reboot.log
export PY_CRON=enable
env | tee -a reboot.log
python -m pip install --upgrade pip  | tee -a reboot.log
python -m pip install --upgrade wwwpy | tee -a reboot.log
python -m pip install -r requirements.txt --upgrade  | tee -a reboot.log
./server_forever.sh  2>&1 | tee -a reboot.log
