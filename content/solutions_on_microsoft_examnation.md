title: 微软2016校园招聘4月在线笔试题解(一)
category: C/CPP
tags: cpp, algorithm, hihocoder
date: 2016-04-09 00:33:07

> If all you have is a hammer, everything looks like a nail.  ---Maslow

## A. Font Size

### Problem

时间限制:10000ms
单点时限:1000ms
内存限制:256MB

#### 描述
Steven loves reading book on his phone. The book he reads now consists of N paragraphs and the i-th paragraph contains ai characters.


Steven wants to make the characters easier to read, so he decides to increase the font size of characters. But the size of Steven's phone screen is limited. Its width is W and height is H. As a result, if the font size of characters is S then it can only show ⌊W / S⌋ characters in a line and ⌊H / S⌋ lines in a page. (⌊x⌋ is the largest integer no more than x)  


So here's the question, if Steven wants to control the number of pages no more than P, what's the maximum font size he can set? Note that paragraphs must start in a new line and there is no empty line between paragraphs.

#### 输入
Input may contain multiple test cases.

The first line is an integer TASKS, representing the number of test cases.

For each test case, the first line contains four integers N, P, W and H, as described above.

The second line contains N integers a1, a2, ... aN, indicating the number of characters in each paragraph.


For all test cases,

1 <= N <= 103,

1 <= W, H, ai <= 103,

1 <= P <= 106,

There is always a way to control the number of pages no more than P.

#### 输出

样例输入
```
2
1 10 4 3
10
2 10 4 3
10 10
```
样例输出
```
3
2
```

### Analysis

本题相比简单，只是要注意一点，**每段要重新开始一行**，另注意到输入的范围也没有超过int32_t表示的范围。分析后容易得到以下结论：

1. 字母是方的，即宽高一样。
2. 每页至少要显示一个字母，才能有解。即字母大小`size = min(W, H)`。
3. 每行至多可以显示`row = W / size`个字母，注意下取整。
4. 一个段包含`p`个字母的段，至少需要占用`require = (p + row - 1) / row`行。 

有了这些结论，代码比较容易写出来了。

### Solution

下面是C++实现的完整代码：

    :::C++
    #include <iostream>
    #include <vector>

    using namespace std;

    int solve(int n, int p, int w, int h, vector<int> &paragraphs)
    {
        for (int i = min(w, h); i; --i) {
            int row = w / i;
            int col = h / i;
            int require = 0;
            for (auto p : paragraphs)
                require += (p + row - 1) / row;
            if (require <= p * col)
                return i;
        }   
        return 1;
    }

    int main(void)
    {
        int tasks;
        cin >> tasks;
        while (tasks-- > 0) {
            int n, p, w, h;
            cin >> n >> p >> w >> h;
            vector<int> paragraphs(n);
            for (int i = 0; i < n; ++i)
                cin >> paragraphs[i];
            cout << solve(n, p, w, h, paragraphs) << endl;
        }   
        return 0;
    }

### Complexity

* 时间复杂度：O(n*min(w, h))
* 空间复杂度：O(1) (不计算存储每段字母数量的空间)

（全文完）

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
