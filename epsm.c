/*
    Naive EPSMa implementation for searching matches in a string 
    Paper: Faro, Simone & Külekci, M.. (2012). Fast Packed String Matching for Short Patterns. Proceedings of the Workshop on Algorithm Engineering and Experiments. 10.1137/1.9781611972931.10. 
    Check this website for details: http://www.dmi.unict.it/~faro/smart/algorithms.php
*/
#include <assert.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <memory.h>
#include <smmintrin.h>
#include <inttypes.h>

typedef union{ 
  __m128i  v; 
  unsigned char uc[16]; 
} B; 

static 
B** pre_process(const char* p, uint32_t m_1, uint32_t alpha)
{
 B** b =  malloc(sizeof(B*)*m_1);
  assert(b != NULL);
  for(int i = 0; i < m_1; ++i){
    b[i] = malloc(sizeof(B)*alpha); 
    assert(b[i] != NULL);
  }
  // Preprocessing
  for(int i = 0; i < m_1; ++i){
    for(int j = 0; j < alpha; ++j){
      b[i]->uc[j] = p[i]; 
    } 
  }
  return b;
}

static
void free_pre_process(B** b, uint32_t m_1)
{
  for(int i = 0; i < m_1; ++i){
    free(b[i]); 
  }
  free(b);
}

static
uint16_t reverse_bits(uint16_t val){
  uint16_t rv = 0;
  for(int i = 0; i < 16; ++i){
    rv <<= 1;
    rv |=  val & 0x01;  
    val = val >> 1;
  }
  assert(val == 0);
  return rv;
}
static
uint32_t lshift_fill_ones(uint32_t w, uint32_t pos)
{
  assert(pos < 32);
  uint32_t mask_fill_ones = w << pos;
  mask_fill_ones |= ((uint32_t)1 << pos) - 1; 
  return mask_fill_ones; 
}

void epsm_a(const char* p, int m, const char* x, int n)
{
  const int alpha = sizeof(__m128i);
  assert(m < alpha);
  __m128i* t = (__m128i*)x; 

  const int m_1 = m; 

  B** b = pre_process(p, m_1, alpha); 

  uint32_t carry_new = 0;
  uint32_t carry_old = 0;

  const uint16_t mask = ((uint16_t)1 << (m_1 -1) ) - 1; 
  // check the string in 16 bytes blocks
  int i = 0;
  for( ; i < n/alpha; ++i){
    carry_old = carry_new;
    carry_new = mask;
    uint64_t r = -1; // same effect as 0xFFFFFFFFFFFFFFFF;
    for(int j = 0; j < m_1; ++j){
      // If a pair of data elements is equal, the corresponding data element in the destination operand is set to all 1s; otherwise, it is set to all 0s. Remember that in gdb the number will be inverted
      __m128i h = _mm_cmpeq_epi8(t[i], b[j]->v); 
        // Creates a mask made up of the most significant bit of each byte of the source operand (second operand) and stores the result in the low byte or word of the destination operand (first operand). (i.e., for a 128 bit, it generates a 16 bit with the most significant bit of every byte)
      uint32_t s = _mm_movemask_epi8(h);
      if(j < m_1 - 1 && carry_new != 0){
        const uint16_t s_rev = reverse_bits(s);
        const uint16_t last_bits = (s_rev & mask);
        const uint32_t mask_fill_ones = lshift_fill_ones(last_bits, j);
       carry_new = carry_new & mask_fill_ones; 
      }
      const uint64_t res = s << (m_1-1-j);
      if(j > 0){
        const uint32_t border = (carry_old & ((uint32_t)1 << (j-1)));
        r = border != 0 ? r | (uint32_t)1 << (m_1-1-j) : r;
      }
      r = res & r;
    }
    while(r != 0){
      // set all bits to zero except the last 1. Nice trick, eh?
      uint64_t t = r & -r;
      // count trailing zeros
      int pos = __builtin_ctzl(r);
      fprintf(stdout, "Match found at pos = %d\n", pos + alpha*i - m + 1);
      // set to zero the last 1
      r ^= t;
    }
  }
  // Naively check last part of the string that didn't fit in the 16 bytes blocks.
  int k = m;
  int j = i > 0 ? i*alpha - m + 1 : 0; 
  for(; j < n; ++j){
    if(p[m-k] == x[j]) 
      --k; 
    else
      k = m;
    if(k == 0){
      fprintf(stdout, "Match found at pos = %d\n", j - m + 1);
    }
  }
  free_pre_process(b,m_1);
}

int main()
{
  const char* needle = "IS";
  const char* haystack = "IN THIS EXAMPLE IS KNUTH OR DIJSTRA LISTED? OR WTF IS THIS EXAMPLE?";
  epsm_a(needle, strlen(needle), haystack, strlen(haystack));
  return 0;
}
