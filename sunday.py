'''
    Naive Sunday implementation for searching matches in a string 
    Paper: Daniel M. Sunday. 1990. A very fast substring search algorithm. Commun. ACM 33, 8 (Aug. 1990), 132-142.
'''
def pre_process_sunday(p):
    m = len(p) 
    alphabet_lenght = 1024
    x = [m+1]*(alphabet_lenght) 
    for i in range(m):
        x[ord(p[i])] = m - i
    return x

def search_sunday(t,p):
    td = pre_process_sunday(p)
    n = len(t)
    m = len(p)
    k  = 0
    i = 0
    x = []
    while i < n - m:
        if t[i+k] != p[k]:
            k = 0
            i = i + td[ord(t[i+m])]
        else:
            k = k + 1
            if k == m:
                x.append(i)
                k = 0
                i = i + td[ord(t[i+m])]
    return x

if __name__ == "__main__":
    t = 'AIABBABABRQMYOAABBBBABABYOSGBBGTVBHABBABABSUJKSKKHKJABBABBABABABAYRQMYOIUHKJHJHSDASDASDNIAURTO ABBABABNLK'
    p = 'ABBABAB'
 
#    t = 'AIABBABABRQMYOAABBBBABABYOSGBBGTVBHABBABABSUJKSKKHKJABBABBABABABAYRQMYOIUHKJHJHSDASDASDNNLK'
#    p = 'ABBABAB'
    positions = search_sunday(t,p)
    for p in positions:
        print 'Pattern found at position = ' + str(p)



