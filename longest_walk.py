def longest_oscillation(L):
    """
    Find the longest oscillation in a given list.
    :Implementation : OPTIMAL
    :param L: A list of integers. Can contain duplicates or be empty
    :time complexity : O(N) time where N is the length of list L
    :auxiliary space complexity : O(N) where N is the length of the list L
    :return: a tuple, where the first element is a number to represent the length of the oscillation.
             The second element is a list of indices of the elements in L which make up the oscillation.
    """
    n = len(L)

    # deal with empty list
    if n is 0:
        return (0, [])

    prev_sign = '' # store whether previous num is negative or positive
    length = 1
    index = []

    for i in range(1, n):
        # find the difference between current element (L[i-1]) and next element (L[i])
        # if the difference of two element alternates between positive and negative continuously,
        # that means its 'oscillating'.
        if L[i] - L[i - 1] != 0:
            sign = find_sign(L[i] - L[i - 1])
            # store current sign for comparision for next iteration and increase length of longest by 1
            # store index of current element because its path of longest oscillation
            if sign != prev_sign:
                prev_sign= sign
                length += 1
                index.append(i - 1)

    index.append(n - 1) # last element can always be part of the longest oscillation sequence
    return (length, index)


def find_sign(num):
    """
    find whether the difference of two elements are positive or negative
    :param num: difference of two elements
    :return: boolean. True for positive number, False for negative number
    :complexity : O(1) time
    """
    if num > 0:
        return True
    return False


def longest_walk(M):
    """
    This function finds the longest increasing walk in the given matrix.
    :implementation : OPTIMAL
    :param M: a list of n lists, with each inner list being length m, and containing only integers.
    :Time complexity : O(nm) where n is the length of matrix and m is the length of inner list of the Matrix
    :Auxiliary space complexity : O(nm) where n is the length of matrix and m is the length of inner list of the Matrix
    :return:tuple, first element is a number to represent the length of the longest increasing walk in M
            and second element is a list of the co-ordinates of the elements in that walk, in order.
    """
    if M == []:
        return (0,[])
    n = len(M)
    m = len(M[0])
    dp = [[-1 for i in range(m)] for i in range(n)] # memo table
    result = -1 # store length of the longest increasing walk
    coord = 0  # store the starting point of the longest increasing walk for backtracking
    for i in range(n):
        for j in range(m):
            if dp[i][j] == -1:
                longest_temp = find_path(dp, M, n, m, i, j)
            else:
                longest_temp = dp[i][j]

            if result < longest_temp:
                result = longest_temp
                coord = (i, j) #
            else:
                result = max(result, longest_temp)

    # initialise by including starting point
    index_lst = [coord]

    # backtrack to find the co-ordinates of the elements in that walk using memo table (dp) obtained above
    index_lst = find_index(M, dp, n, m, coord[0], coord[1], index_lst)
    return (result,index_lst)


def find_index(M, dp, n, m, i, j, index_lst):
    """
    This function backtracks using memoization table obtained from previously function.
    input (i,j) is the coordinate of the starting point of the longest walk.
    This coordinate is used to find the next coordinate (its surrounding) that has a -1 difference in the dp table.
    The function then change the compared value (the starting point...) to -1 and recurse to the next coordinate and so on
    until the lowest value in dp table.

    :param M: is a list of n lists, with each inner list being length m, and containing only integers.
    :param dp: memoization table
    :param n: length of Matrix
    :param m: length of inner list of Matrix
    :param i: i coordinate of origin of longest increasing walk
    :param j: j coordinate of origin of longest increasing walk
    :param index_lst: list of indexes
    :complexity : O(N) where N is the length of the longest walk
    :return: list of indexes that form the longest walk
    """

    # every if statments checks if the difference in memo table of current value and next value is 1
    # and if the value in the matrix of the next coordinate is bigger than current value

    # check bottom cell and within boundary
    if (i + 1 < n and i + 1 >= 0) and  dp[i][j] - dp[i + 1][j] == 1 and M[i][j] < M[i + 1][j]:
        dp[i][j] = -1
        index_lst.append((i + 1, j))
        find_index(M, dp, n, m, i + 1, j, index_lst)

    # check top cell and within boundary
    if (i - 1 < n and i - 1 >= 0 and dp[i][j] - dp[i - 1][j] == 1 and M[i][j] < M[i - 1][j]):
        index_lst.append((i - 1, j))
        dp[i][j] = -1
        find_index(M, dp, n, m, i - 1, j, index_lst)

    # check right cell and within boundary
    if (j + 1 < m and j + 1 >= 0 and dp[i][j] - dp[i][j+1] == 1 and M[i][j] < M[i][j+1]):
        dp[i][j] = -1
        index_lst.append((i , j + 1))
        find_index(M, dp, n, m, i, j + 1, index_lst)

    # check left cell and within boundary
    if (j - 1 < m and j - 1 >= 0 and dp[i][j] - dp[i][j-1] == 1 and M[i][j] < M[i][j-1]):
        dp[i][j] = -1
        index_lst.append((i, j - 1))
        find_index(M, dp, n, m, i, j - 1, index_lst)

    # check bottom right cell and within boundary
    if (j + 1 < m and i + 1 < n and j + 1 >= 0 and i + 1 >= 0 and dp[i][j] - dp[i+1][j+1] == 1 and  M[i][j] < M[i+1][j+1]):
        dp[i][j] = -1
        index_lst.append((i + 1, j + 1))
        find_index(M, dp, n, m, i + 1, j + 1, index_lst)

    # check top left cell and within boundary
    if (j - 1 < m and i - 1 < n and j - 1 >= 0 and i - 1 >= 0 and dp[i][j] - dp[i - 1][j-1] == 1 and  M[i][j] < M[i - 1][j-1]):
        dp[i][j] = -1
        index_lst.append((i - 1, j - 1))
        find_index(M, dp, n, m, i - 1, j - 1, index_lst)

    # check top right cell and within boundary
    if (j + 1 < m and i - 1 < n and j + 1 >= 0 and i - 1 >= 0 and dp[i][j] - dp[i - 1][j+1] == 1 and M[i][j] < M[i - 1][j+1] ):
        dp[i][j] = -1
        index_lst.append((i - 1, j + 1))
        find_index(M, dp, n, m, i - 1, j + 1, index_lst)

    # check bottom left cell and within boundary
    if (j - 1 < m and i + 1 < n and j - 1 >= 0 and i + 1 >= 0 and dp[i][j] - dp[i +1][j-1] == 1 and M[i][j] - M[i +1][j-1]):
        dp[i][j] = -1
        index_lst.append((i + 1, j - 1))
        find_index(M, dp, n, m, i + 1, j - 1, index_lst)

    return index_lst


