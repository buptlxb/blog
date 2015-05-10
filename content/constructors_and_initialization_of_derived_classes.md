title: Derived Class Constructor Initializer List
date: 2015-04-15 20:35
category: C/CPP
tags: constructor, inheritance

**Encapsulation**, **Inheritance** and **Polymorphism** are three key concepts in Object-Oriented Programing.
Here is something intresting about derived class constructor initializer list.

    :::cpp
    #include <stdio.h>

    struct X {
        X (int m): _m(m) {}
        X () : _m(20150304) {}
        protected:
        int _m;
    };

    struct A : public X {
        A (short m) { _m = m; }

    };

    struct B : public X {
        B () {}
    };

    struct C : public X {
        C (short m):X(m) {}
    };

    struct D : public X {
        D (int m) :  _m(m){}
    };

    struct E : public X {
        E (short m) :X(_m*m) {}
    };

    int main(void)
    {
        return 0;
    }

One of the derived class is incorrect. If you can figure out which one is incorrect, it is not necessary for you to read
the [post](http://www.learncpp.com/cpp-tutorial/114-constructors-and-initialization-of-derived-classes/).








****************************************************************************************************

The answer is D. Initializing variable of base class in initialization list of constructor of derived class is
forbidden. The rational behind this rule may relate to the difference between **initialization** and **assignment**.
