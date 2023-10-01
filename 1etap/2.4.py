def main(n):
    z, x, y = 1, 1, 1
    cycle = 0
    for _ in range(1, n ** 2 + 1):
        if y > n:
            y -= n
        print(z, x, y)
        cycle += 1
        if cycle == n:
            cycle = 0
            z += 1
            x = 1
        else:
            x += 1
            y += 1


if __name__ == "__main__":
    main(int(input()))