# -*- coding: utf-8 -*-
# bwcheck_server.py PortNumber
# bwcheck_server.py

import random
from socket import *
import threading  # for Thread()
import os.path
import pbl2017
import sys
import time

server_port = int(sys.argv[1])  ##ポート番号##

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

def size_request_server(word_list,s):#SIZEリクエスト
    filename = word_list[1]
    try:
        file_size = os.path.getsize(filename)
        s.send('{0} {1} bytes\n'.format(filename,file_size).encode()) 
    except:
        s.send('No such file\n'.encode()) 
    
def get_request_server(word_list,s,token_str):#GETリクエスト
    filename = word_list[1]
    if word_list[2] == pbl2017.genkey(token_str):#トークンが一致した場合
        if word_list[3] == 'ALL':#ALL
            try:
                f = open(filename)
                file_size = os.path.getsize(filename)
                sentence = 'OK Sending {} from 0 to {} total {} bytes at {}\n'.format(filename,file_size-1,file_size,time.time())
                s.send(sentence.encode())
                #print(sentence)
                tmp_data = f.read()
                s.send(tmp_data.encode())
            except:
                print('NG 101 NO such file')
                s.send('NG 101 NO such file\n'.encode())
        elif word_list[3] == 'PARTIAL':#PARTIAL
            try:
                f = open(filename)
                offset = int(word_list[4])
                length = int(word_list[5])
                sentence = 'OK Sending {} from {} to {} total {} bytes\n'.format(filename,offset,length,length-offset+1)
                s.send(sentence.encode())
                print(sentence)
                f.seek(offset)
                tmp_data = f.read(length)
                #tmp_data +='\n'
                s.send(tmp_data.encode())
            except:
                print('NG 101 NO such file')
                s.send('NG 101 NO such file\n'.encode())  
    else:#トークンが一致しない場合
        s.send('NG 103 Invalid hash value for file {} with {} '.format(filename,token_str).encode())
    ##修正必要あり
def rep_request_server(word_list,s,token_str):#REPリクエスト
    try:
        if (pbl2017.keycheck(word_list[3],word_list[1]) == True):
            sentence = 'OK Degest of {} with {} was successfully received REP at {}\n'.format(word_list[1],word_list[2],time.time())
            s.send(sentence.encode())
            print(">OK")
        else:
            print('>NG')
            s.send('NG 103 Invalid hash for file\n'.encode())
    except:
        s.send('NG 101 NO such file\n'.encode())
    
def interact_with_client(s):
    token_str = "abcde"
    #sentence = s.recv(1024).decode()#1回目のclientからのデータ受信SIZE,GET,REP...
    tmp_sentence = receive_data2(s)
    sentence = tmp_sentence
    print('受信:',end="")
    word_list = sentence.split()
    
    if len(word_list) == 0:#word_listが何もなし
        print('Invalid_request')
        s.send('NG 301 Invalid command\n'.encode())
    elif word_list[0] == 'SIZE':#SIZE
        print('SIZE_request')
        size_request_server(word_list,s)
    elif word_list[0] == 'GET':#GET
        print('GET_request')
        get_request_server(word_list,s,token_str)
    elif word_list[0] == 'REP':#REP
        print('REP_request')
        rep_request_server(word_list,s,token_str)
    else:
        print('Invalid_request')
        s.send('NG 301 Invalid command\n'.encode())

    s.close()
    
def main():#main
    if len(sys.argv) < 2:
        sys.exit('Usage: python3 server2.py')
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(10)
  
    print('The server is ready to receive')
    while True:
        connection_socket, addr = server_socket.accept()

    # スレッドを作り、そこで動かす関数と引数をスレッドに与える
    #   argsに与えるのはタプル(xxx, xxx, ...)でないといけないので、
    #   たとえ引数が一つであっても、括弧で囲い、かつ一つめの要素のあとにカンマを入れる。
        client_handler = threading.Thread(target=interact_with_client, args=(connection_socket,))
        client_handler.start()  # スレッドを開始
    
if __name__ == '__main__':
    main()
