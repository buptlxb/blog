title: hihoCoder太阁最新面经算法竞赛4
category: C/CPP
tags: cpp, algorithm, hihocoder
date: 2016-06-15 19:58:47
keywords: algorithm, hihocoder, bittiger, 太阁最新面经算法竞赛
description: hihoCoder太阁最新面经算法竞赛4题解

> If all you have is a hammer, everything looks like a nail.  ---Maslow

## 树结构判定

### 问题

时间限制:10000ms
单点时限:1000ms
内存限制:256MB

#### 描述

给定一个包含 N 个顶点 M 条边的无向图 G ，判断 G 是不是一棵树。

#### 输入

第一个是一个整数 T ，代表测试数据的组数。 (1 ≤ T ≤ 10)

每组测试数据第一行包含两个整数 N 和 M 。(2 ≤ N ≤ 500, 1 ≤ M ≤ 100000)

以下 M 行每行包含两个整数 a 和 b ，表示顶点 a 和顶点 b 之间有一条边。(1 ≤ a, b ≤ N)

#### 输出

对于每组数据，输出YES或者NO表示 G 是否是一棵树。

样例输入

    :::
    2
    3 2
    3 1
    3 2
    5 5
    3 1
    3 2
    4 5
    1 2
    4 1 
样例输出

    :::
    YES
    NO

### 分析

感觉这应该是一类经典问题，但是对于我这种算法菜鸟来说每个问题是新的。

给定一个包含 N 个顶点 M 条边的无向图 G ，判断 G
是不是一棵树。题意很清楚，根据我并不扎实的基础知识，可以得到下列判定条件：

1. 图G需要是连通的。
2. 图G无环。

对于一个有N个顶点的树，容易知道其有N-1条边（因为将N个顶点连接起来，至少需要N-1条边，若存在更多的边，则会形成环）

因此，简单的，我们可以利用图的拓扑排序:
1. 若M不等于N-1，显然不是树；
2. 否则，若图中存在度为0的结点，说明图不是连通的，显然也不是树。
3. 将图中度为1的点去掉，更新这些结点连接的结点的度，并将度为1的结点放入队列。
4. 重复3，直到队列为空，比较去掉的结点数是否为N。

### AC程序

下面是C++实现的完整代码：

    :::C++

    #include <iostream>
    #include <vector>
    #include <set>
    #include <queue>

    using namespace std;

    bool solve(vector<set<int>> &graph, vector<int> &degree)
    {
        queue<int> q;
        for (vector<int>::size_type i = 0, iend = degree.size(); i < iend; ++i) {
            if (degree[i] == 0)
                return false;
            if (degree[i] == 1)
                q.push(i);
        }
        int cnt = 0;
        while (!q.empty()) {
            int cur = q.front();
            q.pop();
            ++cnt;
            for (auto p : graph[cur]) {
                if (--degree[p] == 1) {
                    q.push(p);
                }
            }
        }
        return cnt == degree.size();
    }

    int main(void)
    {
        ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int t;
        cin >> t;
        while (t--) {
            int n, m;
            cin >> n >> m;
            vector<set<int>> graph(n);
            vector<int> degree(n);
            for (int i = 0; i < m; ++i) {
                int a, b;
                cin >> a >> b;
                ++degree[a-1];
                ++degree[b-1];
                graph[b-1].insert(a-1);
                graph[a-1].insert(b-1);
            }
            if (n == m + 1 && solve(graph, degree))
                cout << "YES";
            else
                cout << "NO";
            cout << endl;
        }
        return 0;
    }


此外，还可以使用并查集来解决这一问题。

----

## 回文字符串

### 问题
时间限制:10000ms
单点时限:1000ms
内存限制:256MB
#### 描述
给定一个字符串 S ，最少需要几次增删改操作可以把 S 变成一个回文字符串？

一次操作可以在任意位置插入一个字符，或者删除任意一个字符，或者把任意一个字符修改成任意其他字符。

#### 输入
字符串 S。S 的长度不超过100, 只包含'A'-'Z'。

#### 输出
最少的修改次数。

样例输入

    :::
    ABAD

样例输出

    :::
    1

### 分析

1. 长度为0或1的字符串必然是回文字符串s，故需要的编辑次数f(s)=0
2. 长度为n(n > 1) 的字符串s:
    1. 若`s[0] == s[n-1]`，则 f(s) = f(s[1:n-1]);
    2. 否则，f(s) = min(f(s[1:n-1]), f(s[1:n]), f(s[0:n-1]))+1
       ，其中f(s[1:n-1])相当于将s[0]替换成s[n-1]；f(s[1:n])相当于删除s[0]; f(s[0:n-1])相当于删除s[n-1]。

