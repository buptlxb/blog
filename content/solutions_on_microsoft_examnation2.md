title: 微软2016校园招聘4月在线笔试题解(二)
category: C/CPP
tags: cpp, algorithm, hihocoder
date: 2016-04-09 12:42:49

> If all you have is a hammer, everything looks like a nail.  ---Maslow

## B. 403 Forbidden

### Problem

时间限制:10000ms
单点时限:1000ms
内存限制:256MB

#### 描述
Little Hi runs a web server. Sometimes he has to deny access from a certain set of malicious IP addresses while his
friends are still allow to access his server. To do this he writes N rules in the configuration file which look like:

    :::
    allow 1.2.3.4/30
    deny 1.1.1.1
    allow 127.0.0.1
    allow 123.234.12.23/3
    deny 0.0.0.0/0

Each rule is in the form: **allow | deny address or allow | deny address/mask**.

When there comes a request, **the rules are checked in sequence until the first match is found**.
**If no rule is matched the request will be allowed**.
Rule and request are matched if the request address is the same as the rule address or they
share the same first mask digits when both written as 32bit binary number.

For example IP "1.2.3.4" matches rule "allow 1.2.3.4" because the addresses are the same. And IP "128.127.8.125" matches
rule "deny 128.127.4.100/20" because 10000000011111110000010001100100 (128.127.4.100 as binary number) shares the first
20 (mask) digits with 10000000011111110000100001111101 (128.127.8.125 as binary number).

Now comes M access requests. Given their IP addresses, your task is to find out which ones are allowed and which ones
are denied.

#### 输入
Line 1: two integers N and M.

Line 2-N+1: one rule on each line.

Line N+2-N+M+1: one IP address on each line.

All addresses are IPv4 addresses(0.0.0.0 - 255.255.255.255). 0 <= mask <= 32.


For 40% of the data: 1 <= N, M <= 1000.

For 100% of the data: 1 <= N, M <= 100000.

#### 输出
For each request output "YES" or "NO" according to whether it is allowed.

样例输入

    :::
    5 5
    allow 1.2.3.4/30
    deny 1.1.1.1
    allow 127.0.0.1
    allow 123.234.12.23/3
    deny 0.0.0.0/0
    1.2.3.4
    1.2.3.5
    1.1.1.1
    100.100.100.100
    219.142.53.100

样例输出

    :::
    YES
    YES
    NO
    YES
    NO

### Analysis

本题非常适合我这样的菜鸟：读完题目很容易有一个基本的思路，换句话说，这可以实现这个功能，但不保证性能。

#### Naive Approach

由题意直观的可以想到以下做法：

1. 设计一个类，描述配置规则；
2. 按读入顺序保存读入的所有规则；
3. 对于每一个待检验的IP，从头遍历规则，若匹配，返回规则的动作；否则，返回**允许**。

代码也很好写:

    :::C++
    #include <iostream>
    #include <vector>

    using namespace std;

    struct Rule {
        bool allow;
        unsigned int ip;
        int mask;
        Rule () : allow(false), ip(0), mask(32) {}
    };

    inline unsigned int getIp()
    {
        unsigned int a, b, c, d;
        char t;
        cin >> a >> t >> b >> t >> c >> t >> d;
        return (a << 24) | (b << 16) | (c << 8) | d;
    }

    bool solve(vector<Rule> &rules, unsigned int ip)
    {
        for (auto rule : rules) {
            if (rule.mask == 0 || (ip ^ rule.ip) >> (32-rule.mask) == 0)
                return rule.allow;
        }
        return true;
    }

    int main(void)
    {
        int n, m;
        cin >> n >> m;
        vector<Rule> rules(n);
        string cmd;
        char t;
        for (int i = 0; i < n; ++i) {
            cin >> cmd;
            rules[i].allow = cmd == "allow";
            rules[i].ip = getIp();
            cin >> t;
            if (t == '/')
                cin >> rules[i].mask;
            else
                cin.putback(t);
        }
        for (int i = 0; i < m; ++i) {
            unsigned int ip = getIp();
            cout << (solve(rules, ip) ? "YES" : "NO") << endl;
        }
        return 0;
    }


