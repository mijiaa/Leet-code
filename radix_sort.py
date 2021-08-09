import math
import random
import timeit
import matplotlib.pyplot as plt
import csv

def radix_sort(num_lst, b):
    """
    This function is used to sort a list without comparison method. Can be optimised using an appropriate base value (b).
    base values determines number of counting sort will run
    :param num_lst: a list containing positive integers, the range is 1 to 2^64 - 1).
    :param b: base
    :return: sorted list
    """
    # find maximum number in list
    max = 0
    try :
        for i in range(len(num_lst)):
            if num_lst[i] > max:
                max = num_lst[i]
    except:
        for i in range(len(num_lst)):
            if num_lst[i][0] > max:
                max = num_lst[i][0]

    # deal with empty list
    if num_lst == []:
        return []
    represent = math.log(max,b) # find representation of max number using base
    num_of_digits = math.ceil(represent) # digits of a number have in base b

    #Use stable sort to sort them on the k th digit
    for i in range(num_of_digits):
        if type(num_lst[0]) == int: # for only list of values
            counting_sort(num_lst,b,i) # call counting sorts until sorted
        else: # for list of key-value pairs
            counting_sort_index(num_lst,b,i)
    return num_lst

def counting_sort(num_lst,base,digit):
    """
    radix sort need a stable sorting algorithm to sort the list of integers of k-th digits. so counting sort is chosen.
    This function is inspired from lecture slides with modifications to allow usage of base.
    This function sort list without comparison.
    only for TASK 1
    :param num_lst: list of positive integers
    :param base: base
    :param digit: place value
    :complexity : O(N) where N is the length of input list
    :return:
    """
    n = len(num_lst)
    # initialise counter list with base
    counter = [0 for i in range(base)]

    # for each value in input list, store count of each element at their respective indexes
    for i in range(n):
        key = (num_lst[i]//base**digit)%base
        counter[key] += 1

    # calculate the cumulative sum
    for j in range(1,len(counter)):
        counter[j] += counter[j-1]

    result = [ 0 for i in range(n)]

    # construct output
    for k in range(n-1,-1,-1):
        # calculate key to point to position in counter list
        key = (num_lst[k]//base**digit)%base
        # set output[position[key] - 1] to the val from input
        result[counter[key] -1] = num_lst[k]
        # decrement counter
        counter[key] -=1

    for i in range(n):
        num_lst[i] = result[i]

def counting_sort_index(num_lst,base,digit):
    """
    This counting sort is for TASK 3 as it take into account of position of original elements in string_list
    :param num_lst: list of positive integers
    :param base: base
    :param digit: place value
    :complexity : O(N) where N is the length of input list
    """
    m = len(num_lst)
    counter = [0 for i in range(base)]

    # store count of each element at their indexes
    for i in range(m):
        place = (num_lst[i][0]//base**digit)%base
        counter[place] += 1

    # calculate the cumulative sum
    for j in range(1,base):
        counter[j] += counter[j-1]
    result = [ 0 for i in range(m)]

    # Find the index of each element of the original array in count array. This gives the cumulative count.
    # Place the element at the index calculated.
    for k in range(m-1,-1,-1):
        place = (num_lst[k][0]//base**digit)%base
        result[counter[place] -1] = num_lst[k]
        counter[place] -=1

    for i in range(m):
        num_lst[i] = result[i]

# task 2
def time_radix_sort():
    """
    This function is created to analyse the time taken to run radix sort using varying bases. it
    will call radix_sort with different bases and record the times.
    :return: list of tuples of base used and time taken to sort
    """
    test_data = [random.randint(1, (2 ** 64) - 1) for _ in range(100000)]
    # bases = [2,5,10,1000,10000,100000,100001,300000,300555, 500300, 500333]
    bases = [2,3, 4,5, 8,9, 16,17, 32,33, 64, 65, 2**7,2**7 +1, 2**8,2**8 +1]
    #bases = [3, 9, 27, 81, 243, 3**6, 3 ** 7]

    time_lst=[]

    f = open('output_task2.csv', 'w+')
    for i in range(len(bases)):
        start_time = timeit.default_timer()
        radix_sort(test_data,bases[i])
        total_time = timeit.default_timer() - start_time
        f.write("%d, %f" % (bases[i],total_time))
        f.write("\n")
        time_lst.append((bases[i],total_time))
    return time_lst

print(time_radix_sort())

# task 3
def find_rotations(string_list, p):
    """
    find all the strings in the list whose p-rotations also appear in the list.
    :param string_list: list of strings
    :param p: number of left rotations
    :return: list of rotated string which appears in the original list
    """
    n = len(string_list)
    ori_lst = [' ' for i in range(n)]

    # store original positions of elements in list as index
    for i in range(n):
        string_list[i] = (string_list[i],i)

    # copy original list before changes
    for i in range(n):
        ori_lst[i] = string_list[i]

    copy_lst = [' ' for i in range(n)]
    output = []

    # break each string to list of alphabets
    for i in range(n):
        temp,temp_index = string_list[i]
        temp = list(string_list[i][0])
        string_list[i] = (temp,temp_index)

    # store a backup list to compare
    for i in range(n):
        temp, temp_index = string_list[i]
        copy_lst[i] = (temp,temp_index)


    rotated_lst = rotate(string_list, p) # rotate list
    rotated_lst = toString(rotated_lst) # change list to list of string
    rotated_lst = toAscii(rotated_lst) # change list to list of ascii values

    copy_lst = toAscii(copy_lst)

    #combine two lists
    for i in range(n):
        rotated_lst.append(copy_lst[i])

    #sort combined list
    rotated_sorted_lst = radix_sort(rotated_lst, 10)

    # check common elements and add to output
    for i in range(len(rotated_sorted_lst)-1):
        left_element = rotated_sorted_lst[i]
        right_element= rotated_sorted_lst[i+1]

        if left_element[0] == right_element[0]:
            # find index from rotated list to point to element in the original list
            index = rotated_lst[i][1]
            output.append(ori_lst[index][0])

    return output


def rotate(string_list, p):
    """
    rotate strings by p-rotation
    :param string_list: list of strings
    :param p: left rotations
    :complexity : O(NM) where N is the number of strings in the input list and
                  M is the maximum number of letters in a word, among all words in the input list.
    :return: list of rotated strings
    """
    rotated_lst = []
    n = len(string_list)

    for i in range(n):
        string_ = string_list[i]
        m = len(string_[0])
        num_of_rot = p

        # use mod operation to generalise p-rotations when p > length of string
        if p > m:
            num_of_rot = p % m

        if p < 0 and abs(p) > m:
            num_of_rot = -(abs(p)%m)
            string = right_rotation(string_,num_of_rot)
        elif p < 0 :
            string = right_rotation(string_, num_of_rot)
        else:
            string = left_rotation(string_, num_of_rot)

        rotated_lst.append(string)

    return rotated_lst

def left_rotation(string,p):
    """
    This function perform left rotation on string
    :param string: input string to be rotated
    :param p: number of rotation
    :complexity : O(M) M is the maximum number of letters in a word
    :return: rotated string
    """
    element, temp_index = string
    temp = element[p:]
    string = (temp + element[:p], temp_index)

    return string

def right_rotation(string,p):
    """
    This function perform right rotation on string
    :param string: input string to be rotated
    :param p: number of rotation
    :complexity : O(M) M is the maximum number of letters in a word
    :return: rotated string
    """
    element, temp_index = string
    temp = element[:p+len(element)]
    string = (element[p+len(element):len(element)] + temp, temp_index)

    return string


def toAscii(string_list):
    """
    convert a list of strings to its list of Ascii values
    :param string_list: list of string
    :complexity : O(NM) where N is the number of strings in the input list and
                  M is the maximum number of letters in a word, among all words in the input list.
    :return:
    """
    n = len(string_list)
    for i in range(n):
        temp, temp_index = string_list[i]
        string_list[i] = [str(ord(char)) for char in temp]
        string_list[i] = (int(''.join(string_list[i])),temp_index)

    return string_list


def toString(string_list):
    """
    convert a list of integers to its list of strings
    :param string_list: list of string
    :complexity : O(NM) where N is the number of strings in the input list and
                  M is the maximum number of letters in a word, among all words in the input list.
    :return:
    """
    n = len(string_list)
    for i in range(n):
        temp,temp_index = string_list[i]
        string_list[i] = (''.join(map(str, temp)),temp_index)
    return string_list

#-------------------------- for plotting
def plot_csv_time(csv_file):
    time, bases = [],[]
    with open(csv_file,'r') as csv_file:
        plots = csv.reader(csv_file, delimiter=',')
        print(plots)
        for row in plots:
            bases.append(row[0])
            time.append(float(row[1]))
    plt.plot(bases,time,color='b')
    plt.ylabel('Time')
    plt.xlabel('Bases')

    plt.tight_layout()
    plt.show()

plot_csv_time('output_task2.csv')
# print(radix_sort([4,3,2,1],10))
# print(radix_sort([127483,1235,1241,1,34,3,545452,12343,521,5323],10))




