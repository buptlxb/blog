title: [Offer收割]编程练习赛4题解
category: C/CPP
tags: cpp, algorithm, hihocoder, spfa
date: 2016-08-08 20:19:32 
keywords: algorithm, hihocoder, spfa
description: [Offer收割]编程练习赛4题解

> If all you have is a hammer, everything looks like a nail.  ---Maslow

## A.满减优惠

### 问题

时间限制:10000ms
单点时限:1000ms
内存限制:256MB

#### 描述

最近天气炎热，小Ho天天宅在家里叫外卖。他常吃的一家餐馆一共有N道菜品，价格分别是A1, A2, ... AN元。并且如果消费总计满X元，还能享受优惠。小Ho是一个不薅羊毛不舒服斯基的人，他希望选择若干道不同的菜品，使得总价在不低于X元的同时尽量低。

你能算出这一餐小Ho最少消费多少元吗？

#### 输入

第一行包含两个整数N和X，(1 &lt;= N &lt;= 20, 1 &lt;= X &lt;= 100)

第二行包含N个整数A1, A2, ...， AN。(1 &lt;= Ai &lt;= 100)

#### 输出
输出最少的消费。如果小Ho把N道菜都买了还不能达到X元的优惠标准，输出-1。

样例输入

    :::
    10 50
    9 9 9 9 9 9 9 9 9 8

样例输出

    :::
    53

### 分析

题目简单理解起来就是，从数组中选出若干个数，使得这些数的和大于X，并且尽可能的小。

根据数据范围的限制，数组中最多只有20个数，所有这些和的数量为1^20个。数据量并不大。

暴力应该可以搞定：枚举数的所有数的组合情况，使用int32_t表示每个数的选择情况，int32_t的第i位表示数组中下标为i的数是否选中。

### AC程序

下面是C++实现的完整代码：

    :::C++
    #include <iostream>
    #include <vector>

    using namespace std;

    int main(void)
    {
        int n, x, sum = 0;
        cin >> n >> x;
        vector<int> nums(n);
        for (int i = 0; i < n; ++i) {
            cin >> nums[i];
            sum += nums[i];
        }
        if (sum < x) {
            cout << -1 << endl;
            return 0;
        }

        int ret = sum;
        for (int i = 1, iend = 1 << n; i < iend; ++i) {
            if (ret == x)
                break;
            int cur = 0;
            for (int j = 0; j < n; ++j) {
                if (((1 << j) & i)) // select jth number from nums
                    cur += nums[j];
                if (cur >= x) { // because there is no negative number in nums
                    break;
                }
            }
            // update minimum value greater than x
            if (cur >= x && cur < ret)
                ret = cur;
        }
        cout << ret << endl;
        return 0;
    }

----

## B. 积水的城市

### 问题

时间限制:11000ms
单点时限:1000ms
内存限制:256MB

#### 描述

如下图所示，某市市区由M条南北向的大街和N条东西向的道路组成。其中由北向南第i条路和第i+1条路之间的距离是Bi (1 &lt;= i &lht; N)，由西向东第i条街和第i+1条街之间的距离是Ai (1 &lt;= i &lt; M)。

![drown](/assets/images/drown.png)

小Ho现在位于第x条路和第y条街的交叉口，他的目的地是第p条路和第q条街的交叉口。由于连日降雨，城市中有K个交叉口积水太深不能通行。小Ho想知道到达目的地的最短路径的长度是多少。

#### 输入
第一行包含两个整数N和M。(1 &lt;= N, M &lt;= 500)  

第二行包含N-1个整数, B1, B2, B3, ... BN-1。(1 &lt;= Bi &lt;= 100)  

第三行包含M-1个整数, A1, A2, A3, ... AM-1。(1 &lt;= Ai &lt;= 100)  

第四行包含一个整数K，表示积水的交叉口的数目。 (0 &lt;= K &lt;= 30)  

以下K行每行包含2个整数，X和Y，表示第X条路和第Y条街的交叉口积水。(1 &lt;= X &lt;= N, 1 &lt;= Y &lt;= M)  

第K+5行包含一个整数Q，表示询问的数目。 (1 &lt;= Q &lt;= 10)  

以下Q行每行包含4个整数x, y, p, q，表示小Ho的起止点。起止点保证不在积水的交叉口处。  (1 &lt;= x, p &lt;= N, 1 &lt;= y, q &lt;= M)

#### 输出
对于每组询问，输出最短路的长度。如果小Ho不能到达目的地，输出-1。

样例输入

    :::
    4 5  
    2 4 1  
    3 3 3 2  
    3  
    1 3  
    2 3  
    3 2  
    1  
    1 2 2 4  

样例输出

    :::
    24

### 分析

