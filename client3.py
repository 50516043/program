# -*- coding: utf-8 -*-
# client3.py
# python3 client3.py HostName PortNumber

from socket import *
import time
import sys
import pbl2017

hostlist = ['pbl1','pbl2','pbl3','pbl4','pbl5']

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

def receive_data(client_socket):#データ受信関数,aの長さが0のとき終了
    response_server = bytearray()
    while True:
        a =  client_socket.recv(1)#1024バイトずつ
        if len(a)<=0 :
            break
        response_server.append(a[0])
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
  
def get_request_client(input_list,client_socket,token_str):#GETリクエスト
    getarg = pbl2017.genkey(token_str)#トークン文字列から生成したダイジェスト文字列を代入
    if (input_list[2] == 'ALL'):#ALL
        sentence = 'GET {} {} {}\n'.format(input_list[1],getarg,'ALL')#GET filename token ALL/PARTIAL sNUM gNUM
        print("[TO server]\n" + sentence)
        client_socket.send(sentence.encode())#サーバーへリクエスト
        res_str = receive_data2(client_socket)#サーバーからの応答を受信
        #res_str = client_socket.recv(1024).decode()
        #res_str = client_socket.recv(1024).decode()
        print('[FROM server]\n' + res_str)
        if(res_str.split()[0] == 'OK'):#OK
            ALL_file_data = receive_data(client_socket)#ファイルデータ受信
            f = open('filedata.dat','w')
            f.write(ALL_file_data)
            f.close()
            #print(ALL_file_data)
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
    
def main():#main
    if len(sys.argv) < 2:
        sys.exit('Usage: python3 client3.py HostName PortNumber')
    server_name = sys.argv[1]     #ホスト名
    server_port = int(sys.argv[2])#ポート番号
    #filename = sys.argv[3]       　#ファイル名
    token_str = "aaa"         #トークン文字列
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, server_port))  # サーバのソケットに接続する
    
    print('[書式]\nSIZE [filename]\nGET [filename] [ALL or PARTIAL] ([from]) ([to])\nREP [filename]\n>>>',end="") 
    input_sentence = input() #命令入力
    input_list = input_sentence.split()#命令分割
    
    if len(input_list)==0:#入力なしの場合->何もしない
        pass
    elif (input_list[0] == 'SIZE'):#SIZE要求
        size_request_client(input_list,client_socket)
    elif(input_list[0] == 'GET'):#GET要求
        if (len(input_list) > 2 ):
            get_request_client(input_list,client_socket,token_str)
        else:
            print('GETコマンドの引数が正しく入力されていません')
    elif(input_list[0] == 'REP'):#REP要求
        rep_request_client(input_list,client_socket,token_str)
    else:
        client_socket.send(input_sentence.encode())
        print(receive_data(client_socket),end="")
    
    client_socket.close()  
if __name__ == '__main__':
     main()