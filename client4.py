# -*- coding: utf-8 -*-
# client3.py
# python3 client3.py HostName PortNumber

from socket import *
import time
import sys
import pbl2017
import shutil
from fileinput import filename

hostlist = ['pbl1','pbl2','pbl3','pbl4','pbl5']

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
    print(arg_str[4])
    #getarg = pbl2017.genkey(token_str)
    getarg = "e8cf514f7e854da883e9a26421acf2db35d455e7c6ad33435d003678abd8eb00"
    print("hash:",getarg)
    sentence = '{} {} {} {} \n'.format("GETFILE",filename,getarg,int(arg_str[2]))
    #GETFILE rnd50K.txt toke_nstr server_port
    client_socket.send(sentence.encode())
    res_str = receive_data(client_socket)#データを受信
    print(res_str)
  
def rep_request_client(filename,client_socket,token_str):
    sentence = 'REP {} {}\n'.format(filename,pbl2017.repkey(token_str,filename))
    print(sentence)
    client_socket.send(sentence.encode())
    res_str = receive_data(client_socket)#データを受信
    print(res_str)
    
def main():#main
    if len(sys.argv) < 5:
        sys.exit('Usage: python3 client4.py [Server_Host] [PortNumber] [File_Name] [token_str]')
    
    server_name = sys.argv[1]     #ホスト名
    server_port = int(sys.argv[2])#ポート番号
    filename = sys.argv[3]          #ファイル名
    token_str = sys.argv[4]        #トークン文字列
    #print(token_str)
    ft_port = 50000
    cl_port = 50001
    #ファイル転送プログラムに接続
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, ft_port))  # サーバのソケットに接続する
    GET_FILE_request(sys.argv,client_socket)
    client_socket.close()  
    
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', cl_port))
    s.listen(1)
    print('Transmitting file...')
    connection_socket, addr = s.accept()
    sentence = receive_data2(connection_socket)
    print(sentence)
    s.close()
    
    shutil.copy("filedata.dat",filename)
    
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, 60623))  # サーバのソケットに接続する
    #GET_FILE_request(sys.argv,client_socket)
    
    rep_request_client(filename,client_socket,token_str)
    
    
    client_socket.close()  
    
if __name__ == '__main__':
     main()