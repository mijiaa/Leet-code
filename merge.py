def merge(lst,lst2):
    n = len(lst)
    m = len(lst2)
    new_lst = []
    i,j = 0,0

    # for equal lenght
    while i <n and j < m:
        if lst[i] < lst2[j]:
            new_lst.append(lst[i])
            i +=1
        else:
            new_lst.append(lst2[j])
            j+=1

    for x in range(i,n):
        new_lst.append(lst[x])

    for y in range(j,m):
        new_lst.append(lst2[y])

    return new_lst

# print(merge([1,3,5],[4,5,6,7,8]))

def merge_sort(lst):

    if len(lst) == 1:
        return lst

    lst1 = lst[:len(lst)//2]

    lst2 = lst[len(lst)//2 :]

    lst1 =merge_sort(lst1)
    lst2 = merge_sort(lst2)

    sorted_lst = merge(lst1,lst2)
    return sorted_lst

