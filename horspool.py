'''
    Naive Horspool implementation for searching matches in a string 
    Paper: R.N. Horspool: Practical Fast Searching in Strings. Software - Practice and Experience 10, 501-506 (1980) 
'''

def pre_process_horspool(p):
    alphabet_lenght = 1024
    m = len(p)
    x = [m]*alphabet_lenght # if char not found, move m
    # the last character is not processed
    for i in range(m-1):
        x[ord(p[i])] = m - 1 - i
    return x

def search_horspool(t,p):
    x = []
    dic = pre_process_horspool(p)
    n = len(t)
    m = len(p)
    i = 0
    k = m - 1
    while i < n - m:
        while k > -1 and p[k] == t[i+k]:
            k = k - 1
        if k == -1:
            x.append(i)
        k = m - 1
        i = i + dic[ord(t[i+m-1])]

    return x

if __name__ == "__main__":

    t = 'AIABBABABRQMYOAABBBBABABYOSGBBGTVBHABBABABSUJKSKKHKJABBABBABABABAYRQMYOIUHKJHJHSDASDASDNIAURTO ABBABABNLK'
    p = 'ABBABAB'
    positions = search_horspool(t,p)
    for p in positions:
        print 'Pattern found at position = ' + str(p)


