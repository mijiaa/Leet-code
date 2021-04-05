
def valid_palindromic_sub_string(string):
    all_string= set()
    for i in range(len(string)):
        temp = string[i]
        for j in range(1+i,len(string)):
            temp += string[j]
            all_string.add(temp)

    max_len = 0
    longest_str= ""
    for string in all_string:
        print(string)
        if valid_palindromic(string):
            if len(string) > max_len:
                max_len = len(string)
                longest_str = string
    return longest_str

def valid_palindromic(str):
    ptr=len(str)-1

    for i in range(len(str)//2):
        if str[i]!= str[ptr]:
            return False
        else:
            ptr -=1
    return True

print(valid_palindromic_sub_string("banana"))