# -*- coding: utf-8 -*-
# Verify(Time Limit Exceeded)
# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=GRL_1_A&lang=jp
import networkx as nx
import matplotlib.pyplot as plt

INF = 1000000
g = nx.Graph()    # グラフオブジェクトの生成
# 標準入力から以下の形式で読み込む
# |V| |E|
# ai bi wi (辺ai->biのweightがwi)
V,E = map(int,raw_input().split())
edges = [[] for i in range(V)]    # 隣接リスト
edge_labels = {}    # 辺の描画用のラベル
for i in xrange(E):
    (a,b,w) = map(int,raw_input().split())
    g.add_edge(a,b,weight=w)
    edges[a].append({'to':b,'weight':w})
    edges[b].append({'to':a,'weight':w})
    edge_labels[(a,b)] = w

# Dijkstra from A(0)
distance = [INF] * V    # Aからの距離
visited = [False] * V    # 頂点が訪問済みかどうか
distance[0] = 0
for i in range(V):
    min_v = -1
    for v in range(V):
        # A(0)からの最短頂点を見つける (ヒープを使えば計算量を落とせる)
        if not visited[v] and (min_v == -1 or distance[v] < distance[min_v]):
            min_v = v
    # 訪問済みに
    visited[min_v] = True
    # 隣接してる頂点を更新
    for e in edges[min_v]:
        distance[e['to']] = min(distance[min_v] + e['weight'],distance[e['to']])
# 表示
print 'distance from A(0)'
for i in range(V):
    print '%2d: %d' % (i,distance[i])

# trace back from L(11) to A(0)
now = 11
path = [11]
while now != 0:
    for e in edges[now]:
        # labelを利用して経路復元 (頂点更新時に前の頂点を保存しておけば)
        if distance[now]-e['weight'] == distance[e['to']]:
            now = e['to']
            path.append(now)
            break
print 'trace back from L(11)'
print path

labels = {}    # ノードの描画用のラベル
s = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
for i in range(V):
    labels[i] = s[i] # distance[i]に変更すれば,ラベルがAからの最短経路長になる

# 適当に表示
pos = nx.spring_layout(g)
nx.draw_networkx_nodes(g,pos,nodelist=g.nodes(),node_size=600)
nx.draw_networkx_edges(g,pos,edgelist=g.edges())
nx.draw_networkx_labels(g,pos,labels,font_size=20)
nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels,font_size=12)

nx.draw_networkx_edges(g,pos,edgelist=[(path[i],path[i+1]) for i in range(len(path)-1)],width=5,edge_color='b')
nx.draw_networkx_nodes(g,pos,nodelist=path,node_size=600,node_color='b',alpha=0.8)

plt.axis('off')
plt.show()