#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define MAX_LEN 32
#define OBFUSCATION_KEY 0xB7  // Harder to predict key shift

// We split the secret key into two parts to increase complexity
static unsigned char partialKey1[] = { 'S', 'u', 'p', 'e', 'r', 'S', 'e', 'c', 'u', 'r', 'e', 'H', 'i', 'd', '\0' };
static unsigned char partialKey2[] = { 'd', 'e', 'n', 'K', 'e', 'y', '@', '4', '2', '\0' };

void win() {
    printf("Congratulations! You have solved the challenge! Here is your flag: W3bIsCool-But-R3VEng-istoo\n");
}

// Arbitrary offset to hide the real address
uintptr_t globalFnPtrOffset = (uintptr_t)&win + 5;

// Combine partial keys into a single key
void combineKeys(char *combined, size_t maxSize) {
    // partialKey1 + partialKey2 = original: "SuperSecureHiddenKey@42"
    memset(combined, 0, maxSize);
    snprintf(combined, maxSize, "%s%s", (char*)partialKey1, (char*)partialKey2);
}

// Encrypt without assuming the result is a valid string
// We also return the length of the encrypted data in outLen
void xor_encrypt(const char *key, unsigned char *output, size_t *outLen) {
    size_t len = strlen(key);
    *outLen = len;

    for (size_t i = 0; i < len; i++) {
        // More complex shifting
        output[i] = (unsigned char)(key[i] ^ (OBFUSCATION_KEY + (i * 5)));
    }
}

int main() {
    char password[MAX_LEN];
    unsigned char encrypted_key[MAX_LEN];
    size_t encrypted_len = 0;
    char decrypted_key[MAX_LEN];
    char secret_key[64]; // big enough buffer to hold the combined key

    // Reconstruct the full secret key at runtime
    combineKeys(secret_key, sizeof(secret_key));

    printf("Enter password: ");
    fgets(password, MAX_LEN, stdin);
    password[strcspn(password, "\n")] = 0;  // Remove newline

    // Harder password
    if (strcmp(password, "UnbreakableP@ssw0rd!") == 0) {
        printf("Correct password! Generating encrypted key...\n");
        xor_encrypt(secret_key, encrypted_key, &encrypted_len);

        // Print the encrypted bytes in hexadecimal to avoid weird chars or null truncation
        printf("Encrypted Key (HEX): ");
        for (size_t i = 0; i < encrypted_len; i++) {
            printf("%02X", encrypted_key[i]);
        }
        printf("\n");

    } else {
        printf("Incorrect password. Exiting...\n");
        return 1;
    }

    // Additional complexity: function pointer retrieval
    uintptr_t actualFnPtr = globalFnPtrOffset - 5;
    void (*hiddenWin)() = (void(*)())actualFnPtr;

    printf("Now enter the decrypted key: ");
    fgets(decrypted_key, MAX_LEN, stdin);
    decrypted_key[strcspn(decrypted_key, "\n")] = 0;

    if (strcmp(decrypted_key, secret_key) == 0) {
        // We call the hidden win function pointer
        hiddenWin();
    } else {
        printf("Wrong decrypted key! Try harder.\n");
    }
    return 0;
}
