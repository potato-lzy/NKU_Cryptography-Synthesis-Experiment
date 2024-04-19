#include <iostream>
#include<string>
#include<bitset>
#include<fstream>
#include<vector>
#include<sstream>
#include <openssl/des.h>
using namespace std;
#define ENC 1
#define DEC 0

string item;//初始明文字符串
int hex_index = 0;
int pre_length = size(item);
int num = 0;//当前明文组号

// 定义DES密钥和密钥调度表
DES_cblock key;
DES_key_schedule schedule;

vector<string> plaintext = { 0 };//明文分组
vector<string> pre_result = { 0 };

int isAlnum(char c) {//检查参数是否是16进制数
    return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f');
}


void read_in(string input_name) {
    ifstream in_file;//输入文件
    in_file.open(input_name);
    getline(in_file, item);
    for (int i = 0; i < item.length(); i += 16) {
        plaintext.push_back(item.substr(i, 16));
    }
}
void write_down(string output_name) {

    // 创建 ofstream 对象，并打开文件
    std::ofstream outfile(output_name);

    // 检查文件是否成功打开
    if (!outfile.is_open()) {
        std::cerr << "文件打开失败" << std::endl;
        return;
    }
    std::ostringstream oss;

    // 将数组元素写入字符串流
    for (int i = 0; i < (item.length() / 16) + 1; ++i) {
        oss << pre_result[i] << " ";
    }
    // 要写入的内容
    std::string content = oss.str();

    // 写入文件
    outfile << content;

    // 关闭文件
    outfile.close();

    std::cout << "文件写入成功" << std::endl;

    return;
}


void main_solution() {
    string hex_num1 = plaintext[num]; // 当前明文分组
    string hex_num2 = pre_result[num]; // 前一次递归的结果
    // 将十六进制字符串转换为十进制整数
    long num1, num2;
    stringstream(hex_num1) >> hex >> num1;
    stringstream(hex_num2) >> hex >> num2;
    // 执行异或操作
    long mid_1 = (num1 ^ num2);   
    char* mid;
    strcpy(mid, mid_1);
    memcpy(mid_result,mid,64);
    pre_result[num] = DES_encrypt1(mid_result, &key, ENC);
    num++;
    if (num == (item.length() / 16) + 1) return;
    main_solution();
}

int main(char* argv[])
{
    char* iv = argv[1];//cbc的初始字符串
    char* key_str = argv[2];//des加密密钥
    char* inputfile = argv[3];//输入文件名
    char* outputfile = argv[4];//输出文件名

    int iv_length = strlen(argv[1]);
    int key_length = strlen(argv[2]);

    //验证参数的合法性
    if (iv_length != 16) {
        printf("Length of iv is not valid! \n");
        return 1;
    }
    if (key_length != 16) {
        printf("Length of key is not valid! \n");
        return 1;
    }

    int i = 0;
    while (++i <= 16) {
        if (!isAlnum(*iv)) {
            printf("The characters of iv are not valid! \n");
            return 1; // 如果不是字母或数字，返回1
        }
        iv++;
    }
    i = 0;
    while (++i <= 16) {
        if (!isAlnum(*key_str)) {
            printf("The characters of key are not valid! \n");
            return 1; // 如果不是字母或数字，返回1
        }
        key++;
    }

    // 将字符串形式的密钥转换为DES_cblock类型的密钥
    memcpy(&key, argv[2], 8);
    // 使用DES_set_key_unchecked函数设置密钥
    DES_set_key_unchecked(&key, &schedule);

    int k, n;
    pre_result[0] = iv;

    read_in(inputfile);
    main_solution();
    write_down(outputfile);

    //std::cout << "DES Clear Text: " << in[0] << in[1] << std::endl;
    //des_encrypt1((des_cblock*)in, &key, ENC);

    //std::cout << "DES Encryption: " << in[0] << in[1] << std::endl;

    //des_encrypt1((des_cblock*)in, &key, DEC);

    return 0;
}
