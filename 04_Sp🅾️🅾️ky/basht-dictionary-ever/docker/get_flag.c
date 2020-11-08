#include <stdio.h>
#include <stdlib.h>

int main() {
	FILE *fptr;
	char ch;
	int lol;
	printf("Calc: 42*10=");
	fflush(stdout);
	scanf("%d", &lol);
	if(lol!=420) {
		printf("nope.\n");
		exit(420);
	}
	fptr = fopen("/flag.txt", "r");
	ch = fgetc(fptr);
	while(ch != EOF) {
		printf("%c", ch);
		ch = fgetc(fptr);
	}
	fclose(fptr);
}
