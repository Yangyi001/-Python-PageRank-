## 基于Python利用“抽税”法计算网页的PageRank排名

### 前言

搜索引擎的根本用途在于根据用户的查询，快速而准确地从网络的海洋中找到用户最需要的网页。这是针对网页的一类特殊的信息检索过程。它主要有以下两个特点：

- 搜索的数据量相当大
- 搜索的数据之间质量参差不齐

因此，基本的解决思路是根据查询，对这些网页进行排序，按照对用户搜索目的的判断，将最符合用户需求的网页依次排在最前面。也就是说，搜索引擎要解决的最主要问题是对网页排序模型的设计。
这就引出了一个问题：如何对互联网上“成万上亿”的网页进行排序？

一个直观可理解的排序思路就是：如果一个网页的链接被其他网页引用的次数很多，我们可以认为该网页是优质的。（优质网页访问的人比较多）PageRank计算网页排名就是基于此。

本篇讲解根据网页链接数据集“Web-google.txt”，利用“抽税”法计算网页的PageRank排名。“Web-google.txt”数据集中的数据每一行是一个网页以及其所链接的网页。  

### 原理分析及流程  
#### PageRank介绍
PageRank，网页排名，是一种根据网页之间相互的超链接计算的技术，可作为网页排名的要素之一，以Google公司创办人拉里·佩奇(Larry Page)的姓来命名。
Google把从A页面到B页面的链接解释为A页面给B页面投票，Google根据投票来源和目标的等级来决定网页的等级。

#### PageRank基本思想
PageRank的基本思想：被越多优质的网页所指的网页，它是优质的概率就越大。$$R(i)=\sum_{j \in B(i) }R(j)$$网页的PageRank越高，它就越“重要”。

假设有如下Web链接：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200522203935960.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjMwMjQ4Nw==,size_16,color_FFFFFF,t_70#pic_center)
随机冲浪者位置的概率分布可以通过 n 维列向量描述，第 j 个分量代表冲浪者处于网页 j 的概率。
上图对应的Web转移矩阵为：
$$
 \left[
 \begin{matrix}
   0 & 1/2 & 1 & 0\\
   1/3 & 0 & 0 & 1/2\\
   1/3 & 0 & 0 & 1/2\\
   1/3 & 1/2 & 0 & 0
  \end{matrix}
  \right]
$$
如上，第一列表示冲浪者处于网页A时，跳转到B、C、D的概论都是1/3。
假设n个网页的初始概率分布向量是一个每维均为1/n的n维向量$v_0$，Web转移矩阵为$M$，则第1步之后冲浪者的概率分布为$Mv_0$，第2步之后，冲浪者的概率分布为$M^2v_0$……第$i$步之后的位置概率分布向量为$M^iv_0$。
迭代50-75次后，上述分布已经收敛。
下面是上诉所示的四个网页前四次跳转的PageRank值：
$$
  \begin{matrix}
 \left[
 \begin{matrix}
   1/4 \\
   1/4 \\
   1/4 \\
   1/4 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   9/24 \\
   5/24 \\
   5/24 \\
   5/24 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   15/48 \\
   11/48 \\
   11/48 \\
   11/48 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   11/32 \\
   7/32 \\
   7/32 \\
   7/32 
  \end{matrix}
  \right]
\dots
 \left[
 \begin{matrix}
   3/9 \\
   2/9 \\
   2/9 \\
   2/9 
  \end{matrix}
  \right]
  \end{matrix}
$$
网页A的PageRank值最大，为3/9，说明停留在网页A上的概率相对于网页B、C、D来说较大，该网页也较为重要。

#### 终止点问题
一个没有出链的网页称为终止点。例如去掉上例中的C到A的边。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200522204723659.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjMwMjQ4Nw==,size_16,color_FFFFFF,t_70#pic_center)
现在的Web转移矩阵为：
$$
 \left[
 \begin{matrix}
   0 & 1/2 & 0 & 0\\
   1/3 & 0 & 0 & 1/2\\
   1/3 & 0 & 0 & 1/2\\
   1/3 & 1/2 & 0 & 0
  \end{matrix}
  \right]
$$
由于矩阵M的第三列全部为0，最后任何网页出现的概率都为0：
$$
  \begin{matrix}
 \left[
 \begin{matrix}
   1/4 \\
   1/4 \\
   1/4 \\
   1/4 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   3/24 \\
   5/24 \\
   5/24 \\
   5/24 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   5/48 \\
   7/48 \\
   7/48 \\
   7/48 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   21/288 \\
   31/288 \\
   31/288 \\
   31/288 
  \end{matrix}
  \right]
\dots
 \left[
 \begin{matrix}
   0 \\
   0 \\
   0 \\
   0 
  \end{matrix}
  \right]
  \end{matrix}
$$
#### 采集器陷阱
采集器陷阱指没有出链指向该集合之外的其它节点的节点机和。它将导致PageRank值都分配给采集器陷阱以内的节点。
下面给出一个采集器陷阱的例子：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200522205452808.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjMwMjQ4Nw==,size_16,color_FFFFFF,t_70#pic_center)
如上，C的出链改成指向自己的链接，其构成的单节点采集器陷阱，上图对应的转移矩阵如下：
$$
 \left[
 \begin{matrix}
   0 & 1/2 & 0 & 0\\
   1/3 & 0 & 0 & 1/2\\
   1/3 & 0 & 1 & 1/2\\
   1/3 & 1/2 & 0 & 0
  \end{matrix}
  \right]
