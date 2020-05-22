import networkx as nx

def create_edges(file):
    # 创建有向边列表
    edges = []
    for line in file.readlines():
        if not line.startswith('#'):
            edges.append(line.rstrip('\n').split())
    return edges

# # 创建有向边列表
with open('web-Google.txt', 'r') as f:
    edges = create_edges(f)

def create_group(edges):
    # 创建有向图
    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    return G

# 创建有向图
G = create_group(edges)

def calculate_pangrank(G, tax):
    # 计算网页的pangrank值,tax为税值
    pr = nx.pagerank(G, alpha=tax)
    return pr

# 计算网页的pangrank值,tax为税值
pr = calculate_pangrank(G, 0.85)

def pr_descending_order(pr):
    # 转换成按pangrank值为key的降序列表
    pangrank_list = []
    descending_order_pangrank = []
    for webpage, pangrank in pr.items():
        pangrank_list.append([webpage, pangrank])

    descending_order_pangrank = sorted(pangrank_list, key=lambda x:x[1], reverse=True)
    return descending_order_pangrank

# 转换成按pangrank值为key的降序列表
descending_order_pangrank = pr_descending_order(pr)

# 查看前15行
print(descending_order_pangrank[0:15])