title: Yet Another Toy Compiler Compiler
slug: yet-another-toy-compiler-compiler
date: 2016-11-11 15:16:50
category: C/CPP
tags: c, compiler, regular expression, automaton
keywords: engineering a compiler, compiler, regex, automaton
description: yet another attempt to learn compiler

> If all you have is a hammer, everything looks like a nail.  ---Maslow 

## 前言

忽然又有了些时间，所以又开始折腾，又要再尝试学习编译器，学习编译原理。希望这能是一个系统的文章，让我有一天能够看到曾经不堪的自己。
最近看的书叫编译器设计，译自*Engineering a Compiler*
第二版。当前进度第二章。相比原来的情况，明白了如何写一个词法分析器的生成器，其步骤如下：

（假设词法结构由正则表达到式描述）
1. 将中缀形式的正则表达式转换为后缀表达式。（此处我只考虑了正则表达式的连接、选择和闭包操作）
2. 利用Thompson算法，将后缀形式的正则表达式，转换为非确定性有限自动机(NFA, Nondeterministic Finite Automaton)。
3. 利用子集构造法，将NFA转换为确定性有限自动机(DFA, Deterministic Finite Automaton)。
4. 利用Hopcroft算法，将DFA最小化。
5. 最小化后的DFA可以用来作为Tokenizer。

## 玩具

根据书中的描述，勉强实现了部分玩具功能，这么代码做了很大的简化，并且以功能实现为主。

### 中缀转后缀

按照之前的设想，支持的正则表达式，只有连接、选择和闭包三种操作，并允许括号来改变优先级。

Token的类型和定义如下：

    :::cpp
    enum class TokenType{
        OPERAND,
        STAR,
        CONCATENATE,
        BAR,
        LEFT_PARENTTHESIS, // always pushed into stack 
        RIGHT_PARENTHESIS  // never pushed into stack
    };

    struct Token {
        TokenType type;
        char value;
    };

中缀表达式转后缀表达式时，运行符优先级由TokenType给出，越早出现的优先级越高。

    :::cpp
    std::vector<Token> postfix2postfix(const std::vector<Token> &tokens)
    {
        std::vector<Token> postfix;
        postfix.reserve(tokens.size());
        std::stack<Token> st;
        for (auto &token : tokens) {
            if (token.type == TokenType::OPERAND)
                postfix.push_back(token);
            else if (token.type == TokenType::RIGHT_PARENTHESIS) {
                while (!st.empty() && TokenType::LEFT_PARENTTHESIS != st.top().type) {
                    postfix.push_back(st.top());
                    st.pop();
                }
                st.pop();
            } else {
                if (token.type != TokenType::LEFT_PARENTTHESIS) {
                    while (!st.empty() && token.type >= st.top().type) {
                        postfix.push_back(st.top());
                        st.pop();
                    }
                }
                st.push(token);
            }
        }
        while (!st.empty()) {
            postfix.push_back(st.top());
            st.pop();
        }
        return postfix;
    }

### Thompson算法

通过后缀表达式求值的方法，可以将正则表达式转换为NFA。

    :::cpp
    #define NFA_UNARY(st, op) do { \
        assert(st.size() >= 1); \
        auto rhs = st.top(); \
        st.pop(); \
        st.emplace(op rhs); \
    } while(0)
    
    #define NFA_BINARY(st, op) do { \
        assert(st.size() >= 2); \
        auto rhs = st.top(); \
        st.pop(); \
        auto lhs = st.top(); \
        st.pop(); \
        st.emplace(lhs op rhs); \
    } while(0)
    
    NFA Thompson(const std::vector<Token> &re)
    {
        std::stack<NFA> st;
        for (auto &token : re) {
            switch (token.type) {
                case TokenType::OPERAND:
                    st.emplace(token.value);
                    break;
                case TokenType::STAR:
                    NFA_UNARY(st, *);
                    break;
                case TokenType::CONCATENATE:
                    NFA_BINARY(st, +);
                    break;
                case TokenType::BAR:
                    NFA_BINARY(st, |);
                    break;
                default:
                    abort();
            }
        }
        return st.top();
    }

### NFA实现

由Thompson算法生成的NFA主要有以下特点：

1. NFA有且仅有一个开始状态和一个接受状态。
2. 开始状态没有入边，接受状态没有出边。

