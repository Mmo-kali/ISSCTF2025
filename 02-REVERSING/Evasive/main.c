#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/ptrace.h>

#define FLAG_SIZE 31  // bhbureauCTF{xxxxxxxxxxxxxxxx}
#define XOR_KEY 0x7A   // Encryption key

// Encrypted & shuffled flag
char flag_encrypted[FLAG_SIZE] = {0x18, 0x12, 0x18, 0x0F, 0x08, 0x1F, 0x1B, 0x0F, 0x39, 0x2E, 0x3C, 0x01, 0x65, 0x45, 0x29, 0x49, 0x19, 0x08, 0x59, 0x0E, 0x2F, 0x14, 0x0C, 0x49, 0x58, 0x16, 0x49, 0x1E, 0x02, 0x57, 0x07};

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
    struct timespec start, end;
    volatile int junk = 0;

    // Get start time (monotonic clock is preferred for measuring intervals)
    clock_gettime(CLOCK_MONOTONIC, &start);

    // Code to time
    for (volatile int i = 0; i < 9000000; i++) {
        junk += i % 3;
    }

    // Get end time
    clock_gettime(CLOCK_MONOTONIC, &end);

    // Calculate elapsed time in seconds with nanosecond precision
    double elp = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    
    if (elp > 0.045) {
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
   
    return (hash == 0xFFFFD737); 
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