$$
随着迭代的进行，C的PageRank值不断趋近于1，其他非采集器陷阱内节点的PageRank值趋向于0：
$$
  \begin{matrix}
 \left[
 \begin{matrix}
   1/4 \\
   1/4 \\
   1/4 \\
   1/4 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   3/24 \\
   5/24 \\
   11/24 \\
   5/24 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   5/48 \\
   7/48 \\
   29/48 \\
   7/48 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   21/288 \\
   31/288 \\
   205/288 \\
   31/288 
  \end{matrix}
  \right]
\dots
 \left[
 \begin{matrix}
   0 \\
   0 \\
   1 \\
   0 
  \end{matrix}
  \right]
  \end{matrix}
$$
#### 解决方法
出现以上这两个致命的问题的原因是：用户的上网模型是不够准确的。
用户不是傻乎乎的机器，当一个人遇到终止点或者陷阱的话，他不会不知所错，也不会无休止地自己打转，他会通过浏览器的地址栏输入新的地址，以逃离这个网页。
也就是说，用户从一个网页转至另一个网页的过程中，会以一定的概率不点击当前网页中的链接，而是访问一个自己重新输入的新地址。

所以对于以上两个问题，解决的方法之一是给每个节点以一个较小的随机概率跳转到另一个网页，即更改PageRank估计值$v$为$v^{'}$，其迭代公式为：
$$v^{'}=\beta Mv+(1-\beta)e/n$$$(1-\beta)e/n$代表一个节点以$(1-\beta)$的概率随机选择另一个网页进行访问。
取 $\beta = 0.8$，则上述采集器陷阱的迭代公式更改为：
$$
\begin{matrix}
v^{'}=
 \left[
 \begin{matrix}
   0 & 2/5 & 0 & 0\\
   4/15 & 0 & 0 & 2/5\\
   4/15 & 0 & 4/5 & 2/5\\
   4/15 & 2/5 & 0 & 0
  \end{matrix}
  \right]
·v+
 \left[
 \begin{matrix}
   1/20 \\
   1/20 \\
   1/20 \\
   1/20 
  \end{matrix}
  \right]
  \end{matrix}
$$
下面是前几轮迭代的结果：
$$
  \begin{matrix}
 \left[
 \begin{matrix}
   1/4 \\
   1/4 \\
   1/4 \\
   1/4 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   9/60 \\
   13/60 \\
   25/60 \\
   13/60 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   41/300 \\
   53/300 \\
   153/300 \\
   53/300 
  \end{matrix}
  \right]
 \left[
 \begin{matrix}
   543/4500 \\
   707/4500 \\
   2543/4500 \\
   707/4500 
  \end{matrix}
  \right]
\dots
 \left[
 \begin{matrix}
   15/148 \\
   19/148 \\
   95/148 \\
   19/148 
  \end{matrix}
  \right]
  \end{matrix}
$$
作为一个陷阱，C获得了超过一半以上的PageRank值。但是这种效果受到了限制，其它节点也获得了一些PageRank值。所以抽税法能在一定程度上解决采集器陷阱问题。（也可在一定程度上解决终结点问题，此处不做演示）

### 实现流程
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200522210958360.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjMwMjQ4Nw==,size_16,color_FFFFFF,t_70#pic_center)

### 具体实现
导入所需要的包
```
import networkx as nx
```
读入数据并查看前10行
```
In [4]: f = open('web-Google.txt', 'r')

In [5]: for i in range(10):
   ...:     print(f.readline())
   ...:
# Directed graph (each unordered pair of nodes is saved once): web-Google.txt

# Webgraph from the Google programming contest, 2002

# Nodes: 875713 Edges: 5105039

# FromNodeId    ToNodeId

0       11342

0       824020

0       867923

0       891835

11342   0

11342   27469
```
如上输出所示，每一行左边数字表示当前页面，右边为当前页面所指向的页面。
接下来按以上实现流程图，对网页按PageRank值进行排名。
*注：所用到的函数是作者自己封装好的，完整代码文末有给出链接*
```
# 创建有向边
with open('web-Google.txt', 'r') as f:
    edges = create_edges(f)

# 创建有向图
G = create_group(edges)

# 计算网页的pangrank值,tax为税值
# 此处抽税0.15，即认为用户有15%的几率手动输入网址打开新的网页
pr = calculate_pangrank(G, 0.85)

# 转换成按pangrank值为key的降序列表
descending_order_pangrank = pr_descending_order(pr)
```
至此我们得到了网页编号按pangrank值为key的降序列表。查看其前15行数据如下：
```
In [9]: descending_order_pangrank[0:15]
Out[9]:
[['163075', 0.0009521123333766921],
 ['597621', 0.0009013686628239589],
 ['537039', 0.0008953815726589951],
 ['837478', 0.0008761661604312313],
 ['885605', 0.0008216087428295045],
 ['551829', 0.0007901082073484857],
 ['41909', 0.0007794946931031557],
 ['605856', 0.0007791356753662065],
 ['504140', 0.0007457503352830772],
 ['819223', 0.0007101828701989993],
 ['751384', 0.0006933386664532035],
 ['908351', 0.0006924356717897781],
 ['32163', 0.0006911621448826768],
 ['558791', 0.0006804667815363988],
 ['407610', 0.0006720415070519903]]
```
如上所示，计算出了网页的pangrank值，并降序排列输出。

### 总结
PageRank，网页排名，是一种根据网页之间相互的超链接计算的技术，可作为网页排名的要素之一，基于对网页的PageRank值的计算比较，我们可以向用户推荐更加优质的网页，而不是让用户把大量时间浪费在对信息的过滤上。    

当然，PageRank也有许多弊端，此处不做介绍，有兴趣的读者可以查阅相关资料深入了解。  

#### 附录
*数据集：Web-google.txt 及完整代码已放置于：[Github](https://github.com/Yangyi001/-Python-PageRank-.git)*