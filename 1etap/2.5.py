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
    cnt = 3
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
    try:
        if eval(''.join(s)) == eval(''.join(cor_s)):
            return [True]
        else:
            return [False, eval(''.join(s)), eval(''.join(cor_s)), ''.join(s), ''.join(cor_s)]
    except SyntaxError:
        return [False, ''.join(s), ''.join(cor_s), "SyntaxError"]




def main(s, i=0, cor='', variations=[], last=''):
    print(s, i, variations, last)
    if s.count('(') == s.count(')'):
        is_correct = correct(cor, s)
        if not is_correct[0]:
            print("error:", is_correct)
            return s
        if s not in variations:
            variations.append(s)
    if i == len(s) or s.count('(') == 0 and s.count(')') == 0:
        print(f'max i: {(i, s)}')
        return s
    if s[i] == '(' or s[i] == ')':
        s = s[:i] + s[i+1:]
        return main(s, 0, cor, variations, s[i])

    # if s[i] == '(' and last == '(':
    #     return main(s, i + 1, cor, variations, '(')
    #
    # if s[i] == '(' and last != '(':
    #     s = s[:i] + s[i + 1:]
    #     return main(s, 0, cor, variations, '(')
    #
    # if s[i] == ')' and last == ')':
    #     return main(s, i + 1, cor, variations, ')')
    #
    # if s[i] == ')' and last != ')':
    #     s = s[:i] + s[i + 1:]
    #     return main(s, 0, cor, variations, ')')

    else:
        return main(s, i + 1, cor, variations, last)


if __name__ == "__main__":
    s = input()
    if s[0] == '(' and s[-1] == ')':
        s = s[1:-1]
    print(main(s, 0, s))