#include <iostream>
#include <stack>

using namespace std;

// 方案一
class Mystack1{
    stack<int> stackData;
    stack<int> stackMin;

public:

    Mystack1(){

    }

    void push(int newNum){
        if(this->stackMin.empty()){
            this->stackMin.push(newNum);
        }else if(newNum <= this->getMin()){
            this->stackMin.push(newNum);
        }
        this->stackData.push(newNum);
    }

    int pop(){
        if(this->stackData.empty()){
            cout << "The stackData is empty!" << endl;
            exit(-1);
        }
        int val = this->stackData.top();
        this->stackData.pop();
        if(val == this->stackMin.top()){
            this->stackMin.pop();
        }
        return val;
    }

    int getMin(){
        if(this->stackMin.empty()){
            cout << "The stackMin is empty!" << endl;
            exit(-1);
        }else{
            return this->stackMin.top();
        }
    }
};

// 方案二
class Mystack2{
    stack<int> stackData;
    stack<int> stackMin;

public:

    Mystack2(){

    }

    void push(int newNum){
        if(this->stackMin.empty()){
            this->stackMin.push(newNum);
        }else if(newNum < this->getMin()){
            this->stackMin.push(newNum);
        }else{
            this->stackMin.push(this->stackMin.top());
        }
        this->stackData.push(newNum);
    }

    int pop(){
        if(this->stackData.empty()){
            cout << "The stackData is empty!" << endl;
            exit(-1);
        }
        this->stackMin.pop();
        int val = this->stackData.top();
        this->stackData.pop();
        return val;
    }

    int getMin(){
        if(this->stackMin.empty()){
            cout << "The stackMin is empty!" << endl;
            exit(-1);
        }else{
            return this->stackMin.top();
        }
    }
};


int main() {
    Mystack1 * st1 = new Mystack1;
    st1->push(3);
    cout << st1->getMin() << endl;
    st1->push(4);
    cout << st1->getMin() << endl;
    st1->push(5);
    cout << st1->getMin() << endl;
    st1->push(1);
    cout << st1->getMin() << endl;
    st1->push(2);
    cout << st1->getMin() << endl;
    st1->push(1);
    cout << st1->getMin() << endl;

    st1->pop();
    cout << st1->getMin() << endl;
    st1->pop();
    cout << st1->getMin() << endl;
    st1->pop();
    cout << st1->getMin() << endl;
    st1->pop();
    cout << st1->getMin() << endl;
    st1->pop();
    cout << st1->getMin() << endl;
    st1->pop();
    cout << st1->getMin() << endl;

    /*
output:
3
3
3
1
1
1
1
1
3
3
3
The stackMin is empty!
     */

    cout << endl;

    Mystack2 * st2 = new Mystack2;
    st2->push(3);
    cout << st2->getMin() << endl;
    st2->push(4);
    cout << st2->getMin() << endl;
    st2->push(5);
    cout << st2->getMin() << endl;
    st2->push(1);
    cout << st2->getMin() << endl;
    st2->push(2);
    cout << st2->getMin() << endl;
    st2->push(1);
    cout << st2->getMin() << endl;

    st2->pop();
    cout << st2->getMin() << endl;
    st2->pop();
    cout << st2->getMin() << endl;
    st2->pop();
    cout << st2->getMin() << endl;
    st2->pop();
    cout << st2->getMin() << endl;
    st2->pop();
    cout << st2->getMin() << endl;
    st2->pop();
    cout << st2->getMin() << endl;

    /*
output:
3
3
3
1
1
1
1
1
3
3
3
The stackMin is empty!
     */

    return 0;
}