'''
    Naive Two way String-Matching implementation for searching matches in a string 
    Paper: Maxime Crochemore and Dominique Perrin, 1991. Two-way string-matching. J. ACM 38, 3 (July 1991), 650-674
'''


def pre_process_max_suffix(p):
    n = len(p)
    ms = -1
    j = 0
    k = 1
    pos = 1
    while j + k < n:
        a = p[ms+k]
        b = p[j+k]
        if(ord(b) < ord(a)):
           j = j + k
           k = 1
           pos = j-ms
        elif (ord(b) == ord(a)):
            if k == pos:
                j = j + pos
                k = 1
            else:
                k = k +1 
        else: #(ord(b) > ord(a)):
            ms = j
            j = ms + 1
            k = 1
            pos = 1
    return ms,pos

def pre_process_max_suffix_tilde(p):
    n = len(p)
    ms = -1
    j = 0
    k = 1
    pos = 1
    while j + k < n:
        a = p[j+k]
        b = p[ms+k]
        if(ord(b) < ord(a)):
           j = j + k
           k = 1
           pos = j-ms
        elif (ord(b) == ord(a)):
            if k == pos:
                j = j + pos
                k = 1
            else:
                k = k +1 
        else: #(ord(b) > ord(a)):
            ms = j
            j = ms + 1
            k = 1
            pos = 1
    return ms,pos

'''
    Critical factorization, we divide the string X in X_l and X_r.
    where the period and the local period converge.
    period => x[i] = x[i+p]
    local period => How much do I have to enlarge a string from a position so that X_l equal X_r
    or a part of it e.g., AB AB 
                            2 -> since AB == AB
                          ABC DEF
                             6 -> since  (DEF)ABC == DEF(ABC)
    l, is the index of the last char of X_l e.g., page 656 at the ACM paper
                G C A G A G A G
Local Period:    3 7 7 2 2 2 2
Period : 7
l = 1
X_l = GC ; X_r = AGAGAG
or
X_l = GCA ; X_r = GAGAG

                A M A Z O N I 
Local Period:    2 7 7 7 7 7 
Period : 7
l = 1
X_l = AM ; X_r = AZONI
or
X_l = AMA ; X_r = ZONI
or
X_l = AMAZ ; X_r = ONI

As we are using max suffix, X_l = AMA, X_r = ZONI

                A B A A B A A
Local Period:    2 3 1 3 3 1
Period : 3
l = 1
X_l = AB; X_r = AABAA

'''

def critical_factorization(p):
    l_1,p_1 = pre_process_max_suffix(p)
    l_2,p_2 = pre_process_max_suffix_tilde(p)

    if(l_1 >= l_2):
        return l_1,p_1
    else:
        return l_2,p_2


def search_two_way(t, pattern):
    n = len(pattern)
    l, p = critical_factorization(pattern) 
    s1 = pattern[0:l+1]
    s2 = pattern[l+1:l+p+1]
    is_suffix = s2.endswith(s1);
    P = []
    if l < n/2 and is_suffix: 
        pos = 0
        s = -1
        while pos + n <= len(t):
            i = max(l,s) + 1 # get the index of X_r
            while i < n and pattern[i] == t [pos + i]:
                i = i + 1
            if i < n:
                pos = pos + max(i-l,s-p+1)
                s = -1
            else: # check the left part of the word
                j = l
                while j > s and pattern[j] == t[pos+j]:
                    j = j -1
                if j <= s:
                   P.append(pos)
                pos = pos + p
                s = n - p - 1
        return P
    else:
        q = max(l, n-l) + 1
        pos = 0
        while pos + n <= len(t):
            i = l+1
            while i < n and pattern[i] == t[pos + i]:
                i = i + 1
            if i < n:
                pos = pos + i - l
            else:
                j = l
                while j > -1 and pattern[j] == t[pos+j]:
                    j = j -1
                if j == -1:
                    P.append(pos)
                pos = pos + q
        return P

if __name__ == "__main__":
    p = 'GCAGAGAG'
    #p = 'ABAABAA'
    #p = 'AMAZONIA'
    #p = 'AAA' 

    #t = 'AAAMAZONIAAIABBABABRQMYOAABBBBABABYOSGBBGTVBHABBABABSUJKSKKHKJAMAZONZONABBAMAZONIAABBABABABAYAMAZONIARQMYOIUHKJHJHSDASDASDNIAURTOAMAZONIAAABBABABNLK'
    #t = 'AAADERFTYAAAHSWEEAAA' 
    t = 'AIABBABABRQMYOAABBBBABABYOSGBBGTVBHGCAGAGAGABBABABSUJKSKKHKJABBABBABABABAYRQMYOIUHKJHJHSDASDASDNNLK'
    positions = search_two_way(t,p)
    for p in positions:
        print 'Pattern found at position = ' + str(p)

