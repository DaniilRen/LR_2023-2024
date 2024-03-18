rgb = [i for i in input()]
numb = list(map(int, input().split()))

def sorted_rgb(s, nubers):
    result = []
    for i in 'rgb':
        for n, j in enumerate(s):
            if i == j:
                result.append(str(nubers[n]))
    return result

print(' '.join(sorted_rgb(rgb, numb)))
