import socket
import hashlib
import random
import pickle
import sys
import struct

def hash_and_power(u, w, r):
    # 连接字符串u和w
    concat_str = u + w
    
    # 对连接后的字符串进行SHA-256哈希运算
    hashed = hashlib.sha256(concat_str.encode()).hexdigest()
    
    # 将哈希结果转换为整数
    hashed_int = int(hashed, 16)
    
    # 对整数进行k次方运算
    result = pow(hashed_int,r)
    
    return result

# 创建一个UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定客户端地址和端口
client_address = ('localhost', 54321)
client_socket.bind(client_address)

# 服务器地址和端口
server_address = ('localhost', 12345)

# 输入 k 和 z
u = input("请输入 用户名: ")
w = input("请输入 密码: ")

r = random.randint(1, 100)

x = hash_and_power(u, w, r)

hashed_value = hashlib.sha256(u.encode()).hexdigest()
b = hashed_value[:2]


# 将 x 转换为字节串
x_bytes = x.to_bytes((x.bit_length() + 7) // 8, 'big')

# 将 x 字节串拆分成多个段，并逐个发送
segment_size = 4096

num_segments = int((len(x_bytes) + segment_size - 1) // segment_size)
client_socket.sendto(f'{num_segments}'.encode(), server_address)

for i in range(num_segments):
    start = int(i * segment_size)
    end = int(min((i + 1) * segment_size, len(x_bytes)))
    segment_data = x_bytes[start:end]

    
    # 在数据前面添加一个4字节的序号，用来标识数据包的顺序
    packet = struct.pack('I', i) + segment_data
    
    client_socket.sendto(packet, server_address)

client_socket.sendto(f'{b}'.encode(), server_address)

# 接收服务器发送的数据
column, server = client_socket.recvfrom(4096*2)
print("成功接收column")

# 反序列化接收到的数据
rows = pickle.loads(column)

received_data = b""
received_packets = {}
data, server_address = client_socket.recvfrom(4096)

num_segments = data.decode()  # 将接收到的字节串解码为字符串
num_segments = int(num_segments)  # 将字符串转换为整数类型

while len(received_packets) < num_segments:
    # 接收数据包
    packet, client = client_socket.recvfrom(4096)
    
    # 解析序号和数据
    seq_number, data = struct.unpack('I', packet[:4])[0], packet[4:]
    
    # 将数据包存储到字典中
    received_packets[seq_number] = data

# 将接收到的数据按顺序组装
for i in range(num_segments):
    received_data += received_packets[i]

# 解析接收到的数据
y = struct.unpack('Q', received_data[:8])[0]
print("成功接收y")



y_float = float(y)
x_ = pow(y_float, 1/r)
x_ = pow(x_, 1/7)
x_str = str(x_)
print("x_:" + x_str)

# 在查询结果中查找特定数据的示例
target_data = 'x_'
for row in rows:
    if target_data in row:
        print("match")
        break
else:
    print("none")

# 关闭连接
client_socket.close()
