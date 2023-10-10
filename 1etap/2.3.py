def is_valid(s):
    last = s[1]
    for i in s:
        if i != last:
            last = i
            continue
        else:
            return False
    return True

def check(s, pieces):
    indexes = list(pieces.keys())
    output = []
    res = ''
    end_value_flag = False
    for k, v in pieces.items():
        # последний ли кусок?
        try:
            next_value = pieces[indexes[indexes.index(k)+1]][0]
        except IndexError:
            end_value_flag = True

        if end_value_flag: # если последний кусок
            if res[-1] == v[0]: # переворот
                res += v[::-1]
                output.append((*k, 180))
            else:
                res += v # просто добавляем в конец
                output.append((*k, 0))
        elif k[0] == 1: # если самый первый кусок
                res += v
                output.append((*k, 0))
        else: # в остальных случаях
            if res[0] != v[-1] and res[-1] == v[0] and v[-1] == next_value[0]: # меняем местами
                res = v + res
                output.insert(0, (*k, 0))
            elif res[-1] == v[0] and res[-1] == v[0] and v[-1] != next_value[0]: # переворот
                res += v[::-1]
                output.append((*k, 180))

    if len(res) == len(s) and is_valid(res): # если результат верный
        return [res, output]
    else:
        return ['no']

if __name__ == "__main__":
    s = input() # вводим строку
    pieces = {} # куски и их индексы

    last = 0
    start = 1
    for i in range(len(s)):
        if s[i] == s[last] and i != 0:
            pieces[(start, i)] = s[start-1:i]
            start = i+1
        last = i
        if i == len(s)-1:
            pieces[(start, i+1)] = s[start-1:i+1]

    result = check(s, pieces)
    if len(result) == 1:
        print(result[0])
    else:
        # print(result[0])
        for i in result[1]:
            print(*i)