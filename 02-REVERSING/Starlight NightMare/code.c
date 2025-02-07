#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define OBFUSCATION_KEY 0xB7

// Convert a single hex character to its numeric value
unsigned char hexValue(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    } else if (c >= 'A' && c <= 'F') {
        return c - 'A' + 10;
    } else if (c >= 'a' && c <= 'f') {
        return c - 'a' + 10;
    } else {
        return 0; // Invalid hex char
    }
}

// Decode a hex string into raw bytes
size_t hexDecode(const char *hexStr, unsigned char *out) {
    size_t len = strlen(hexStr);
    size_t outLen = 0;

    // Expect an even number of hex digits
    for (size_t i = 0; i < len; i += 2) {
        unsigned char high = hexValue(hexStr[i]);
        unsigned char low  = hexValue(hexStr[i + 1]);
        out[outLen++] = (high << 4) | low;
    }
    return outLen;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <hex_string>\n", argv[0]);
        return 1;
    }

    const char *hexInput = argv[1];
    size_t hexLen = strlen(hexInput);

    // Must be even length
    if (hexLen % 2 != 0) {
        fprintf(stderr, "Error: hex string must have even length.\n");
        return 1;
    }

    // Allocate enough space for decoded bytes
    unsigned char *encrypted = (unsigned char*)malloc(hexLen / 2 + 1);
    if (!encrypted) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    // Convert from hex to raw bytes
    size_t byteCount = hexDecode(hexInput, encrypted);

    // Decrypt in-place
    for (size_t i = 0; i < byteCount; i++) {
        encrypted[i] ^= (OBFUSCATION_KEY + (i * 5));
    }

    // Treat decrypted data as a C-string
    encrypted[byteCount] = '\0';

    printf("Decrypted Key: %s\n", encrypted);

    free(encrypted);
    return 0;
}
