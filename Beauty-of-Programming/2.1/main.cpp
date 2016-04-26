/*
 * 题目：求二进制数中1的个数
 * 注意：在编写程序的过程中，根据实际应用的不同，对存储空间或效率的要求也不一样
 */

#include <iostream>

using namespace std;

typedef unsigned char BYTE;

// 解法一
// 通过相除和判断余数的值来分析，时间复杂度O(log2v)
int Count1(BYTE v){
    int num = 0;
    while(v){
        if(v%2==1){
            num++;
        }
        v/=2;
    }
    return num;
}

// 解法二
// 位操作比除、余操作的效率要高很多，时间复杂度O(log2v)
int Count2(BYTE v){
    int num = 0;
    while(v){
        num += (v&0x01);
        v >>= 1;
    }
    return num;
}

// 解法三
// 时间复杂度O(M)，M为v中1的个数
int Count3(BYTE v){
    int num = 0;
    while(v){
        v &= (v-1);
        num++;
    }
    return num;
}

// 解法四
// 使用分支操作

// 解法五
// 查表法

int main() {
    cout << Count1(141) << endl;
    cout << Count2(141) << endl;
    cout << Count3(141) << endl;
    return 0;
}