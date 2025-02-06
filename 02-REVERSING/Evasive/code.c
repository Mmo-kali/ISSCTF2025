#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/ptrace.h>

#define FLAG_SIZE 32  // bhbureauCTF{xxxxxxxxxxxxxxxx}
#define XOR_KEY 0x7A   // Encryption key

// Encrypted & shuffled flag
char flag_encrypted[FLAG_SIZE] = {
    0x2A, 0x6C, 0x78, 0x1B, 0x3D, 0x42, 0x5E, 0x10, 
    0x66, 0x7F, 0x49, 0x58, 0x5D, 0x3A, 0x70, 0x31,
    0x4F, 0x2D, 0x6A, 0x5B, 0x2E, 0x73, 0x64, 0x15,
    0x3F, 0x21, 0x5C, 0x6E, 0x79, 0x34, 0x47, 0x5F
};

// XOR decryption
void decrypt_flag(char *flag) {
    for (int i = 0; i < FLAG_SIZE; i++) {
        flag[i] = flag_encrypted[i] ^ XOR_KEY;
    }
}

// Anti-debugging: detects tracing via ptrace
void anti_debug() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        puts("Debugger detected! Exiting...");
        exit(1);
    }
}

// Timing check: detects breakpoints via execution delays
void timing_check() {
    volatile int junk = 0;
    clock_t start = clock();
    for (volatile int i = 0; i < 1000000; i++) {
        junk += i % 3;  // Prevent compiler optimization
    }
    clock_t end = clock();
    if ((end - start) > 100) {
        puts("Timing anomaly detected! Exiting...");
        exit(1);
    }
}

// Complex key verification function
int check_key(const char *input) {
    if (strlen(input) != FLAG_SIZE) return 0;
    if (strncmp(input, "bhbureauCTF{", 12) != 0) return 0; // Enforce flag format
    
    // Jumbled transformation
    char modified[FLAG_SIZE];
    for (int i = 12; i < FLAG_SIZE - 1; i++) {
        modified[i] = input[i] ^ ((i * 7) % 256);
    }

    // Final transformation check
    unsigned int hash = 0;
    for (int i = 12; i < FLAG_SIZE - 1; i++) {
        hash += modified[i] * (i + 1);
    }

    return (hash == 0xDEADC0DE);  // Fake check; actual hash needs solving
}

int main() {
    anti_debug();
    timing_check();

    char input[FLAG_SIZE + 1];
    printf("Enter the flag: ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0;  // Remove newline

    if (check_key(input)) {
        char decrypted[FLAG_SIZE];
        decrypt_flag(decrypted);
        printf("Correct! Flag is: %s\n", decrypted);
    } else {
        puts("Incorrect flag!");
    }

    return 0;
}
