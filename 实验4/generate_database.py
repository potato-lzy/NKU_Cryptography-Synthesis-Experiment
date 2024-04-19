from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import random
import string
import hashlib
import time

start_time = time.time()

# 创建一个 MySQL 引擎
engine = create_engine('mysql://root:root@localhost/c3server_v3')

# 创建一个元数据对象
metadata = MetaData()

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
        # 生成随机用户名
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        # 生成随机密码
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # 计算用户名的哈希值
        username_hash = hashlib.sha256(username.encode()).hexdigest()
        # 计算密码的哈希值
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        # 检查哈希前缀是否已经存在于映射中，如果不存在则创建新表
        if username_hash[:2] not in prefix_table_mapping:
            # 动态创建新表
            table_name = f"hash_data_{username_hash[:2].lower()}"
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

print(f"Total execution time: {execution_time} seconds")