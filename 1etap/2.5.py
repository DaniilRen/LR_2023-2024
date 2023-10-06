def correct(cor_s, s):
    s = list(s)
    cor_s = list(cor_s)
    vars = {}
    vars_cor = {}
    cnt = 3
    for i in s:
        if i not in '-=+*/()':
            vars[i] = str(cnt)
            cnt += 1
    for i in range(len(s)):
        if s[i] not in '-=+*/()':
            s[i] = vars[s[i]]
    for i in cor_s:
        if i not in '-=+*/()':
            vars_cor[i] = str(cnt)
            cnt += 1
    for i in range(len(cor_s)):
        if cor_s[i] not in '-=+*/()':
            cor_s[i] = vars_cor[cor_s[i]]
    return eval(''.join(s)) == eval(''.join(cor_s))



def main(s, i=0, bal=0, cor=''):
    print(s, i, bal)
    if not correct(cor, s) and bal == 0:
        return s
    if i == len(s) or s.count('(') == 0 and s.count(')') == 0:
        return s
    if s[i] == '(':
        s = s[:i] + s[i+1:]
        return main(s, i + 1, bal+1)
    elif s[i] == ')':
        s = s[:i] + s[i+1:]
        return main(s, i + 1, bal-1)
    else:
        return main(s, i+1, bal)


if __name__ == "__main__":
    s = input()
    if s[0] == '(' and s[-1] == ')':
        s = s[1:-1]
    print(main(s, 0, 0, s))
    # print(correct("(3+4+5)*6", "3+4+5*6"))