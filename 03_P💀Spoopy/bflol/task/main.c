#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define INPUT_BUF 1000
#define BF_BUF 30000


typedef struct {
    signed int buf_pos;
    int max_buf_pos;
    int prog_pos;
    unsigned char buf[BF_BUF];
    unsigned char prog[INPUT_BUF];
} vm;


int jump(vm *state, int direction){
    int ppos = state->prog_pos;

    while (ppos < INPUT_BUF && ppos >= 0) {
        ppos += direction;
        if ((direction == -1 && state->prog[ppos] == '[')||(direction == 1 && state->buf[ppos] == ']')) {
            return ppos;
        }
    }
}

void interpret(vm *state) {

    while(state->prog[state->prog_pos] != 0) {
        switch (state->prog[state->prog_pos]) {
            case '>':
                ++state->buf_pos;
                break;
            case '<':
                --state->buf_pos;
                break;
            case '+':
                ++state->buf[state->buf_pos];
                break;
            case '-':
                --state->buf[state->buf_pos];
                break;
            case '.':
                putchar(state->buf[state->buf_pos]);
                break;
            case ',':
                state->buf[state->buf_pos] = getchar();
            case '[':
                if (state->buf[state->buf_pos] == 0)
                    state->prog_pos = jump(state, 1);
                break;
            case ']':
                if (state->buf[state->buf_pos] != 0)
                    state->prog_pos = jump(state, -1);
                break;
        }
        state->prog_pos++;
    }
}


int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    vm state;

    state.buf_pos = 0;
    state.max_buf_pos = BF_BUF;
    state.prog_pos = 0;

    memset(state.buf, '\0', BF_BUF);
    memset(state.prog, '\0', INPUT_BUF);

    if(!fgets(state.prog, INPUT_BUF, stdin)) {
        puts("Reading didn't work.");
        return 1;
    }

    interpret(&state);

    return 0;
}
