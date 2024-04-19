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

string item;//��ʼ�����ַ���
int hex_index = 0;
int pre_length = size(item);
int num = 0;//��ǰ�������

// ����DES��Կ����Կ���ȱ�
DES_cblock key;
DES_key_schedule schedule;

vector<string> plaintext = { 0 };//���ķ���
vector<string> pre_result = { 0 };

int isAlnum(char c) {//�������Ƿ���16������
    return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f');
}


void read_in(string input_name) {
    ifstream in_file;//�����ļ�
    in_file.open(input_name);
    getline(in_file, item);
    for (int i = 0; i < item.length(); i += 16) {
        plaintext.push_back(item.substr(i, 16));
    }
}
void write_down(string output_name) {

    // ���� ofstream ���󣬲����ļ�
    std::ofstream outfile(output_name);

    // ����ļ��Ƿ�ɹ���
    if (!outfile.is_open()) {
        std::cerr << "�ļ���ʧ��" << std::endl;
        return;
    }
    std::ostringstream oss;

    // ������Ԫ��д���ַ�����
    for (int i = 0; i < (item.length() / 16) + 1; ++i) {
        oss << pre_result[i] << " ";
    }
    // Ҫд�������
    std::string content = oss.str();

    // д���ļ�
    outfile << content;

    // �ر��ļ�
    outfile.close();

    std::cout << "�ļ�д��ɹ�" << std::endl;

    return;
}


void main_solution() {
    string hex_num1 = plaintext[num]; // ��ǰ���ķ���
    string hex_num2 = pre_result[num]; // ǰһ�εݹ�Ľ��
    // ��ʮ�������ַ���ת��Ϊʮ��������
    long num1, num2;
    stringstream(hex_num1) >> hex >> num1;
    stringstream(hex_num2) >> hex >> num2;
    // ִ��������
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
    char* iv = argv[1];//cbc�ĳ�ʼ�ַ���
    char* key_str = argv[2];//des������Կ
    char* inputfile = argv[3];//�����ļ���
    char* outputfile = argv[4];//����ļ���

    int iv_length = strlen(argv[1]);
    int key_length = strlen(argv[2]);

    //��֤�����ĺϷ���
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
            return 1; // ���������ĸ�����֣�����1
        }
        iv++;
    }
    i = 0;
    while (++i <= 16) {
        if (!isAlnum(*key_str)) {
            printf("The characters of key are not valid! \n");
            return 1; // ���������ĸ�����֣�����1
        }
        key++;
    }

    // ���ַ�����ʽ����Կת��ΪDES_cblock���͵���Կ
    memcpy(&key, argv[2], 8);
    // ʹ��DES_set_key_unchecked����������Կ
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