有了这些就可以写程序了。

### AC程序

    :::C++
    #include <iostream>
    #include <vector>

    using namespace std;

    int palindromic_edit_distance(const string &s)
    {
        string::size_type len = s.size();
        vector<vector<int>> dp(len, vector<int>(len));
        for (string::size_type i = 0; i < len; ++i)
            dp[i][i] = 0;
        for (string::size_type i = 1; i < len; ++i) {
            for (string::size_type j = 0; i + j < len; ++j) {
                if (s[j] == s[j+i])
                    dp[j][j+i] = dp[j+1][j+i-1];
                else
                    dp[j][j+i] = min(dp[j+1][j+i-1], min(dp[j][j+i-1], dp[j+1][j+i])) + 1;
            }
        }
        return dp[0][len-1];
    }

    int main(void)
    {
        string s;
        cin >> s;
        cout << palindromic_edit_distance(s) << endl;
        return 0;
    }

----

## 希尔伯特曲线

### 问题

时间限制:10000ms
单点时限:1000ms
内存限制:256MB

#### 描述

希尔伯特曲线是以下一系列分形曲线 Hn 的极限。我们可以把 Hn 看作一条覆盖 2n × 2n 方格矩阵的曲线，曲线上一共有 2n × 2n
个顶点(包括左下角起点和右下角终点)，恰好覆盖每个方格一次。

![hilbert curve](/assets/images/hilbert-curve.png)

Hn(n > 1)可以通过如下方法构造：

1. 将 Hn-1 顺时针旋转90度放在左下角

2. 将 Hn-1 逆时针旋转90度放在右下角

3. 将2个 Hn-1 分别放在左上角和右上角

4. 用3条单位线段把4部分连接起来

对于 Hn 上每一个顶点 p ，我们定义 p 的坐标是它覆盖的小方格在矩阵中的坐标，定义 p
的序号是它在曲线上从起点开始数第几个顶点。给定 p 的坐标，你能算出 p 的序号吗？ 

#### 输入
输入包含3个整数 n , x , y 。 n 是分形曲线的阶数，(x, y)是 p 的坐标。

1 ≤ n ≤ 30

1 ≤ x, y ≤ 2n

#### 输出
p 的序号。

样例输入

    :::
    3 6 1

样例输出

    :::
    60

### 分析

根据题意的描述，可以看出希尔伯特曲线的构造是个递归的过程，而一阶的希尔伯特曲线，我们很容易根据给出的坐标，算出它的序号。
在进行递归时，只要小心计算坐标映射关系就好。

Hn(n > 1)可以通过如下方法构造(其中b表示n-1阶时正方形的边长)：

1. 将 Hn-1 顺时针旋转90度放在左下角: (x, y) => (y, x)

2. 将 Hn-1 逆时针旋转90度放在右下角: (x, y) => (b-y+1, 2b-x+1)

3. 将 Hn-1 放在左上角 : (x, y) => (x, y-b)

4. 将 Hn-1 放在右上角 : (x, y) => (x-b, y-b)

最后，需要注意的是要使用unsigned long long，因为30阶的希尔伯特曲线顶点数为2^60，使用64bit的数据类型刚好可以表示。

### AC程序

    :::C++
    #include <iostream>
    #include <vector>
    #include <cassert>

    using namespace std;

    unsigned long long hilbert(int n, int x, int y)
    {
        if (n == 1) {
            if (x == 1 && y == 1)
                return 1;
            if (x == 1 && y == 2)
                return 2;
            if (x == 2 && y == 2)
                return 3;
            if (x == 2 && y == 1)
                return 4;
        }
        unsigned long long b = 1ull << (n - 1);
        unsigned long long c = 1ull << (2*n-2);
        if (x <= b && y <= b)
            return hilbert(n-1, y, x);
        if (x <= b && y > b)
            return c + hilbert(n-1, x, y-b);
        if (x > b && y > b)
            return c * 2 + hilbert(n-1, x-b, y-b);
        if (x > b && y <= b)
            return c * 3 + hilbert(n-1, b-y+1, 2*b-x+1);
        assert(0);
    }

    int main(void)
    {
        int n, x, y;
        cin >> n >> x >> y;
        cout << hilbert(n, x, y) << endl;
        return 0;
    }


更多AC程序欢迎follow我的[github](https://github.com/buptlxb/hihoCoder)

（全文完）

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
