n, m = int(input()), int(input())
r = 0;
flag=True
while (flag):
    if n != m:
        r += 1
        if n < m:
            n += 3
        elif m < n:
            m += 7
    else:
        flag=False
        print(r)