有障碍的最短路径问题，对于无权的格子问题，只需要利用BFS探索即可。本题中“路”和“街”的长度可能不同，因此，利用SPFA算法。
也就是在BFS的基础上，记录源点到其它每个点的距离，当新探索出的路径长度更小时，更新记录，并将当前状态入栈。
当遇到“积水”的路口时，直接丢弃该状态即可表示不能通过本路口。

### AC程序

    :::C++
    #include <iostream>
    #include <cstring>
    #include <set>
    #include <queue>
    #include <utility>
    
    #define N 501
    #define M 501
    #define UDF 0x3f3f3f3f
    
    using namespace std;
    
    int A[M];
    int B[N];
    int n, m;
    set<pair<int, int>> dead;
    
    struct Status{
        int x, y, d;
        Status(int a, int b, int c) : x(a), y(b), d(c) {}
    };
    
    int visit[N][M];
    
    int solve(int x, int y, int p, int q)
    {
        static int dx[] = {-1, 0, 1, 0};
        static int dy[] = {0, 1, 0, -1};
    
        queue<Status> sq;
        sq.push(Status(x, y, 0));
        visit[x][y] = 0;
        while (!sq.empty()) {
            int cx = sq.front().x;
            int cy = sq.front().y;
            int cd = sq.front().d;
            sq.pop();
            // explore 4 directions
            for (int i = 0; i < 4; ++i) {
                int nx = cx + dx[i];
                int ny = cy + dy[i];
                // skip invalid coordinates and water crossing
                if (nx <= 0 || ny <= 0 || nx > n || ny > m || dead.find(make_pair(nx, ny)) != dead.end())
                    continue;
                int nd = dx[i] == 0 ? cd + A[min(cy, ny)] : cd + B[min(cx, nx)];
                // skip longer path
                if (visit[nx][ny] <= nd)
                    continue;
                // skip the destination itself
                if (nx != p || ny != q)
                    sq.push(Status(nx, ny, nd));
                visit[nx][ny] = nd;
            }
        }
        return visit[p][q] == UDF ? -1 : visit[p][q];
    }

    int main(void)
    {
        cin >> n >> m;
        for (int i = 1; i < n; ++i)
            cin >> B[i];
        for (int i = 1; i < m; ++i)
            cin >> A[i];
        int k;
        cin >> k;
        for (int i = 0; i < k; ++i) {
            int x, y;
            cin >> x >> y;
            dead.insert(make_pair(x, y));
        }
        int t;
        cin >> t;
        for (int i = 0; i < t; ++i) {
            int x, y, p, q;
            cin >> x >> y >> p >> q;
            memset(visit, UDF, sizeof(visit));
            cout << solve(x, y, p, q) << endl;
        }
        return 0;
    }

----

## C. 罚抄一百遍

### 问题

时间限制:10000ms
单点时限:1000ms
内存限制:256MB

#### 描述

小Ho忘了做英语作业，被老师罚抄某段文本N遍。抄写用的作业纸每行包含M个格子，每个格子恰好能填写一个字符或者空格。抄写过程中单词不能跨行，如果某行剩余的格子不足以写完一个单词，那么这个单词需要写在下一行。单词间的空格不能省略。

例如在M=9的作业纸上写2遍"Good good study day day up"：

    :::
    123456789
    Good good
    study   
    day day   
    up Good  
    good     
    study day
    day up  

小Ho想知道当他抄写完N遍以后，最后一个字符在第几行、第几列。

#### 输入
第一行包含两个整数N和M。  

第二行包含要抄写的文本。文本只包含大小字母和空格，并且单词之间只有一个空格。

对于40%的数据，1 <= N, M <= 1000  

对于100%的数据，1 <= N, M <= 1000000000, M >= 文本中最长的单词的长度，文本长度不超过100个字符。

#### 输出
最后一个字符的行号和列号。

样例输入

    :::
    2 9
    Good good study day day up

样例输出

    :::
    7 7

### 分析

根据题意的描述，可知当抄写的次数足够多时，必须存在循环节，也就是当抄写次数足够多时，必然存在i,
j，使得第i次抄写和第j次抄写开始的列数相同。寻找循环节的方法也很简单，只需要用Hash表记录，每次抄写时开始的行数x,列数y即可。

由于题目要求每两个单词之间必须存在一个空格，第二遍抄写的第一个单词与第一遍的最后一个单词之间，也要存在一个空格。
所以我们可以把要抄写的字符串前加上一个空格，以方便处理。那么此时，第一遍抄写时开始的行x=1，列y=-1。

当我们利用Hash表找到循环节后，即可以跳过中间重复的模拟过程。

此外，要小心行数x溢出int32_t表示范围。

