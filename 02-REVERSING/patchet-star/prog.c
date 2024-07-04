#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <ctype.h>
#include <stdlib.h> 

void anti_debug() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("Debugger detected!\n");
        exit(1);
    }
}

int check_key_stage1(const char *key) {
    return strlen(key) == 7 && key[0] == 'C' && key[1] == 'T' && key[2] == 'F';
}

int check_key_stage2(const char *key) {
    int sum = 0;
    for (int i = 3; i < 7; i++) {
        if (!isdigit(key[i])) return 0;
        sum += key[i] - '0';
    }
    return sum == 8;
}

int check_key(const char *key) {
    char obfuscated_key[] = { 'S', 'H', 'A', 'D', 'O', 'W', 'C', 'T', 'F', '\0' };
    for (int i = 0; i < strlen(obfuscated_key); i++) {
        obfuscated_key[i] ^= 0x5A; // XOR with a constant
    }
    return strcmp(key, obfuscated_key) == 0 && check_key_stage1(key) && check_key_stage2(key);
}

int main() {
    anti_debug();

    char key[256];
    printf("Enter the key: ");
    scanf("%255s", key);

    if (check_key(key)) {
        printf("Correct key! The flag is shadowCTF\n");
    } else {
        printf("Incorrect key.\n");
    }

    return 0;
}

