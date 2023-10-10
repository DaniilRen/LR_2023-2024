a = input()
c = []
opt = 0


def opetgr(s, i, j):
    shi = s[:i] + s[i:j].replace('+', '@') + s[j:]
    return shi

def removea(s, i, j):
    i_2 = i
    j_2 = j
    if i != 0:
        i_2 = i - 1
    if j != len(s) - 1:
        j_2 = j + 1
    s_obr = s[i_2:j_2]
    if '+' in s_obr[1:-1]:
        flag = False
        s = opetgr(s, i, j)
    else:
        flag = True
    if s[i_2] != '*' and s[j_2] != '*':
        if len(s) - 1 == j:
            s = s[:j]
        else:
            s = s[:j] + s[j + 1:]
        s = s[:i] + s[i + 1:]
        return s, 2
    elif (s[i_2] == '*' or s[j_2] == '*') and flag:
        if len(s) - 1 == j:
            s = s[:j]
        else:
            s = s[:j] + s[j + 1:]
        s = s[:i] + s[i + 1:]
        return s, 2
    return s, 0


for n, i in enumerate(a):
    n -= opt
    if i == ')':
        a, opt1 = removea(a, c[-1], n)
        c.pop()
        opt += opt1
    if i == '(':
        c.append(n)


print(a.replace('@', '+'))
