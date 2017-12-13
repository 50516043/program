# -*- coding: utf-8 -*-
# tcp_client.py for Python 3

# socketモジュールから全てのシンボルをインポートする
#  この結果、とくにモジュール名を書かなくてもsocketモジュール内の
#  クラスや関数などにアクセスできる
from socket import *  


server_name = 'localhost'  # サーバのホスト名あるいはIPアドレスを表す文字列
server_port = 50000  # サーバのポート
client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
client_socket.connect((server_name, server_port))  # サーバのソケットに接続する
sentence = input('Input lowercase sentence: ')   # キーボードから入力された文字列を受け取る
client_socket.send(sentence.encode())  # 文字列をバイト配列に変換後、送信する。
modified_sentence = client_socket.recv(1024)  # 最大1024バイトを受け取る。受け取った内容はバイト配列として格納される。
print('From Server: {0}'.format(modified_sentence.decode()))  # バイト配列を文字列に変換して表示する
client_socket.close()  # ソケットを閉じる