# -*- coding: utf-8 -*-
# file_trancefer.py PortNumber
# bwcheck_server.py

import random
from socket import *
import threading  # for Thread()
import os.path
import sys
import time

#passlist = ['pbl1','pbl2','pbl3','pbl4']#経路リスト
passlist = ['pbl5','pbl1','pbl2']
#passlist = ['azm-ubuntu','azm.mydns.jp']
token_str = "abcde"
#passlist = []
hostlist = ['pbl1','pbl2','pbl3','pbl4','pbl5']
#clienthost = 'pbl5'  ##クライアントホスト
serverhost = 'pbl2'  ##サーバーホスト
server_port = int(sys.argv[1])  ##ポート番号

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

def size_request_client(input_list,client_socket):#SIZEリクエスト
    try:
        filename = input_list[1]
    except:
        print("ファイル名が入力されていません")
        sys.exit()
    sentence = '{} {} \n'.format("SIZE",filename)
    client_socket.send(sentence.encode())
    res_str = receive_data(client_socket)#データを受信
    print(res_str)
  
def get_request_client(input_list,client_socket,getarg):#GETリクエスト
    #getarg = pbl2017.genkey(token_str)#トークン文字列から生成したダイジェスト文字列を代入
    if (input_list[2] == 'ALL'):#ALL
        sentence = 'GET {} {} {}\n'.format(input_list[1],getarg,'ALL')#GET filename token ALL/PARTIAL sNUM gNUM
        print("[TO server]\n" + sentence)
        client_socket.send(sentence.encode())#サーバーへリクエスト
        res_str = receive_data2(client_socket)#サーバーからの応答を受信
        #res_str = client_socket.recv(1024).decode()
        print('[FROM server]\n' + res_str)
        if(res_str.split()[0] == 'OK'):#OK
            ALL_file_data = receive_data(client_socket)#ファイルデータ受信
            f = open('filedata.txt','w')
            print("aaa")
            f.write(ALL_file_data)
            f.close()
            print("OKOKOK")
        elif(res_str.split()[0] == 'NG'):#NG
            print(res_str)
  
    elif (input_list[2] == 'PARTIAL'):#PARTIAL
        sentence = 'GET {0} {1} PARTIAL {2} {3}\n'.format(input_list[1],getarg,input_list[3],input_list[4])
        print("[TO server]\n" + sentence)
        client_socket.send(sentence.encode())#サーバーへリクエスト
        res_str = receive_data(client_socket)#サーバーからの応答を受信
        #res_str = client_socket.recv(1024).decode()
        print('[FROM server]\n' + res_str)
        if(res_str.split()[0] == 'OK'):
            PARTIAL_file_data = receive_data(client_socket)
            print(PARTIAL_file_data)
            print(res_str)
        elif(res_str.split()[0] == 'NG'):
            print(res_str)

def rep_request_client(input_list,client_socket,token_str):
    sentence = 'REP {} {}\n'.format(input_list[1],pbl2017.repkey(token_str,input_list[1]))
    print(sentence)
    client_socket.send(sentence.encode())
    res_str = receive_data(client_socket)#データを受信
    #if(res_str.split()[0] == 'OK'):
    print(res_str)

def nextpasslist():
    uname =  os.uname()[1]
    for n in range(len(passlist)):
        if passlist[n] == uname:
                try:
                    nextpass = passlist[n+1]
                    print(nextpass)
                except:
                    nextpass = None
                return nextpass

def SEND_FILE_request_next(server_name):
    print("Connect to" ,server_name)
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, server_port))
    
    sentence = "SEND FILE \n"
    client_socket.send(sentence.encode())
    #res_str = receive_data(client_socket)
    res_str = client_socket.recv(1024).decode()
    res_str_list = res_str.split()
    print(res_str)
    if res_str_list[0] == 'OK':
        print("SEND_FILE_DATA...",end='')
        filedata = "Helllo,World!!!"   ####ファイル送信####
        client_socket.send(filedata.encode())
        print('完了！')
    client_socket.close()

def SEND_FILE_request(word_list,s):#SEND,データを受け取る
    s.send("OK \n".encode())#応答OK
    ALL_file_data = receive_data(s)#data受信
    print(">[filedata]:",ALL_file_data,':')
    
def SEND_PASS_request(s):
    s.send("OK \n".encode())
    sentence = receive_data(s)
    passlist = sentence.split()
    print("<<経路情報更新>>")
    print(passlist)
    
def get_request_ft(word_list,client_socket):
    #GET [filename] [ALL or PARTIAL] ([from]) ([to])
    sentence = "GET {} {}".format(word_list[1],"ALL","0","0")
    getarg = word_list[2]
    input_list = sentence.split()
    get_request_client(input_list,client_socket,getarg)
    nextpass = nextpasslist()
    print(nextpass)
    if nextpass != None:
        SEND_FILE_request_next(nextpass)
    
def interact_with_client(s):
    print('>>>Request受信:',end ='')
    sentence = s.recv(1024).decode()#1回目のclientからの要求受信
    print(sentence)
    word_list = sentence.split()
    
    if len(word_list) == 0:#word_listが何もなし
        print('Invalid_request')
        s.send('NG 301 Invalid command\n'.encode())
        s.close()
        
    elif word_list[0] == 'SEND':#SEND FILE [filename]
        if word_list[1] == 'FILE':
            print('SEND_FILE_Request')
            print(">FILE受信中...")
            SEND_FILE_request(word_list,s)
            print(">...OK")
            s.close()
            nextpass = nextpasslist()
            if nextpass != None:
                SEND_FILE_request_next(nextpass)
        elif word_list[1] == 'PASS':
            print('SEND_PASS_Request')
            SEND_PASS_request(s)
    elif word_list[0] == 'GETFILE':  #wordlist:GETFILE [filename] [token_strのダイジェスト] [serverport]
        print("GETFILE")
        #GET [filename] [ALL or PARTIAL] ([from]) ([to])
        s.close()
        server_port = int(word_list[3])
        client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
        client_socket.connect(('localhost',server_port))
        
        get_request_ft(word_list,client_socket)
        
        s.close()
        #GET [filename] [ALL or PARTIAL] ([from]) ([to])
    
def main():#main
    if len(sys.argv) < 2:
        sys.exit('Usage: python3 file_transfer.py [PortNumber]')
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(10)
    
    print('FILE Trancefer Program is running...')
    print(' [INFMATION]')
    sentence = ' ホスト名:{},ポート番号:{}'.format(os.uname()[1],server_port)
    print(sentence)
    print('...')
    while True:
        connection_socket, addr = server_socket.accept()

    # スレッドを作り、そこで動かす関数と引数をスレッドに与える
    #   argsに与えるのはタプル(xxx, xxx, ...)でないといけないので、
    #   たとえ引数が一つであっても、括弧で囲い、かつ一つめの要素のあとにカンマを入れる。
        client_handler = threading.Thread(target=interact_with_client, args=(connection_socket,))
        client_handler.start()  # スレッドを開始
    
if __name__ == '__main__':
    main()
    
