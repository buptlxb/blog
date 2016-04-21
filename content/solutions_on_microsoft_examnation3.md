title: 微软2016校园招聘4月在线笔试题解(三)
category: C/CPP
tags: cpp, algorithm, hihocoder
date: 2016-04-09 14:20:51

> If all you have is a hammer, everything looks like a nail.  ---Maslow

## C. Demo Day

### Problem

时间限制:10000ms
单点时限:1000ms
内存限制:256MB

#### 描述

You work as an intern at a robotics startup. Today is your company's demo day. During the demo your company's robot will be put in a maze and without any information about the maze, it should be able to find a way out.

The maze consists of N * M grids. Each grid is either empty(represented by '.') or blocked by an obstacle(represented by 'b'). The robot will be release at the top left corner and the exit is at the bottom right corner.

Unfortunately some sensors on the robot go crazy just before the demo starts. As a result, the robot can only repeats two operations alternatively: keep moving to the right until it can't and keep moving to the bottom until it can't. At the beginning, the robot keeps moving to the right.

    :::
    rrrrbb..            
    ...r....     ====> The robot route with broken sensors is marked by 'r'. 
    ...rrb..
    ...bb...

While the FTEs(full-time employees) are busy working on the sensors, you try to save the demo day by rearranging the maze in such a way that even with the broken sensors the robot can reach the exit successfully. You can change a grid from empty to blocked and vice versa. So as not to arouse suspision, you want to change as few grids as possible. What is the mininum number?

#### 输入
Line 1: N, M.

Line 2-N+1: the N * M maze.



For 20% of the data, N * M <= 16.

For 50% of the data, 1 <= N, M <= 8.

For 100% of the data, 1<= N, M <= 100.

#### 输出
The minimum number of grids to be changed.

样例输入

    :::
    4 8
    ....bb..
    ........
    .....b..
    ...bb...

样例输出

    :::
    1

### Analysis

想我这种菜鸟，估计也提供不了什么好的思考问题的方法。

我只会一点简单的DP，看到这个题也就是向DP靠，根本没考虑有没有重叠子问题，有没有最优子结构。（[这都是个啥？](https://zh.wikipedia.org/wiki/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)）

糙快猛，列方程：

`dp[i][j][k]`表示robot跑到`i`行`j`列目前移动方向为`k`时，所需要的最小的flip。其中`0 <= i <= N`，`0 <= j <= M`，`k = right/down`

    :::C++
    
    //           j-1    j
    //     i-1          r`  
    //                  |
    //       i    r``-- ?--> right
    //
    //     i+1          ?
    dp[i][j][right] = min(dp[i][j-1][right], dp[i-1][j][down] + (i+1 < n && maze[i+1][j] != 'b')) + (maze[i][j] == 'b');

    //          j-1    j   j+1
    //    i-1          r`  
    //                 |
    //      i    r``-- ?    ?
    //                 |
    //                 v
    //                 down
    dp[i][j][down] = min(dp[i-1][j][down], dp[i][j-1][right] + (j+1 < m && maze[i][j+1] != 'b')) + (maze[i][j] == 'b');


有了这些结论，代码比较容易写出来了。

### Solution

下面是C++实现的完整代码：

    :::C++
    #include <iostream>
    #include <vector>

    using namespace std;

    int solve(vector<vector<char>> &maze)
    {
        const int n = maze.size();
        const int m = maze.front().size();
        vector<vector<vector<int>>> dp(n, vector<vector<int>>(m, vector<int>(2)));
        dp[0][0][0] = maze[0][0] == 'b';
        dp[0][0][1] = dp[0][0][0] + (1 < m && maze[0][1] != 'b');
        for (int i = 1; i < n; ++i) {
            dp[i][0][1] = min(dp[i-1][0][0] + (1 < m && maze[i-1][1] != 'b'), dp[i-1][0][1]) + (maze[i][0] == 'b');
            dp[i][0][0] = dp[i][0][1] + (i+1 < n && maze[i+1][0] != 'b');
        }
        for (int i = 1; i < m; ++i) {
            dp[0][i][0] = min(dp[0][i-1][1] + (1 < n && maze[1][i-1] != 'b'), dp[0][i-1][0]) + (maze[0][i] == 'b');
            dp[0][i][1] = dp[0][i][0] + (i+1 < m && maze[0][i+1] != 'b');
        }
        for (int i = 1; i < n; ++i) {
            for (int j = 1; j < m; ++j) {
                dp[i][j][0] = min(dp[i][j-1][0], dp[i-1][j][1] + (i+1 < n && maze[i+1][j] != 'b')) + (maze[i][j] == 'b');
                dp[i][j][1] = min(dp[i-1][j][1], dp[i][j-1][0] + (j+1 < m && maze[i][j+1] != 'b')) + (maze[i][j] == 'b');
            }
        }
        return min(dp[n-1][m-1][0], dp[n-1][m-1][1]);
    }

    int main(void)
    {
        int n, m;
        while (cin >> n >> m) {
            vector<vector<char>> maze(n, vector<char>(m));
            for (int i = 0; i < n; ++i) {
                for (int j = 0; j < m; ++j) {
                    cin >> maze[i][j];
                }
            }
            cout << solve(maze) << endl;
        }
    }

### Complexity

* 时间复杂度：O(n*m)
* 空间复杂度：O(n*m)

（全文完）

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
