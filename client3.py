# -*- coding: utf-8 -*-
# client3.py
# python3 client3.py localhost 54301 
#

from socket import *
import time
import sys
import pbl2017

def receive_data(client_socket):#データ受信関数
  response_server = bytearray()#配列
  while True:
    a =  client_socket.recv(1)
    if len(a)<=0:
      break
    response_server.append(a[0])

  receive_str = response_server.decode()
  return receive_str

def size_request_client(input_list,client_socket):
  try:
    filename = input_list[1]
  except:
    print("ファイル名が入力されていません")
    sys.exit()
  sentence = '{} {} \n'.format("SIZE",filename)
  client_socket.send(sentence.encode())
  res_str = receive_data(client_socket)#データを受信
  print(res_str)
  
def get_request_client(input_list,client_socket,token_str):
  getarg = pbl2017.genkey(token_str)
  if (input_list[2] == 'ALL'):
    sentence = 'GET {} {} {}'.format(input_list[1],getarg,'ALL')
    client_socket.send(sentence.encode())
    res_str = receive_data(client_socket)#データを受信
    #print(res_str + '(from server)')
    if(res_str.split()[0] == 'OK'):
      ALL_file_data = receive_data(client_socket)
      
      f = open('filedata.dat','w')
      f.write(ALL_file_data)
      f.close()
      print(res_str)
    elif(res_str.split()[0] == 'NG'):
      print(res_str)
  
  elif (input_list[2] == 'PARTIAL'):
    sentence = 'GET {0} {1} PARTIAL {2} {3}'.format(input_list[1],getarg,input_list[3],input_list[4])
    client_socket.send(sentence.encode())
    res_str = receive_data(client_socket)#データを受信
    if(res_str.split()[0] == 'OK'):
      PARTIAL_file_data = receive_data(client_socket)
      #print(PARTIAL_file_data)
      print(res_str)
    elif(res_str.split()[0] == 'NG'):
      print(res_str)
def rep_request_client(input_list,client_socket,token_str):  
  sentence = 'REP {} {} {}'.format(input_list[1],token_str,pbl2017.repkey(token_str,'filedata.dat'))
  client_socket.send(sentence.encode())
  res_str = receive_data(client_socket)#データを受信
  #if(res_str.split()[0] == 'OK'):
  print(res_str)
  
  
def main():
  server_name = sys.argv[1]
  server_port = int(sys.argv[2])
  #filename = sys.argv[3]
  token_str = "abcdeaaaaa"  #トークン
  client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
  client_socket.connect((server_name, server_port))  # サーバのソケットに接続する
  
  print('[書式]\nSIZE [filename]\nGET [filename] [ALL or PARTIAL] ([from]) ([to])\nREP [filename]\n>>>',end="") 
  input_sentence = input() #入力
  input_list = input_sentence.split()
  if len(input_list)==0:
    pass
  elif (input_list[0] == 'SIZE'):
    size_request_client(input_list,client_socket)#SIZE要求
  elif(input_list[0] == 'GET'):
    if (len(input_list) > 2 ):
      get_request_client(input_list,client_socket,token_str)#GET要求
    else:
       print('GETコマンドの引数が正しく入力されていません')
  elif(input_list[0] == 'REP'):
    rep_request_client(input_list,client_socket,token_str)#REP要求
  else:
    client_socket.send(input_sentence.encode())
    print(receive_data(client_socket),end="")
    
  client_socket.close()  
if __name__ == '__main__':
    main()

