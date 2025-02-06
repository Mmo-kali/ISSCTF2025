#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/ptrace.h>
#include <time.h>

#define PORT 31337  // Hidden listening port
#define PAYLOAD_SIZE 16
#define TIMEOUT 300  // 5 minutes in seconds

// Encoded flag (XOR with key)
unsigned char encoded_flag[] = {0x25, 0x1E, 0x28, 0x0D, 0x3D, 0x0B, 0x1D, 0x3A, 
                                0x04, 0x0C, 0x2B, 0x01, 0x2A, 0x06, 0x09, 0x35,
                                0x38, 0x13, 0x2C, 0x0D, 0x24, 0x19, 0x0F, 0x30};

// XOR key for flag decryption
const char flag_xor_key = 0x42;

// XOR key for payload encryption
const char xor_key[PAYLOAD_SIZE] = {0x3A, 0x5F, 0x2D, 0x4C, 0x7B, 0x19, 0x42, 0x6E, 
                                    0x51, 0x39, 0x7A, 0x20, 0x5C, 0x33, 0x71, 0x48};


// Simple XOR decryption
void decrypt_payload(char *data, int len) {
    for (int i = 0; i < len; i++) {
        data[i] ^= xor_key[i % PAYLOAD_SIZE];
    }
}

// Decrypt the flag dynamically
void decrypt_flag(char *flag_buffer) {
    size_t flag_len = sizeof(encoded_flag);
    for (size_t i = 0; i < flag_len; i++) {
        flag_buffer[i] = encoded_flag[i] ^ flag_xor_key;
    }
    flag_buffer[flag_len] = '\0';
}

// Function that checks if the received payload is correct
int verify_payload(char *received) {
    char expected[PAYLOAD_SIZE] = {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0,
                                   0x1A, 0x2B, 0x3C, 0x4D, 0x5E, 0x6F, 0x7D, 0x8C};
    decrypt_payload(expected, PAYLOAD_SIZE);
    
    return memcmp(received, expected, PAYLOAD_SIZE) == 0;
}

// Main backdoor functionality
void start_listener() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[PAYLOAD_SIZE] = {0};

    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        exit(EXIT_FAILURE);
    }

    // Set socket options
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);  // Now listening silently

    // Bind the socket
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_fd, 1) < 0) {
        exit(EXIT_FAILURE);
    }

    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            continue;
        }

        read(new_socket, buffer, PAYLOAD_SIZE);
        decrypt_payload(buffer, PAYLOAD_SIZE);

        if (verify_payload(buffer)) {
            char flag[sizeof(encoded_flag) + 1];
            decrypt_flag(flag);
            send(new_socket, flag, strlen(flag), 0);
        }

        close(new_socket);
    }
}

// Run for 5 minutes, doing nothing
void start_timer() {
    time_t start_time = time(NULL);
    while (time(NULL) - start_time < TIMEOUT) {
        sleep(1); // Just waiting without consuming CPU
    }
}

// Displays the "cool" ASCII graphic with the warning message
void display_timer_message() {
    printf("\n");
    printf("╔════════════════════════════════════════╗\n");
    printf("║          ⏳  TIME IS TICKING...        ║\n");
    printf("║ You have 5 minutes to send FakeCrypto ║\n");
    printf("║          to address 0x01010101        ║\n");
    printf("╚════════════════════════════════════════╝\n");
    printf("\n");
    start_listener();
}

int main() {
    display_timer_message(); // Show the message before running
    start_timer(); // Run for 5 minutes
    return 0;
}

