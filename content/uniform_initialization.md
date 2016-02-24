title: Uniform Initialization
date: 2015-12-03 14:05:42
category: C/CPP
tag: c++11, initialization

> If you use [STL](http://www.cplusplus.com/reference/stl/) containers, the redundant initialization is really boring.
> But, the initialization for the build-in array and struct in C language is quiet easy.
> Uniform Initializatin introduced in C++11 is an exciting feature for this.

### What's it and why should I care?

C++ offers several ways of initializing an object depending on its type and the initialization context.
When misused, the error can be surprising and the error messages obscure.

It can be hard to remember the rules for initialization and to choose the best way.
The C++11 solution is to allow **{}**-initializer lists for all initialization.
Importantly, **X{a}** constructs the same value in every context, so that **{}**-initialization gives the same result in all places where it is legal.

### What should I do about it?

```c++
int arr[] {1, 2, 3, 4};
std::vector<int> vec {1, 2, 3, 4};
std::set<int> s {1, 2, 3, 4};
std::map<int, string> m { {1, "1"}, {2, "2"}, {3, "3"} };
```

### References
[1] [http://stackoverflow.com/questions/4178175/what-are-aggregates-and-pods-and-how-why-are-they-special](http://stackoverflow.com/questions/4178175/what-are-aggregates-and-pods-and-how-why-are-they-special)

[2] [http://www.stroustrup.com/C++11FAQ.html#uniform-init](http://www.stroustrup.com/C++11FAQ.html#uniform-init)