### AC程序

    :::C++
    
    #include <iostream>
    #include <unordered_map>
    #include <vector>
    
    using namespace std;
    
    // copy n times starting at (x, y)
    void ncopy(const vector<int> &nums, int n, int m, long long &x, int &y)
    {
        for (int i = 0; i < n; ++i) {
            for (auto num : nums) {
                if (y == m)
                    y = 0, ++x;
                ++y;
                if (y + num > m)
                    y = 0, ++x;
                y += num;
            }
        }
    }
    
    int main(void)
    {
        int n, m;
        cin >> n >> m;
        vector<int> nums;
        string s;
        while(cin >> s)
            nums.push_back(s.size());
    
        // record nth copy starting at (x, y) => dict[y] = make_pair(n, x)
        unordered_map<int, pair<int, long long>> dict;
        long long x = 1;
        int y = -1;
        for (int i = 1; i <= n; ++i) {
            ncopy(nums, 1, m, x, y);
            if (dict.find(y) != dict.end()) { // find the repetend
                // fast forward to skip the repetend
                long long remain = (n - i) % (i - dict[y].first); 
                // add x by repetend's rows
                x += (n - i) / (i - dict[y].first) * (x - dict[y].second);
                // copy the reset times
                ncopy(nums, remain, m, x, y);
                break;
            }
            // record ith copy starting at (x, y)
            dict.emplace(y, make_pair(i, x));
        }
    
        cout << x << ' ' << y << endl;
        return 0;
    }

----

## D. 分隔相同整数

### 问题

时间限制:10000ms
单点时限:1000ms
内存限制:256MB

#### 描述
给定一个包含N个整数的数组A。你的任务是将A重新排列，使得任意两个相等的整数在数组中都不相邻。  

如果存在多个重排后的数组满足条件，输出字典序最小的数组。  

这里字典序最小指：首先尽量使第一个整数最小，其次使第二个整数最小，以此类推。

#### 输入
第一行包含一个整数N，表示数组的长度。(1 <= N <= 100000)  

第二行包含N个整数，依次是 A1, A2, ... AN。(1 <= Ai <= 1000000000)

#### 输出
输出字典序最小的重排数组。如果这样的数组不存在，输出-1。

样例输入

    :::
    4  
    2 1 3 3

样例输出

    :::
    1 3 2 3

### 分析

将一个由长度为n(n>1)同一字母组成的字符串分隔开，显然需要n-1个其它字符。
由此，我们可以统计，输入字符串的每个数字出现的次数Bi，我们可以按照如下规则排列数字：

1. 若出现最多的数字x的次数为Bx，则分隔x至少需要Bx-1个数字，若Bx + Bx - 1 <
   N，说明还有充足的字符可以分隔x，故输出与前次输出不同的最小数字即可;
2. 否则，说明此时必须输出x，因为，分隔x的字符即将不足。此时，若x与前次输出数字相同，则无解。

因此，我们可以利用Hash表，统计各数字出现的次数，将利用二叉查找树，得到次数最多的数字。
此处，不使用大根堆的原因是，当输出的数字不是次数最多的数字，即输出的数字不是大根堆的堆顶元素，
此时，更新相应元素的次数后，需要调整堆，以满足大根堆的性质，这个操作比较麻烦。

### AC程序

    :::C++

    #include <iostream>
    #include <algorithm>
    #include <map>
    #include <set>
    #include <vector>
    #include <queue>
    #include <cassert>
    
    using namespace std;
    
    bool solve(vector<int> &s)
    {
        map<int, int> dict;
        // count every number's times
        for (auto c : s)
            ++dict[c];
        set<pair<int, int>> heap;
        // use black-red tree simulate heap
        for (auto d : dict)
            heap.insert(make_pair(d.second, d.first));
        vector<int>::size_type size = s.size(), idx = 0;
        int last = -1;
        while (size) {
            auto iter = dict.find(heap.rbegin()->second);
            if (size/2 < iter->second) { // rule 2
                if (last == iter->first) // fail to rearrange
                    return false;
            } else { // rule 1
                iter = dict.begin();
                if (iter->first == last)
                    ++iter;
                assert(iter != dict.end());
            }
            // output a number
            s[idx++] = iter->first;
            // update heap
            heap.erase(make_pair(iter->second, iter->first));
            iter->second -= 1;
            if (iter->second == 0)
                dict.erase(iter);
            else
                heap.insert(make_pair(iter->second, iter->first));
            last = s[idx-1];
            --size;
        }
        return true;
    }
    
    int main(void)
    {
        int n;
        cin >> n;
        vector<int> nums(n);
        for (int i = 0; i < n; ++i)
            cin >> nums[i];
        if (!solve(nums))
            cout << -1 << endl;
        else {
            cout << nums[0];
            for (int i = 1; i < n; ++i)
                cout << ' ' << nums[i];
            cout << endl;
        }
        return 0;
    }
    

更多AC程序欢迎follow我的[github](https://github.com/buptlxb/hihoCoder)

（全文完）

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
