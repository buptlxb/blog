title: linux tricks
slug: linux-tricks
date: 2016-08-09 17:08:39
category: Linux
tags: cpp, linux, shell
keywords: shell, linux, tricks
description: 开发常用技巧收集 

> If all you have is a hammer, everything looks like a nail.  ---Maslow 

### Find MACRO definition in header file

    :::bash
    cpp -dM -E /usr/include/netinet/in.h | grep SOCKADDR_COMMON