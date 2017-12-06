# -*- coding: utf-8 -*-
# file_trancefer.py PortNumber
# bwcheck_server.py

import random
from socket import *
import threading  # for Thread()
import os.path
import sys
import time

#passlist = ['localhost','pbl2','pbl1']#経路リスト
passlist = ['localhost','azm.mydns.jp']
hostlist = ['pbl1','pbl2','pbl3','pbl4','pbl5']
#clienthost = 'pbl5'  ##クライアントホスト
#serverhost = 'pbl2'  ##サーバーホスト
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
def nextpasslist():
    uname =  os.uname()[1]
    for n in range(len(passlist)):
        if passlist[n] == uname:
            try:
                nextpass = passlist[n+1]
                print(nextpass)
                return nextpass
            except:
                return 0
            break

def SEND_request_s(server_name):
    
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, server_port))
    
    sentence = "SEND \n"
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

def SEND_request(word_list,s):#SEND,データを受け取る
    sentence = "OK \n"
    #print(sentence)
    s.send(sentence.encode())#応答OK
    ALL_file_data = receive_data(s)#data受信
    print(">[filedata]:",ALL_file_data,':')

def interact_with_client(s):
    print('>>>Request受信:',end ='')
    sentence = s.recv(1024).decode()#1回目のclientからの要求受信
    word_list = sentence.split()
    
    if len(word_list) == 0:#word_listが何もなし
        print('Invalid_request')
        s.send('NG 301 Invalid command\n'.encode())
    elif word_list[0] == 'SEND':#SEND
        print('SEND_request')
        print(">FILE受信中...")
        SEND_request(word_list,s)
        print(">...OK")
    s.close()
    
    nextpass = nextpasslist()
    if nextpass != 0:
        SEND_request_s(nextpass)
        
    
def main():#main
    if len(sys.argv) < 2:
        sys.exit('Usage: python3 server2.py PortNumber')
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
