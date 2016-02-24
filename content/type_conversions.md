title: Type Conversions
category: C/CPP
tags: cpp, type, constructor
date: 2016-02-24 16:01:41

>Type conversions are very complicated in C++ language. Maybe you do not agree with me. But it really makes me crazy!
>Type conversions contain many and many topics, such as integer promotion, array degrading to pointers, type castings 
>and so on. Some kinds of type conversions are easy to understand, however, it is quiet hard to know the other kinds of type conversions well.
>Even worse, all of them are easily forgotten.

## Integer Promotion

It is relatively easy to understand Integer Promotion. In a word, integer promotion simplily converts integer from low
precision to high one and from signed to unsigned, such as from `char` to `short`, from `short` to `unsigned short`.

## Array degrading to pointers

Array is a special type in C/C++. You can easily define a array with `Type []`. But you can never pass an array to a
function. When you try to do this, the array degrades to pointer implicitly. It is why we all declare a function like
`Return-type function-name (Type [], Size_t)`.

## Type castings

Type castings usually mean explicit type conversions. There are four type casting operators `static_cast`,
`dynamic_cast`, `const_cast`, `reinterpret_cast`.

## Type conversions with class

When type conversions meet class, things go worse. `single-argument constructors`, `assignment operator`,
`type-cast operator` are all relative with implicit type conversions. These three member functions can be
controlled by user to define their own type conversions.


## Rules of Type Conversions

* There must not be two or more user defined type conversions in any sequence of conversions.

    There are more rules of type conversions in C++. I will add them here when I come across to them.
