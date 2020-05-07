'''
    Naive Rabin-Karp implementation for searching matches in a string 
    Two Rolling hash implementations 
    https://en.wikipedia.org/wiki/Rolling_hash
'''



class BuzHash():
    def __init__(self,s):
        first_time = True
        self.hash = 0
        self.k = len(s)
        i = 1
        x = 0

        for c in s:
            x = self.left_rotate(x,1)
            x = x ^ self.char_to_int(c)
        self.hash = x
        print 'buzhash val = ' + str(self.hash) + ' for str = ' + s


    def slide(self, previtm, nextitm):
        x = self.left_rotate(self.hash,1)
        z = self.left_rotate(self.char_to_int(previtm), self.k)
        x = x ^ z ^ self.char_to_int(nextitm)
        
        self.hash =  x 


    def char_to_int(self,c):
        #Naive implementation. Change for better hashing results
        return ord(c)

    #x is the number an n the positions t rotate, in our case, is one
    def left_rotate(self,x,n):
        # Supposing 64 bit machine
        return (x << n) | (x >> (64-n))


class PolyRollingHash(): #Polynomial rolling hash

    def __init__(self,s):
    # H = c_1*a^(k-1) + c_2*a^(k-2) + ... + c_k*a^0
    # shift left by multiplying by a
    # use a modulo aritmethic not to deal with very big integers
        self.a = 3037 # prime number
        self.n = 100003 # prime number
        self.hash = 0
        self.k = len(s) 
        for c in s:
            self.hash = self.hash * self.a   
            self.hash = self.hash + ord(c)
        self.hash = self.hash  % self.n


    def slide(self, previtm,nextitm):
        minus_val = ord(previtm) * (self.a ** (self.k-1)) 
        self.hash = ( (self.hash - minus_val ) * self.a) + ord(nextitm) 
        self.hash = self.hash % self.n
        return self.hash
        

def search_rabin_karp(t,p):
#    rh_p = PolyRollingHash(p)
    rh_p = BuzHash(p)
    rh_t = None

    n = len(p) 
    x = []
    t1 = ''
    pos = 0
    t_idx = 0
    nextitm = 'a'
    previtm = 'a'
    while pos + n < len(t):
        while len(t1) < n:
            t1 = t1 + t[t_idx]
            t_idx = t_idx + 1
        nextitm = t1[n-1]
        if rh_t == None:
#           rh_t = PolyRollingHash(t1)
           rh_t = BuzHash(t1)
        else:
           rh_t.slide(previtm,nextitm)
        
        if rh_p.hash == rh_t.hash:
            if p == t1:
                x.append(pos)

        previtm = t1[0]
        t1 = t1[1:]
        pos = pos + 1
    return x

if __name__ == "__main__":

    t = 'IRQMYOAABBSSCCDIORQMYOKJUUSKHHYRQMYOSGBBGTVBHSUJKSKKHKJYRQMYOIUHKJHJHSDASDASDNNLK'
    p = 'RQM'
    positions = search_rabin_karp(t,p)
    for p in positions:
        print 'Pattern found at position = ' + str(p)

