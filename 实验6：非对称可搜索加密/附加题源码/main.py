from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
import hashlib

Hash1pre = hashlib.md5

salt= "None"

def Hash1(w):
    hv = Hash1pre(str(w).encode('utf8')).hexdigest()
    print("The value of Hash1(salt_and_hash_keyword(w,salt)) is:", hv)
    hv = group.hash(hv, type=G1)
    return hv

Hash2 = hashlib.sha256

def salt_and_hash_keyword(w,salt):
    # 加盐
    salted_w = w + str(salt)
    hashed_w = hash_function(salted_w)
    return hashed_w

def hash_function(input_string):
    # 在这里实现哈希函数的具体逻辑，例如使用 hashlib 库进行哈希计算
    hashed_result = hashlib.sha256(input_string.encode()).hexdigest()
    return hashed_result
    

def Setup(param_id='SS512'):
    group = PairingGroup(param_id)
    g = group.random(G1)
    alpha = group.random(ZR)
    sk = group.serialize(alpha)
    pk = [group.serialize(g), group.serialize(g ** alpha)]
    return [sk, pk]

def Enc(pk, w, param_id='SS512'):
    group = PairingGroup(param_id)
    g, h = group.deserialize(pk[0]), group.deserialize(pk[1])    
    r = group.random(ZR)
    t = pair(Hash1(w), h ** r)
    c1 = g ** r
    c2 = t
    print("The serialize value of pair(Hash1(salt_and_hash_keyword(w,salt)) , h ** r) is:", group.serialize(c2))
    return [group.serialize(c1), Hash2(group.serialize(c2)).hexdigest()]

def TdGen(sk, w, param_id='SS512'):

    group = PairingGroup(param_id)
        # 生成随机盐值
    global salt  # 声明为全局变量
            # 生成随机盐值
    salt = group.random(ZR)  
    sk = group.deserialize(sk)
    td = Hash1(salt_and_hash_keyword(w,salt)) ** sk
    return group.serialize(td)

def Test(td, c, param_id='SS512'):
    group = PairingGroup(param_id)
    c1 = group.deserialize(c[0])
    c2 = c[1]
    print("The value of c[1] is:", c2)
    td = group.deserialize(td)
    return Hash2(group.serialize(pair(td, c1))).hexdigest() == c2

if __name__ == '__main__':
    param_id = 'SS512'
    [sk, pk] = Setup(param_id)
    group = PairingGroup(param_id)
    
    td = TdGen(sk, "yes")
    c = Enc(pk, salt_and_hash_keyword("yes",salt))
    assert(Test(td, c))
    td = TdGen(sk, "no")
    c = Enc(pk, salt_and_hash_keyword("yes",salt))
    assert(not Test(td, c))
    c = Enc(pk, salt_and_hash_keyword("Su*re",salt))
    assert(not Test(td, c))
    c = Enc(pk, salt_and_hash_keyword("no",salt))
    assert(Test(td, c))

    td = TdGen(sk, str(9 ** 100))
    c = Enc(pk, salt_and_hash_keyword(str(9 ** 100),salt))
    assert(Test(td, c))
    td = TdGen(sk, str(9 ** 100 + 1))
    c = Enc(pk, salt_and_hash_keyword(str(9 ** 100),salt))
    assert(not Test(td, c)) 
