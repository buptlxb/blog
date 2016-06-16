title: 线段树
category: C/CPP
tags: cpp, algorithm, segment tree
date: 2016-05-13 21:27:07
keywords: segment tree, 线段树
descriptions: 线段树的简单介绍


> One thing I know is that I know nothing. ---Socrates

## What is that?

线段树是一种二叉搜索树，它的每一个节点表示一段区间，节点[a, b]的左子树表示的区间是[a, (a+b)/2]，而其右节点表示的区间为[(a+b)/2+1, b]。利用数组可以很好的表示一棵线段树，对于表示区间[1, n]的线段树所需要的数组大小大概为**4n**。

## Why should I care?

线段树对于解决一些区间更新、查询的问题非常有效。

通常情况下，其具有O(logn)的更新和查询时间复杂度。
线段树可以解决RMQ（Range Maximum/Minimum
Query）问题，对于一些只关心区间的相交覆盖问题，还可以使用离散化的技巧缩小区间大小。

## What should I do about it?

下面是一个常用的线段树模版：

    :::C++
    class SegmentTree {
        int size;
        vector<int> tree;
        void update(int index, int val, int root, int left, int right);
        int query(int first, int last, int root, int left, int right);
    public:
        int lson(int idx) { return idx << 1; }
        int rson(int idx) { return (idx << 1) | 1; }
        explicit SegmentTree(int n) : size(n), tree(n*4) {}
        explicit SegmentTree(vector<int> & v) : size(v.size()), tree(v.size()*4) {
            for (int i = 0, iend = v.size(); i < iend; ++i)
                update(i, v[i]);
        }
        void update(int index, int val) {
            update(index, val, 1, 0, size-1);
        }
        int query(int first, int last) {
            return query(first, last, 1, 0, size-1);
        }
        friend ostream & operator<< (ostream &os, const SegmentTree &st);
    };

    void SegmentTree::update(int index, int val, int root, int left, int right)
    {
        if (left == right)
            tree[root] = val;
        else {
            int mid = left + (right-left)/2;
            if (index <= mid)
                update(index, val, lson(root), left, mid);
            else
                update(index, val, rson(root), mid+1, right);
            tree[root] = min(tree[lson(root)], tree[rson(root)]);
        }
    }

    int SegmentTree::query(int first, int last, int root, int left, int right) {
        if (first == left && last == right)
            return tree[root];
        int mid = left + (right-left)/2;
        if (last <= mid)
            return query(first, last, lson(root), left, mid);
        if (first > mid)
            return query(first, last, rson(root), mid+1, right);
        return min(query(first, mid, lson(root), left, mid), query(mid+1, last, rson(root), mid+1, right));
    }

    ostream & operator<< (ostream &os, const SegmentTree &st) {
        for (auto x : st.tree)
            os << x << " ";
        return os;
    }


对于区间更新有时可以设置lazy tag来延迟更新，从而提高更新速度。

下面是一些常见的线段树问题：

| # | Problem | Solution |
|---|---------|----------|
|1|[RMQ问题再临-线段树](http://hihocoder.com/problemset/problem/1077)|[1077](https://github.com/buptlxb/hihoCoder/tree/master/solutions/1077)| 
|2|[线段树的区间修改](http://hihocoder.com/problemset/problem/1078)|[1078](https://github.com/buptlxb/hihoCoder/tree/master/solutions/1078)| 
|3|[离散化](http://hihocoder.com/problemset/problem/1079)|[1079](https://github.com/buptlxb/hihoCoder/tree/master/solutions/1079)| 
|4|[更为复杂的买卖房屋姿势](http://hihocoder.com/problemset/problem/1080)|[1080](https://github.com/buptlxb/hihoCoder/tree/master/solutions/1080)| 
|5|[计算](http://hihocoder.com/problemset/problem/1116)|[1116](https://github.com/buptlxb/hihoCoder/tree/master/solutions/1116)| 


    线段树的核心问题是如何设计树中的节点，当更新时，可以快速的通过子区间的某些运算，得到父节点的新值，这就是常说的PushUp操作。
    另一方面，在使用Lazy tag时，在查询时，需要根据父节点的Lazy tag更新子区间，这就是常说的PushDown操作。
    一些复杂的情况下，这PushUp和PushDown是较难设计的，所以也是关键所在。

（全文完）

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
