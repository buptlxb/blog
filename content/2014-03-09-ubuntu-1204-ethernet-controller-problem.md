title: Ubuntu 12.04 Ethernet Controller Problem
category: Linux
tags: Linux, Network, Ubuntu


## Problem

Ethernet controller can not detect the cable.

## Solution

``` bash

wget http://r8168.googlecode.com/files/r8168-8.037.00.tar.bz2
tar xjf r8168-8.037.00.tar.bz2
cd r8168-8.037.00
./autorun.sh

```

