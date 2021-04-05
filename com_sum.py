
def combinationSum(candidates, target):
    """
    :type candidates: List[int]
    :type target: int
    :rtype: List[List[int]]
    """
    dict = {}
    i = 0
    output = []
    while target != 0:
        temp = target - candidates[i]
        if temp > 0:
            if dict[str(temp)]:
                target -= dict[temp]
                output.append(dict[temp])
            else:
                dict[str(temp)] = candidates[i]
                print(dict)

    print(output)

print(combinationSum([2,3,6,7],7))