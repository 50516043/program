# -*- coding: utf-8 -*-
# client3.py
# python3 client3.py HostName PortNumber

from socket import *
import time
import sys
import pbl2017
import shutil
import math
import os.path

#hostlist2 = ['pbl1','pbl2','pbl3','pbl4','pbl5']
hostlist2 = ['pbl1','pbl2','pbl3','pbl4','pbl5','pbl6','pbl7']
hostlist=[]
ft_port = 54900
cl_port = 54901
rep_sentence=''
server_name =''

def receive_data(client_socket):#データ受信関数,aの長さが0のとき終了
    response_server = bytearray()
    while True:
        a =  client_socket.recv(1)#1024バイトずつ
        if len(a)<=0 :
            break
        response_server.append(a[0])
    receive_str = response_server.decode()
    return receive_str

def receive_data2(client_socket):#データ受信関数,改行で終了
    response_server = bytearray()
    while True:
        a =  client_socket.recv(1)#1バイトずつ
        if len(a)==0:
            continue
        response_server.append(a[0])
        if a == b'\n':
            break
    receive_str = response_server.decode()
    return receive_str

def GET_FILE_request(arg_str,client_socket):
    filename = arg_str[3]
    token_str = arg_str[4]
    print('token_str:',arg_str[4])
    getarg = pbl2017.genkey(token_str)
    print("hash:",getarg)
    sentence = '{} {} {} {} \n'.format("GETFILE",filename,getarg,int(arg_str[2]))
    #GETFILE rnd50K.txt toke_nstr server_port
    client_socket.send(sentence.encode())
    res_str = receive_data(client_socket)#データを受信
    print(res_str)
  
def rep_request_client(filename,client_socket,token_str):
    global rep_sentence
    sentence = 'REP {} {}\n'.format(filename,pbl2017.repkey(token_str,filename))
    #print(sentence)
    client_socket.send(sentence.encode())
    rep_sentence = receive_data2(client_socket)#REP時間
    #print(rep_sentence)
    
def time_request():
    bandwidth_list = []
    for i in range(len(hostlist)):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((hostlist[i], ft_port))
        s.send('TIMELIST \n'.encode())
        sentence = receive_data(s)
        print(sentence)
        tmp_list = sentence.split()
        s.close()
        for i in range(2,len(tmp_list)):
            bandwidth_list.append(tmp_list[i])  
    #print(bandwidth_list)
    return bandwidth_list
def send_passlist(passlist):
    sentence = ''
    for i in range(len(passlist)):
        sentence += '{} '.format(passlist[i])
    for i in range(len(hostlist)):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((hostlist[i], ft_port))
        s.send('PASSLIST \n'.encode())
        res_str = receive_data2(s)
        s.send(sentence.encode())
        s.close()
    
def send_info():
    uname =  os.uname()[1]
    sentence = '{} {} {} '.format('client',uname,'hostlist')
    for i in range(len(hostlist)):
        sentence += '{} '.format(hostlist[i])
    sentence += '\n'
    
    for i in range(len(hostlist2)):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((hostlist2[i], ft_port))
        s.send('INFO \n'.encode())
        s.send(sentence.encode())
        s.close()
    
def main():#main
    if len(sys.argv) < 3:
        sys.exit('Usage: python3 client4.py [Server_Host] [PortNumber]')
    
    global server_name
    global hostlist
    server_name = sys.argv[1]     #ホスト名
    server_port = int(sys.argv[2])#ポート番号
    #filename = sys.argv[3]          #ファイル名
    #token_str = sys.argv[4]        #トークン文字列
    #passlist = []
    #uname =  os.uname()[1]
    #hostlist.append(server_name)
    #for n in range(len(hostlist2)):
    #    if server_name != hostlist2[n] and uname != hostlist2[n]:
    #        hostlist.append(hostlist2[n])
    #hostlist.append(uname)
    #print(hostlist)
    
    #send_info()
    print('帯域幅計測')
    
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((hostlist2[0], ft_port))
    client_socket.send('BANDWIDTH CALCULATION \n'.encode())
    client_socket.close()
            
if __name__ == '__main__':
     main()