结果当然是TLE了，其实这种题对于搞过ACM的人来说应该是秒的吧，但是我完全不会什么线段树什么的。

仔细想想Naive Approach的问题，对于一个IP，每次检查的时候复杂度为O(n)，特别地，当这个IP没有任合匹配规则时，要尝试完所有的规则。
有什么办法可以准确的知道一个IP适用哪些规则呢？当然，所谓“适用”其实，题目说明的很清楚，即IP的`mask`长的前缀必须匹配。

前缀匹配问题，可以用前缀树来解决。因此，可以利用前缀树来确定哪些规则可以适用于一个IP。

#### Trie Approach

于是有了下面的想法：

1. 规则集利用前缀树描述
2. 前缀树每个结点记录，到本结点是否为一个规则，规则要求的动作是什么，规则的序号。
3. 对于一个IP，遍历前缀树，找到所适用规则中序号最小的，返回该规则的要求，若没有适用规则，返回允许。
4. 一个IPv4的地址大小为32bit，也就是可以在常量时间找到适用规则。

至此，剩下的问题就是如果建立前缀树，由于题意要求，最早匹配原则，树的建立可以这样做：

1. 若插入新规则i时，该规则的前缀路径上已有规则j, 则规则j的序号一定比i小，也即，规则i被j屏蔽，直接丢弃i即可。
2. 注意第一条中，当规则i和j等长时，也适用。

由此，当检查一个IP时，只需要返回这个IP适用的最长规则（为什么？上面的性质可以想一想）

有了这些结论，代码比较容易写出来了。

### Solution

下面是C++实现的完整代码：

    :::C++

    #include <iostream>
    #include <cassert>

    using namespace std;

    #define POOL_SIZE 3200005

    class Trie {
        struct TrieNode {
            int order;
            TrieNode *children[2];
            TrieNode() : order(0) {}
        };
        TrieNode *root, *pool;
        int num;
        TrieNode *getTrieNode() {
            assert(num < POOL_SIZE);
            return pool + num++;
        }
    public:
        Trie() : pool(new TrieNode[POOL_SIZE]), num(0) { root = getTrieNode(); }
        ~Trie() { delete[] pool; }
        void add(unsigned int ip, int mask, int order) {
            TrieNode *pos = root;
            for (int i = 0; i < mask; ++i) {
                if (pos->order)
                    return;
                int bit = (ip >> (31 - i)) & 1;
                if (!pos->children[bit])
                    pos->children[bit] = getTrieNode();
                pos = pos->children[bit];
            }
            if (!pos->order)
                pos->order = order;
        }
        int query(unsigned int ip) {
            TrieNode *pos = root;
            int order = 1;
            for (int i = 0; i < 32; ++i) {
                if (pos->order)
                    order = pos->order;
                int bit = (ip >> (31 - i)) & 1;
                if (!pos->children[bit])
                    break;
                pos = pos->children[bit];
            }
            return order;
        }
    };

    inline unsigned int getIp()
    {
        unsigned int a, b, c, d;
        char t;
        cin >> a >> t >> b >> t >> c >> t >> d;
        return (a << 24) | (b << 16) | (c << 8) | d;
    }

    int main(void)
    {
        int n, m;
        cin >> n >> m;
        Trie conf;
        string cmd;
        char t;
        for (int i = 1; i <= n; ++i) {
            cin >> cmd;
            unsigned int ip = getIp();
            int mask = 32;
            cin >> t;
            if (t == '/')
                cin >> mask;
            else
                cin.putback(t);
            int order = i;
            if (cmd != "allow")
                order *= -1;
            conf.add(ip, mask, order);
        }
        for (int i = 0; i < m; ++i) {
            unsigned int ip = getIp();
            cout << (conf.query(ip) < 0 ? "NO" : "YES") << endl;
        }
        return 0;
    }

### Complexity

* 时间复杂度：建前缀树O(n) 每一个IP检测O(1) 总体O(min(n, m))
* 空间复杂度：主要是缀树空间，树高32(33?)，至多m个叶子结点，每个叶子结点至多一个父结点。即O(m)

（全文完）

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
