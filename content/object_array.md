title: On Object Array
category: C/CPP
tags: cpp, array, contructor
date: 2015-04-11 23:54

>Whereever an object array is defined in an cpp program, the array is always initialized. If no initializer is given,
>the default constructor is invoked. The following simple program speaks louder than words.

    :::c++

    #include <iostream>

    using std::cout;
    using std::endl;

    class Test {
        public:
            Test () {cout << "Test constructor invoked " << counter++ << endl; }
        private:
            static int counter;
    };

    int Test::counter = 0;

    int main(void)
    {
        Test test_array[10];
        cout << sizeof(Test) << " " << sizeof(test_array) << endl;
        return 0;
    }

The Result is as follow:

    :::
    Test constructor invoked 0
    Test constructor invoked 1
    Test constructor invoked 2
    Test constructor invoked 3
    Test constructor invoked 4
    Test constructor invoked 5
    Test constructor invoked 6
    Test constructor invoked 7
    Test constructor invoked 8
    Test constructor invoked 9
    1 10

One some thing you may notice is that a class without any instance variables has a size of 1 byte.