def find_path(dp, M, n, m, i, j):
    """
    This function finds the longest increasing walk of a given coordinate (i,j) and store the result in the dp table so
    that the result can be reused for overlapping sub-problems. This also ensures that function runs in O(nm) time
    complexity.
    :param dp: memoization table
    :param M: is a list of n lists, with each inner list being length m, and containing only integers.
    :param n: length of Matrix
    :param m: length of inner list of Matrix
    :param i: current row of matrix
    :param j: current column of matrix

    :Time complexity : O(nm)
    :return: length of the longest increasing walk in M, integer

    """
    # check if current coordinate is an overlapping sub-problems
    if (dp[i][j] != -1):
        return dp[i][j]

    #initialise to 1 to include starting point
    result = 1

    # every If statement checks if current coordinate is part of any overlapping sub problems
    # and if value of the next coordinate in matrix is bigger than current value in matrix

    # check bottom cell and within boundary
    if i + 1 < n and i + 1 >= 0 and M[i][j] < M[i + 1][j]:
        if dp[i + 1][j]!= -1:
            result = max(result, 1 + dp[i + 1][j])
        else:
            result = max(result, 1 + find_path(dp, M, n, m, i + 1, j))

    # check top cell and within boundary
    if i - 1 < n and i - 1 >= 0  and M[i][j] < M[i - 1][j]:
        if dp[i - 1][j]  != -1:
            result = max(result, 1 + dp[i - 1][j])
        else:
            result = max(result, 1 + find_path(dp, M, n, m, i - 1, j))

    # check right cell and within boundary
    if j + 1 < m and j + 1 >= 0 and M[i][j] < M[i][j + 1]:
        if dp[i][j + 1]  != -1:
            result = max(result, 1 + dp[i][j + 1])
        else:
            result = max(result, 1 + find_path(dp, M, n, m, i, j + 1))

    # check left cell and within boundary
    if j - 1 < m and j - 1 >= 0  and M[i][j] < M[i][j - 1]:
        if dp[i][j - 1]  != -1:
            result = max(result, 1 + dp[i][j - 1])
        else:
            result = max(result, 1 + find_path(dp, M, n, m, i, j - 1))

    # check bottom right cell and within boundary
    if j + 1 < m and i + 1 < n and j + 1 >= 0 and i + 1 >= 0 and M[i][j] < M[i + 1][j + 1]:
        if dp[i + 1][j + 1]  != -1:
            result = max(result, 1 + dp[i + 1][j + 1])
        else:
            result = max(result, 1 + find_path(dp, M, n, m, i + 1, j + 1))

    # check top left cell and within boundary
    if j - 1 < m and i - 1 < n and j - 1 >= 0 and i - 1 >= 0 and M[i][j] < M[i - 1][j - 1]:
        if dp[i - 1][j - 1]  != -1:
            result = max(result, 1 + dp[i - 1][j - 1])
        else:
            result = max(result, 1 + find_path(dp, M, n, m, i - 1, j - 1))

    # check top right cell and within boundary
    if j + 1 < m and i - 1 < n and j + 1 >= 0 and i - 1 >= 0  and M[i][j] < M[i - 1][j + 1]:
        if dp[i - 1][j + 1]  != -1:
            result = max(result, 1 + dp[i - 1][j + 1])
        else:
            result = max(result, 1 + find_path(dp, M, n, m, i - 1, j + 1))

    # check bottom left cell and within boundry
    if j - 1 < m and i + 1 < n and j - 1 >= 0 and i + 1 >= 0 and M[i][j] < M[i + 1][j - 1]:
        if dp[i + 1][j - 1] != -1:
            result = max(result, 1 + dp[i + 1][j - 1])
        else:
            result = max(result, 1 + find_path(dp, M, n, m, i + 1, j - 1))

    # store sub-problem result in memo table
    dp[i][j] = result

    return dp[i][j]

