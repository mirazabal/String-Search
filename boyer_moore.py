'''
    Naive Boyer-Moore implementation for searching matches in a string 
    Paper: R.S. Boyer, J.S. Moore: A Fast String Searching Algorithm. Communications of the ACM, 20, 10, 762-772 (1977)
'''


'''
    Rightmost occurrence of character
    Known as Bad character Heuristic
'''
import pdb

def pre_process_delta_1(p):
    alphabet_lenght = 1024
    x = [-1]*alphabet_lenght
    m = len(p)
    for i in range(m):
        x[ord(p[i])] = i
    return x


'''
    Known as Good Suffix Heuristics 
'''
def pre_process_delta_2(p):
    m = len(p)
    assert m > 1
    i = m 
    k = m + 1
    shift = [0] * (m+1)
    pattern = [0] * (m+1)
    pattern[i] = k
    while i > 0:
        while k < m + 1 and p[i-1] != p[k-1]:
            if shift[k] == 0:
                shift[k] = k - i  
            k = pattern[k] # search for patterns given before in the string 
        k = k - 1
        i = i - 1
        pattern[i] = k


    k = pattern[0]
    for i in range(m+1):
        if shift[i] == 0:
            shift[i] = k
        if k == i:
            k = pattern[k]
    return shift

def search_boyer_moore(t,p):
    x = []
    delta_1 = pre_process_delta_1(p)
    delta_2 = pre_process_delta_2(p)

    m = len(p)
    n = len(t)
    i = m - 1
    k = m - 1 
    while i < n:
        if t[i] != p[k]:
            shift1 = m - 1 - delta_1[ord(t[i])] # find next occurrence of the missed char
            shift2 = m - k # maybe we advanced in the pattern more than the next occurrence 
            shift3 = delta_2[k+1] # Look if the pattern seen so far is repeated in the string
            shift = max(shift3, max(shift1,shift2))
            i = i + shift
            k = m - 1
        else:
            if k == 0:
                k = m - 1
                x.append(i)
                i = i + m
            else :
                k = k - 1
                i = i - 1
    return x

if __name__ == "__main__":

    t = 'AIABBABABRQMYOAABBBBABABYOSGBBGTVBHABBABABSUJKSKKHKJABBABBABABABAYRQMYOIUHKJHJHSDASDASDNNLK'
    p = 'ABBABAB'
    positions = search_boyer_moore(t,p)
    for p in positions:
        print 'Pattern found at position = ' + str(p)

