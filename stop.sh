#!/bin/sh
expect -c "
  spawn ssh lab-pc
  
  expect \":~\"
  send \"ssh pblm\n\"
  
  expect \" ~]& \"
  send \"ssh pbl3 \n\"
  
  expect \"~]\"
  send \"python3 ~/pbl/program/file_transfer.py \n\"
  
  expect \"~]\"
  send \"exit \n\"
  
  expect \"~]\"
  send \"exit \n\"
  
  expect \":~\"
  send \"exit \n\"
  expect \":~$\"
"
