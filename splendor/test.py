def nthUglyNum(n):
    all_set = [1]
    num2 = 0
    num3 = 0
    num5 = 0
    while len(all_set) < n:
        min_element = min(2 * all_set[num2], 3 * all_set[num3], 5 * all_set[num5])
        if min_element == 2 * all_set[num2]:
            num2 += 1
        elif min_element == 3 * all_set[num3]:
            num3 += 1
        else:
            num5 += 1
        all_set.append(min_element)
        all_set = list(set(all_set))
    return all_set

n = 10
nthUglyNum(n)

