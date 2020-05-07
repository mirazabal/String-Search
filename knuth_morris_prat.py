'''
    Naive knuth-Morris-Prat implementation for searching matches in a string 
    Based on finite-automata. Read CLRS for an introduction on finite automata.
    Of special interest if the alphabet is small i.e., x = {0,1} (bits), x = {a,b,c} ...
'''


# arr[q] = max{k | k < q and P_{k} is a suffix of P_{q}}
def kmp_prefix_func(p):
    m = len(p)
    arr = []
    arr.append(0)
    k = 0
    for i in range(1,m):
        # if the next character is different that p[k], go back to previous k seq. 
        # and look if that matches the new character.
        while k > 0 and p[k] != p[i]:
            k = arr[k-1]
        if p[k] == p[i]:
            k = k + 1
        print 'i = ' + str(i) + ' k = ' + str(k)
        arr.append(k) # this is equal to arr[i] = k
    return arr

def search_kmp(t,p):
    n = len(t)
    m = len(p)
    x = []
    arr = kmp_prefix_func(p)
    q = 0
    for i in range (0,n):
        while q > 0 and p[q] != t[i]:
            q = arr[q-1]
        if p[q] == t[i]:
            q = q + 1
        if q == m:
            x.append(i-(m-1) )
            q = arr[q-1]
            
    return x



if __name__ == "__main__":

    t = 'ABABACABAACABAABBBAABABACAAACABABACCAACABACACBACBABCBAACBACCBBAAACBBCACABABBACBBABA'
    p = 'ACABACA'
    positions = search_kmp(t,p)
    for p in positions:
        print 'Pattern found at position = ' + str(p)

