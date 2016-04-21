title: 微软2016校园招聘4月在线笔试题解(四)
category: C/CPP
tags: cpp, algorithm, hihocoder
date: 2016-04-09 14:58:38
keywords: algorithm, hihocoder, Microsoft, 微软笔试
description: 微软2016校园招聘4月在线笔试题解第四题，Building in Sandbox

> If all you have is a hammer, everything looks like a nail.  ---Maslow

## D. Buiding in Sandbox

### Problem

时间限制:30000ms
单点时限:3000ms
内存限制:256MB

#### 描述

Little Hi is playing a sandbox voxel game. In the game the whole world is constructed by massive 1x1x1 cubes. The edges of cubes are parallel to the coordinate axes and the coordinates (x, y, z) of the center of each cube are integers.

At the beginning there is nothing but plane ground in the world. The ground consists of all the cubes of z=0. Little Hi needs to build everything by placing cubes one by one following the rules:

1. The newly placed cube must be adjacent to the ground or a previously placed cube. Two cubes are adjacent if and only if they share a same face.

2. The newly placed cube must be accessible from outside which means by moving in 6 directions(up, down, left, right, forward, backward) there is a path from a very far place - say (1000, 1000, 1000) in this problem - to this cube without passing through ground or other cubes.

Given a sequence of cubes Little Hi wants to know if he can build the world by placing the cubes in such order.

#### 输入

The first line contains the number of test cases T(1 <= T <= 10).

For each test case the first line is N the number of cubes in the sequence.

The following N lines each contain three integers x, y and z indicating the coordinates of a cube.



For 20% of the data, 1 <= N <= 1000, 1 <= x, y, z <= 10.

For 100% of the data, 1 <= N <= 100000, 1 <= x, y, z <= 100.

#### 输出

For each testcase output "Yes" or "No" indicating if Little Hi can place the cubes in such order.

样例提示

In the first test case three cubes are placed on the ground. It's OK.

In the second test case (1, 3, 2) is neither on the ground nor adjacent to previous cubes. So it can't be placed.

In the last test case (2, 2, 1) can not be reached from outside. So it can't be placed.  

样例输入

    :::
    3
    3
    1 1 1
    1 2 1
    1 3 1
    3
    1 1 1
    1 2 1
    1 3 2
    17
    1 1 1
    1 2 1
    1 3 1
    2 3 1
    3 3 1
    3 2 1
    3 1 1
    2 1 1
    2 1 2
    1 1 2
    1 2 2
    1 3 2
    2 3 2
    3 3 2
    3 2 2
    2 2 2
    2 2 1

样例输出

    :::
    Yes
    No
    No

### Analysis

Buiding in Sandbox ???
Building in Sandbox !

算了，还是分析题吧。。。

题目大意就是，沙盒中搭建筑，基本元素为1x1x1的立方体，现在地面已经铺满了立方体了(z坐标为0)，并且立方体没有斜着的。

新添加的立方体有些要求：

1. 必须挨着一个之前放好的立方体。
2. 立方体必须能放进去，即存在一条路径从很高的地方可以移动到目标地方，而不穿过已有的立方体。
3. 对于条件2，简单的理解就是：**当这个建筑搭好了，你要能够，按照立方体添加顺序的逆序把它拆了！**

因此，检查的方法：

1. 对于条件1，放置时，检查上下左右前后有没有已放的立方体。若有，则标记该位置放了一个立方体；否则，返回No。
2. 对于条件2，当所有立方体放置完毕后，执行拆除。即，倒序遍历每一个放置的立方体，决定是否存在一条路径可以到达很高的地方（101，101，101）
若有，则标记该位置没有立方体了（恭喜，被你成功拆掉了^-^）；否则，返回No。

两个点间是否存在一条路径，我竟然也会写了？？？好吧，DFS和BFS都可以做这事的，我选了BFS，比较好做一些优化。（真的是我选的吗？——)

有了这些结论，代码比较容易写出来了。

### Solution

下面是C++实现的完整代码：

    :::C++

    #include <iostream>
    #include <cstring>
    #include <queue>

    using namespace std;

    bool sandbox[102][102][102];
    int visited[102][102][102];
    int dir[6][3] = {
        {-1, 0, 0}, {0, -1, 0}, {0, 0, -1},
        {1, 0, 0}, {0, 1, 0}, {0, 0, 1}
    };

    struct Cord{
        int x, y, z;
        Cord(int a, int b, int c) : x(a), y(b), z(c) {}
        Cord() : x(0), y(0), z(0) {}
    } cords[100001];

    int min_x, min_y, min_z, max_x, max_y, max_z;

    bool bfs(int a, int b, int c, int n)
    {
        sandbox[c][a][b] = false;
        bool ret = false;
        queue<Cord> q;
        q.push(Cord(a, b, c));
        visited[c][a][b] = n;
        while (!q.empty()) {
            int x = q.front().x;
            int y = q.front().y;
            int z = q.front().z;
            q.pop();
            if (x < min_x || y < min_y || z < min_z || x > max_x || y > max_y || z > max_z) {
                ret = true;
                break;
            }
            for (int i = 0; i < 6; ++i) {
                int nz = z + dir[i][0];
                int nx = x + dir[i][1];
                int ny = y + dir[i][2];
                if (!sandbox[nz][nx][ny] && n != visited[nz][nx][ny]) {
                    if (visited[nz][nx][ny]) {
                        ret = true;
                        break;
                    } else {
                        visited[nz][nx][ny] = n;
                        q.push(Cord(nx, ny, nz));
                    }
                }
            }
        }
        return ret;
    }

    bool unbuild(int n)
    {
        memset(visited, 0, sizeof(visited));
        while (n-- > 0) {
            if (!bfs(cords[n].x, cords[n].y, cords[n].z, n+1))
                return false;
        }
        return true;
    }

    bool build(int x, int y, int z)
    {
        if (sandbox[z][x][y])
            return false;
        int i;
        for (i = 0; i < 6; ++i) {
            if (sandbox[z+dir[i][0]][x+dir[i][1]][y+dir[i][2]])
                break;
        }
        if (i == 6)
            return false;

        sandbox[z][x][y] = true;
        min_x = min(min_x, x);
        max_x = max(max_x, x);
        min_y = min(min_y, y);
        max_y = max(max_y, y);
        min_z = min(min_z, z);
        max_z = max(max_z, z);
        return true;
    }

    int main(void)
    {
        int t;
        cin >> t;
        for (int i = 0; i < t; ++i) {
            memset(sandbox, false, sizeof(sandbox));
            memset(sandbox[0], true, sizeof(sandbox[0]));
            int n;
            cin >> n;
            bool res = true;
            for (int j = 0; j < n; ++j) {
                int x, y, z;
                cin >> x >> y >> z;
                cords[j].x = x;
                cords[j].y = y;
                cords[j].z = z;
                if (!res)
                    continue;
                res = build(x, y, z);
            }
            res = res ? unbuild(n) : false;
            cout << (res ? "Yes" : "No") << endl;
        }
    }


我不想用这么多全局量啊，我也不想这样啊。

除了BFS的一点优化，我竟然还尝试维护了一个最远点？一个？

### Complexity

* 时间复杂度：O(X*Y*Z) ?? 不怎么会算。。。
* 空间复杂度：O(X*Y*Z)

（全文完）

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
