x, y = 0, 0
cnt = 0

def bin_mul(a, b):
    a = bin(a)
    b = bin(b)
    if a[0] == '-':
        a = a[3:]
    else:
        a = a[2:]
    if b[0] == '-':
        b = b[3:]
    else:
        b = b[2:]
    return bin(int(a, 2) * int(b, 2))


for i in range(0, 2):
    for j in range(0, 65):
        x = 2**i - 1
        y = 2**j - 1
        print(x, y)
        if (x > y) and (('0' in bin_mul(x, y) or '1' in bin_mul(x, y))) and abs(bin_mul(x, y).count('0') - bin_mul(x, y).count('1') <= 13):
            cnt += 1
print(cnt)