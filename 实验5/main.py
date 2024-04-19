import secrets
import gmpy2
import pybloom_live
from Crypto.PublicKey import RSA

RSA_BITS = 1024
RSA_EXPONENT = 65537
RT_COUNT = 0
def generate_private_key(bits=RSA_BITS, e=RSA_EXPONENT):
    private_key = RSA.generate(bits=bits, e=e)   
    public_key = private_key.publickey()
    return private_key

def generate_random_factors(public_key):              
    random_factors = []
    rff = open('randomfactors.raw','w')
    for _ in range(RF_COUNT):
        r = secrets.randbelow(public_key.n)         
        r_inv = gmpy2.invert(r, public_key.n)       
        r_encrypted = gmpy2.powmod(r, public_key.e, public_key.n)    
        random_factors.append((r_inv, r_encrypted))
        rff.writelines(f"{r_inv.digits()}\n")

        rff.writelines(f"{r_encrypted.digits()}\n")
    rff.close()
    return random_factors

def blind_data(my_data_set, random_factors, n):          

    A = []
    bdf = open('blinddata.raw','w')
    for p, rf in zip(my_data_set, random_factors):
        r_encrypted = rf[1]
        blind_result = (p * r_encrypted) % n 
        A.append(blind_result)
        bdf.writelines(f"{blind_result.digits()}\n")
    bdf.close()
    return A

def setup_bloom_filter(private_key, data_set):
    mode = pybloom_live.ScalableBloomFilter.SMALL_SET_GROWTH
    bf = pybloom_live.ScalableBloomFilter(mode=mode)
    for q in data_set:
        sign = gmpy2.powmod(q, private_key.d, private_key.n)     
        bf.add(sign)                
    bff = open('bloomfilter.raw','wb')
    bf.tofile(bff)
    bff.close()
    return bf

def sign_blind_data(private_key, A):
    B = []
    sbdf = open('signedblinddata.raw','w')
    for a in A:
        sign = gmpy2.powmod(a, private_key.d, private_key.n)    #盲签名
        B.append(sign)
        sbdf.writelines(f"{sign.digits()}\n")
    sbdf.close()
    return B

def intersect(my_data_set, signed_blind_data, random_factors, bloom_filter, public_key):
    n = public_key.n
    result = []
    for p, b, rf in zip(my_data_set, signed_blind_data, random_factors):
        r_inv = rf[0]            
        to_check = (b * r_inv) % n
        if to_check in bloom_filter:    
            result.append(p)
    return result

if __name__ == '__main__':
	client_data_set = list(range(0, 1024, 249))
	server_data_set = list(range(0, 1024))
	RF_COUNT = len(client_data_set)
	private_key = generate_private_key()   
	public_key = private_key.public_key()
	random_factors = generate_random_factors(public_key)
	A = blind_data(client_data_set, random_factors, public_key.n)

	bf = setup_bloom_filter(private_key, server_data_set)

	B = sign_blind_data(private_key, A)
    
	result = intersect(client_data_set, B, random_factors, bf, public_key)
	print(result)