因此，我最初设计的NFA抽象成如下代码：

    :::cpp
    
    constexpr char EPSILON = '\xFF';

    struct FANode {
        std::vector<FANode *> prev;
        std::multimap<char, FANode *> next;
        bool isAccepted;
        FANode () : isAccepted(false) {}
    };

    class NFA {
        FANode *s0, *sa;
    public:
        NFA (char c=EPSILON) : s0(new FANode), sa(new FANode) {
            s0->next.emplace(c, sa);
            sa->prev.push_back(s0);
            sa->isAccepted = true;
        }
        NFA (const NFA *that) {
            std::map<FANode *, FANode *> dict;
            s0 = new FANode;
            dict[that->s0] = s0;
            sa = new FANode;
            dict[that->sa] = sa;
            sa->isAccepted = true;
            copy(that->s0, dict);
        }
        NFA (const NFA &that) {
            std::map<FANode *, FANode *> dict;
            s0 = new FANode;
            dict[that.s0] = s0;
            sa = new FANode;
            dict[that.sa] = sa;
            sa->isAccepted = true;
            copy(that.s0, dict);
        }
        NFA (NFA &&that) {
            this->s0 = that.s0;
            this->sa = that.sa;
            that.s0 = that.sa = nullptr;
        }
        ~NFA () {
            if (!s0)
                return;
            std::set<FANode *> mem;
            std::queue<FANode *> q;
            q.push(s0);
            mem.insert(s0);
            while (!q.empty()) {
                auto cur = q.front();
                q.pop();
                for (auto &n : cur->next) {
                    if (mem.find(n.second) == mem.end()) {
                        q.push(n.second);
                        mem.insert(n.second);
                    }
                }
                delete cur;
            }
        }
        NFA operator+ (const NFA &) const;
        NFA operator| (const NFA &) const;
        NFA & operator* ();
        NFA & operator+= (const NFA &);
        NFA & operator|= (const NFA &);
        std::string to_mermaid();
    private:
        static void copy(FANode *s0, std::map<FANode *, FANode *> &dict) {
            std::queue<FANode *> q;
            q.push(s0);
            while (!q.empty()) {
                auto cur = q.front();
                q.pop();
                for (auto &n : cur->next) {
                    if (dict.find(n.second) == dict.end()) {
                        dict.emplace(n.second, new FANode);
                        q.push(n.second);
                    }
                    dict[cur]->next.emplace(n.first, dict[n.second]);
                    dict[n.second]->prev.push_back(dict[cur]);
                }
            }
        }

        friend std::ostream & operator<< (std::ostream &os, const NFA &nfa);
    };


每个NFA记录了其开始状态和接受状态，便于进行NFA的连接、选择和闭包操作。然而，这也导致了我在抽象DFA时陷入了两难的窘境：

- DFA是一种特殊的NFA，故NFA支持的操作逻辑上DFA都应该支持
- 然而，DFA未必只有一个终结态，其不满足我简化后的NFA类的特征。

此致，在抽象NFA时，我将状态的转移关系直接维护在状态中，使用multimap进行管理。这种方式实现简单，却使得正则表达式中的范围操作如[a-Z]非常昂贵。
下一步，准备将转移关系也抽象出来，并支持范围操作。

下面是目前支持的三种操作，连接(operator+)、选择(operator|) 和 闭包(operator*)：

    :::cpp

    NFA NFA::operator+ (const NFA &that) const {
        NFA res(this);
        return res += that;
    }

    NFA NFA::operator| (const NFA &that) const {
        NFA res(this);
        return res |= that;
    }

    NFA & NFA::operator* () {
        debug("star(NFA@0x%p)\n", this);
        FANode *ns0 = new FANode, *nsa = new FANode;
        nsa->isAccepted = true;

        this->sa->isAccepted = false;
        this->sa->next.emplace(EPSILON, this->s0);
        this->sa->next.emplace(EPSILON, nsa);
        nsa->prev.push_back(this->sa);

        ns0->next.emplace(EPSILON, this->s0);
        ns0->next.emplace(EPSILON, nsa);

        this->s0 = ns0;
        this->sa = nsa;
        return *this;
    }

    NFA & NFA::operator+= (const NFA &that) {
        debug("NFA@0x%p + NFA@0x%p\n", this, &that);
        assertm(this->sa->next.empty(), "The accepted state of NFA@0x%p should not have any succeeding", this);
        this->sa->isAccepted = false;

        std::map<FANode *, FANode *> dict;

        dict.emplace(that.s0, new FANode);
        this->sa->next.emplace(EPSILON, dict[that.s0]);
        dict[that.s0]->prev.push_back(this->sa);

        dict.emplace(that.sa, new FANode);
        dict[that.sa]->isAccepted = true;
        copy(that.s0, dict);
        this->sa = dict[that.sa];

        return *this;
    }

    NFA & NFA::operator|= (const NFA &that) {
        debug("NFA@0x%p | NFA@0x%p\n", this, &that);
        FANode *ns0 = new FANode, *nsa = new FANode;
        nsa->isAccepted = true;

        ns0->next.emplace(EPSILON, this->s0);
        this->s0->prev.push_back(ns0);
        this->sa->isAccepted = false;
        this->sa->next.emplace(EPSILON, nsa);
        nsa->prev.push_back(this->sa);

        this->s0 = ns0;
        this->sa = nsa;

        std::map<FANode *, FANode *> dict;

        dict.emplace(that.s0, new FANode);
        ns0->next.emplace(EPSILON, dict[that.s0]);
        dict[that.s0]->prev.push_back(ns0);
        dict.emplace(that.sa, new FANode);
        dict[that.sa]->next.emplace(EPSILON, nsa);
        nsa->prev.push_back(dict[that.sa]);
        copy(that.s0, dict);

        return *this;
    }

