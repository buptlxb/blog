title: 程序员的模运算
category: C/CPP
tags: cpp, algorithm, hihocoder
date: 2016-04-22 14:57:28
keywords: algorithm, modulo, prime
description: "关于求模运算的常识"

> One thing I know is that I know nothing.  ---Socrates

## What is that?

求模运算是程序员的常用操作，C/CPP中使用`%`进行运算。程序员的描述通常是对于整数`a`和`b`，`a %
b`表示a除以b后，除不尽的那部分。（好吧，不是程序员，这是我的常用描述，小学水平。。。）

`3 % 2 = 1`, `6 % 10 = 6`这东西很难吗？

## Why should I care?

有些时候还是有点麻烦的：

1. <span id='p1'> `-1 % 2 = ???` </span>
2. <span id='p2'> `2 % -1 = ???` </span>
3. <span id='p3'> `(a * b) % c =? (a%c) * (b%c)` </span>
4. <span id='p4'> `(a + b) % c =? a%c + b%c` </span>
5. ...

程序员要关心这些?那看这个：

    :::C++
    bool is_odd(int x) {
        return x % 2 == 1;
    }

这个实现对吗？奇数就是除以2余1的正数，也就是`x % 2`结果是1，则x为奇数？我原来是这么想的，也是这么做的。

但是这个实现并不对，如果你有疑问那还是看完吧。

## What should I do about it

### Dividend / Divisor sign problem

对于[问题1](#p1)和[问题2](#p2)，请看下表：

| Language | Operator | result has the same sign as|
|----------|----------|----------------------------|
| AWK | % | Dividend |
| Bash | % | Dividend |
| C (ISO 1990) | % | **Implementation-defined** |
| C (ISO 1990) | div | Dividend |
| C (ISO 1995) | %, div | Dividend |
| C++ (ISO 1998) | % | **Implementation-defined** |
| C++ (ISO 1998) | div | Dividend |
| C++ (ISO 2011) | %, div | Dividend |
| Java | % | Dividend |
| Java | Math.floorMod | Divisor |
| JavaScript | % | Dividend |
| Python | % | Divisor |
| Java | math.fmod | Dividend |

### Modulo Arithmetic


#### Multiplication

对于[问题3](#p3)，显然不对，`(2 * 2) % 3 != (2 % 3) * (2 % 3)`，然而：

有下面的等式

    :::
    (a * b) % c == ((a % c) * (b % c)) % c

**证明**:

令`a%c == x`, `b%c == y`，则`a == n*c + x`, `b == m*c + y`。

易知:

    :::
    (a * b) % c
    = ((n*c + x) * (m*c + y)) % c 
    = (x*y + (x*m + n*y + n*m*c)*c) % c
    = (x * y) % c
    = ((a%c) * (b%c)) % c

证毕。

#### Addition

对于[问题4](#p4)，显然不对，`(1 + 1) % 2 != 1 % 2 + 1 % 2`，然而：

有下面的等式

    :::
    (a + b) % c == (a%c + b%c) % c

**证明**：

令`a%c == x`, `b%c == y`，则`a == n*c + x`, `b == m*c + y`。

易知:

    :::
    (a + b) % c
    = (n*c + x + m*c + y) % c 
    = (x + y) % c 
    = (a%c + b%c) % c

证毕。

## Useful Implementation

一些常见的应用：

### 正确的奇偶实现：

    :::C++
    bool is_odd(int x) {
        return (x % 2) != 0;
    }

### 大数的乘模运算：

    :::C++
    inline uint64_t mul_mod(uint64_t a, uint64_t b, uint64_t n)
    {   
        a %= n;
        b %= n;
        uint64_t ret = 0;
        while (b) {
            if (b & 1)
                ret = (ret + a) % n;
            a = (a << 1) % n;
            b >>= 1;
        }
        return ret;
    }


[1] ["Modulo operation"](https://en.wikipedia.org/wiki/Modulo_operation#cite_note-C99-2)

[2] ["Modular arithmetic"](https://en.wikipedia.org/wiki/Modular_arithmetic)

[3] ["An Introduction to Modular Arithmetic"](https://nrich.maths.org/4350)

（全文完）

（转载本站文章请注明作者和出处，请勿用于任何商业用途）
