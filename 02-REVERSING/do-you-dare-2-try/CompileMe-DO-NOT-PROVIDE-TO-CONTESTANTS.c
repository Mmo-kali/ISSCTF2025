#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Decoding table to map Base64 characters to their indices
static const int b64_index[256] = {
    ['A'] = 0, ['B'] = 1, ['C'] = 2, ['D'] = 3,
    ['E'] = 4, ['F'] = 5, ['G'] = 6, ['H'] = 7,
    ['I'] = 8, ['J'] = 9, ['K'] = 10, ['L'] = 11,
    ['M'] = 12, ['N'] = 13, ['O'] = 14, ['P'] = 15,
    ['Q'] = 16, ['R'] = 17, ['S'] = 18, ['T'] = 19,
    ['U'] = 20, ['V'] = 21, ['W'] = 22, ['X'] = 23,
    ['Y'] = 24, ['Z'] = 25, ['a'] = 26, ['b'] = 27,
    ['c'] = 28, ['d'] = 29, ['e'] = 30, ['f'] = 31,
    ['g'] = 32, ['h'] = 33, ['i'] = 34, ['j'] = 35,
    ['k'] = 36, ['l'] = 37, ['m'] = 38, ['n'] = 39,
    ['o'] = 40, ['p'] = 41, ['q'] = 42, ['r'] = 43,
    ['s'] = 44, ['t'] = 45, ['u'] = 46, ['v'] = 47,
    ['w'] = 48, ['x'] = 49, ['y'] = 50, ['z'] = 51,
    ['0'] = 52, ['1'] = 53, ['2'] = 54, ['3'] = 55,
    ['4'] = 56, ['5'] = 57, ['6'] = 58, ['7'] = 59,
    ['8'] = 60, ['9'] = 61, ['+'] = 62, ['/'] = 63
};

unsigned char* base64_decode(const char* data, size_t input_length, size_t* output_length) {
    if (input_length % 4 != 0) return NULL;

    *output_length = input_length / 4 * 3;
    if (data[input_length - 1] == '=') (*output_length)--;
    if (data[input_length - 2] == '=') (*output_length)--;

    unsigned char* decoded_data = malloc(*output_length);
    if (decoded_data == NULL) return NULL;

    for (size_t i = 0, j = 0; i < input_length;) {
        uint32_t sextet_a = data[i] == '=' ? 0 & i++ : b64_index[(int)data[i++]];
        uint32_t sextet_b = data[i] == '=' ? 0 & i++ : b64_index[(int)data[i++]];
        uint32_t sextet_c = data[i] == '=' ? 0 & i++ : b64_index[(int)data[i++]];
        uint32_t sextet_d = data[i] == '=' ? 0 & i++ : b64_index[(int)data[i++]];

        uint32_t triple = (sextet_a << 18) + (sextet_b << 12) + (sextet_c << 6) + sextet_d;

        if (j < *output_length) decoded_data[j++] = (triple >> 16) & 0xFF;
        if (j < *output_length) decoded_data[j++] = (triple >> 8) & 0xFF;
        if (j < *output_length) decoded_data[j++] = triple & 0xFF;
    }

    return decoded_data;
}

void assembleFlag(char part1[], char part2[], char part3[], int controlVar) {
    if (controlVar == 1) {
        // Assuming the parts are Base64 encoded, decode them before concatenating
        size_t output_length1, output_length2, output_length3;
        unsigned char* decoded_part1 = base64_decode(part1, strlen(part1), &output_length1);
        unsigned char* decoded_part2 = base64_decode(part2, strlen(part2), &output_length2);
        unsigned char* decoded_part3 = base64_decode(part3, strlen(part3), &output_length3);

        if (!decoded_part1 || !decoded_part2 || !decoded_part3) {
            printf("Failed to decode the flag.\n");
            free(decoded_part1);
            free(decoded_part2);
            free(decoded_part3);
            return;
        }

        // Print each decoded part
        printf("CTF Flag: ");
        fwrite(decoded_part1, 1, output_length1, stdout);
        fwrite(decoded_part2, 1, output_length2, stdout);
        fwrite(decoded_part3, 1, output_length3, stdout);
        printf("\n");

        free(decoded_part1);
        free(decoded_part2);
        free(decoded_part3);
    } else {
        printf("Access Denied.\n");
    }
}

int main() {
    int controlVar = 1; // Set this to 1 to assemble and display the flag
    // Base64 encoded parts of the flag
    char part1[] = "YmhidXI=";
    char part2[] = "ZWF1Q1RGe0hpZGRlblBsYWc=";
    char part3[] = "aXNIZXJlfQ==";

    assembleFlag(part1, part2, part3, controlVar);

    return 0;
}