下面是一些NFA的格式化输出，用于方便地观察生成的NFA的形态。感谢[mermaid](https://github.com/knsv/mermaid)可以允许以图形的方式查看我的NFA。

    :::cpp
    std::ostream & operator<< (std::ostream &os, const FANode *fan) {
        os << "0x" << std::hex << reinterpret_cast<unsigned long>(fan) << std::dec;
        if (fan->isAccepted)
            os << "[$]";
        return os;
    }

    std::ostream & operator<< (std::ostream &os, const FANode &fan) {
        return operator<< (os, &fan);
    }

    std::ostream & operator<< (std::ostream &os, const NFA &nfa) {
        std::queue<FANode *> q;
        std::set<FANode *> mem;
        q.push(nfa.s0);
        while (!q.empty()) {
                auto cur = q.front();
                q.pop();
                os << cur << "=>{";
                for (auto n : cur->next) {
                    if (mem.find(n.second) == mem.end() && !n.second->isAccepted) {
                        mem.emplace(n.second);
                        q.push(n.second);
                    }
                    os << n.first << ":" << n.second << ";";
                }
                os << "};";
        }
        return os;
    }

    std::string NFA::to_mermaid() {
        std::ostringstream os;
        std::queue<FANode *> q;
        std::map<FANode *, unsigned> dict;
        unsigned index = 0;
        q.push(this->s0);
        dict.emplace(this->s0, index++);
        dict.emplace(this->sa, index++);
        while (!q.empty()) {
                auto cur = q.front();
                q.pop();
                for (auto n : cur->next) {
                    if (dict.find(n.second) == dict.end()) {
                        dict.emplace(n.second, index++);
                        q.push(n.second);
                    }
                    os << "s" << dict[cur] << "--";
                    if (n.first == EPSILON)
                        os << "eplisoin";
                    else
                        os << n.first;
                    os << "-->" << "s" << dict[n.second];
                    if (n.second->isAccepted)
                        os << "((" << "s" << dict[n.second] << "))";
                    os << '\n';
                }
        }
        return os.str();
    }

### 测试

由于没有实现对正则表达式的Tokenizer，输出的中缀形式的正则表达式，只有以丑陋的手工方式进行Token分割。（鸡生蛋，蛋生鸡呀，我在写一个Lexer
Compiler啊）

    :::cpp
    std::vector<Token> postfix{
        {TokenType::OPERAND, 'a'},
        {TokenType::CONCATENATE, '+'},
        {TokenType::LEFT_PARENTTHESIS, '('},
        {TokenType::OPERAND, 'b'},
        {TokenType::BAR, '|'},
        {TokenType::OPERAND, 'c'},
        {TokenType::RIGHT_PARENTHESIS, ')'},
        {TokenType::STAR, '*'}
    };
    std::vector<Token> tokens = postfix2postfix(postfix);

    NFA res = Thompson(tokens);

    std::cout << res.to_mermaid() << std::endl;

输出：

    :::bash
    s0--a-->s2
    s2--eplisoin-->s3
    s3--eplisoin-->s4
    s3--eplisoin-->s1((s1))
    s4--eplisoin-->s5
    s4--eplisoin-->s6
    s5--b-->s7
    s6--c-->s8
    s7--eplisoin-->s9
    s8--eplisoin-->s9
    s9--eplisoin-->s4
    s9--eplisoin-->s1((s1))

借助mermaid可视化为：

![mermaid](/assets/images/nfa.png)

(期待我还能写一篇)
