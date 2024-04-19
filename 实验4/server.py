from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData,select
import random
import string
import hashlib
import time
import socket
import struct
import pickle


def hash_and_power(u, w, k):
    # 连接字符串u和w
    concat_str = u + w
    
    # 对连接后的字符串进行SHA-256哈希运算
    hashed = hashlib.sha256(concat_str.encode()).hexdigest()
    
    # 将哈希结果转换为整数
    hashed_int = int(hashed, 16)
    
    # 对整数进行k次方运算
    result = hashed_int ** k
    
    return result


def preduce_data(count,k):
			
    #数据库预处理

    start_time = time.time()

    # 创建一个 MySQL 引擎
    engine = create_engine('mysql://root:root@localhost/c3server_v3')


    # 定义一个 users 表
    pre_data = Table('pre_data', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(255)),
              Column('password', String(255)),
              Column('username_hash', String(255)),
              Column('password_hash', String(255)))

    hash_data = Table('hash_data', metadata,
              Column('id', Integer, primary_key=True),
              Column('username_hash', String(255)))

    # 创建表
    metadata.create_all(engine)

    prefix_table_mapping = {}

    # 准备生成的用户名数量
    num_users = 1000


    # 生成随机用户名和密码并插入到数据库中

    with engine.connect() as conn:
        for i in range(num_users):

            username = ''.join(random.choices(string.ascii_lowercase, k=8))
    
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
            username_hash = hashlib.sha256(username.encode()).hexdigest()
            # 计算密码的哈希值
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            #计算用户名||密码的hash值的k次方
            hash_and_powered = hash_and_power(username, password, k)
            # 检查哈希前缀是否已经存在于映射中，如果不存在则创建新表
            if username_hash[:2] not in prefix_table_mapping:
                # 动态创建新表
                table_name = f"{username_hash[:2].lower()}"
                prefix_table_mapping[username_hash[:2]] = Table(
                    table_name, metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username_hash', String(255))
                )
                metadata.create_all(engine)  # 创建新表
        

            # 插入数据到 pre_data 表
            conn.execute(pre_data.insert().values(
                username=username, password=password,
                username_hash=username_hash, password_hash=password_hash))

            conn.execute(prefix_table_mapping[username_hash[:2]].insert().values(
                username_hash=username_hash))

    end_time = time.time()

    execution_time = end_time - start_time

    print(f"数据库预处理 time: {execution_time} seconds")
    print('服务器已启动，数据库预处理完成')



metadata = MetaData()
# 创建一个 MySQL 引擎
engine = create_engine('mysql://root:root@localhost/c3server_v3')
# 创建一个UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定服务器地址和端口
server_address = ('localhost', 12345)
server_socket.bind(server_address)

print('服务器已启动，等待客户端连接...')


# 接收客户端发送的数据并发送响应
# 准备生成的用户名数量
count = 1000


k = int(input("请输入 密钥: "))

preduce_data(count,k)
print("数据库初始化完成")

input("按下回车键继续...")



# 接收所有分段数据
received_data = b""
received_packets = {}
data, client_address = server_socket.recvfrom(4096)

num_segments = data.decode()  # 将接收到的字节串解码为字符串
num_segments = int(num_segments)  # 将字符串转换为整数类型

while len(received_packets) < num_segments:
    # 接收数据包
    packet, client = server_socket.recvfrom(4096)
    
    # 解析序号和数据
    seq_number, data = struct.unpack('I', packet[:4])[0], packet[4:]
    
    # 将数据包存储到字典中
    received_packets[seq_number] = data

# 将接收到的数据按顺序组装
for i in range(num_segments):
    received_data += received_packets[i]

# 解析接收到的数据
x = struct.unpack('Q', received_data[:8])[0]
print("成功接收x")

b, client_address = server_socket.recvfrom(4096)
print("成功接收b: " + b.decode())

    # 将 b_bytes 解码为十六进制字符串 b
b = b.hex()
    # 指定要查询的表名
byte_string = bytes.fromhex(b)

# 将字节对象解码为字符串
table_name = byte_string.decode('utf-8')
print("table_name:"+table_name)
#table_name = str(b, 'utf-8')

    # 从数据库中获取指定表的元数据

table = Table(table_name, metadata, autoload_with=engine)



    # 连接数据库并执行查询
with engine.connect() as conn:
        # 执行 SELECT 查询
    query = table.select().with_only_columns(table.c.username_hash)



    result = conn.execute(query)
        
        # 获取查询结果
    rows = result.fetchall()

    # 使用 pickle 序列化查询结果
serialized_rows = pickle.dumps(rows)
    # 发送序列化后的查询结果给客户端
server_socket.sendto(serialized_rows, client_address)



y = pow(x,k)
# 将 x 转换为字节串
y_bytes = y.to_bytes((y.bit_length() + 7) // 8, 'big')

# 将 x 字节串拆分成多个段，并逐个发送
segment_size = 4096

num_segments = int((len(y_bytes) + segment_size - 1) // segment_size)
server_socket.sendto(f'{num_segments}'.encode(), client_address)

for i in range(num_segments):
    start = int(i * segment_size)
    end = int(min((i + 1) * segment_size, len(y_bytes)))
    segment_data = y_bytes[start:end]

    
    # 在数据前面添加一个4字节的序号，用来标识数据包的顺序
    packet = struct.pack('I', i) + segment_data
    
    server_socket.sendto(packet, client_address)
