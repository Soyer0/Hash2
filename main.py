import hashlib
import secrets


def random_bit_vector(n):
    return secrets.token_bytes(n//8)


def R(x):
    x = x.encode() if not isinstance(x, bytes) else x
    r = secrets.token_bytes(12)  # len = 128 - n bits, n = 32
    return r + x


def hash_sha384(bytes_data):
    hash_object = hashlib.sha384()
    hash_object.update(bytes_data)
    return hash_object.hexdigest()


def alg1(K, L):
    table = {}
    for i in range(K):
        x_i0 = random_bit_vector(32)
        x_ij = x_i0
        for _ in range(L):
            x_ij = hash_sha384(R(x_ij))
        table[x_i0.hex()] = x_ij
    return table



def alg2_(table, L):
    y = hash_sha384(random_bit_vector(256))
    global x
    for _ in range(L):
        for key, value in table.items():
            if value == y:
                return key
            y = hash_sha384(R(y))

    return "Прообраз не знайдено"


def alg2(table, L):
    x = alg2_(table, L)
    if x == "Прообраз не знайдено":
        return "Прообраз не знайдено"
    for m in range(L):
        x = hash_sha384(R(x))
    return R(x)


success = 0
K = 2 ** 11 # Потім для інших степенів
L = 2 ** 6
N = 10000

for _ in range(N):
    table = alg1(K, L)
    result = alg2(table, L)
    if result != "Прообраз не знайдено":
        success += 1
        print("Знайдено прообраз!!!")
print(f"Відсоток успішних знаходжень прообразів для K={K}, L={L} дорівнює {success / N}")

def predict_probability_by_hellmann_theorem(K, L):
    n = 2**32

    sum_val = 0
    for i in range(1, K + 1):
        for j in range(L):
            sum_val += (1 - (i * L) / n) ** (j + 1)

    sum_val /= n
    return sum_val

print(f"Оцінка за теоремою Хеллмана: {predict_probability_by_hellmann_theorem(K,L)}")
