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

void get_flag(char *output) {
    unsigned char obfuscated_flag[] = {
        0x3d, 0xf1, 0x40, 0x6a, 0x28, 0x69, 0xf0, 0x7e, 0x20, 0x68, 0x5b, 0x56,
        0x36, 0x70, 0x2b, 0x60
    };
    char key = 0x4F; // XOR key
    for (int i = 0; i < sizeof(obfuscated_flag); i++) {
        output[i] = obfuscated_flag[i] ^ key;
    }
    output[sizeof(obfuscated_flag)] = '\0'; // null-terminate the string
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
    char obfuscated_key[] = { 'S', 'H', 'A', 'D', 'O', 'W', 'P', 'A', 'T', 'C', 'H', '\0' };
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
        char flag[50];
        get_flag(flag);
        printf("Correct key! The flag is: %s\n", flag);
    } else {
        printf("Incorrect key.\n");
    }

    return 0;
}
