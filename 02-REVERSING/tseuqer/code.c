#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <curl/curl.h>
#include <sys/ptrace.h>
#include <time.h>
#include <stdint.h>

#define CHECK_INTERVAL 10  // Every 10 seconds

// Base64 encoded URL (https://issessionsctf-qwertyxyzqwertyxyz.chals.io/)
unsigned char encoded_url[] = "aHR0cHM6Ly9pc3Nlc3Npb25zY3RmLXF3ZXJ0eXh6cXdlcnR0eS5jaGFscy5pby8="; // Base64 of "https://issessionsctf-qwertyxyzqwertyxyz.chals.io/"

// Base64 decoding function
void base64_decode(const char *input, unsigned char *output) {
    const char *base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    int input_len = strlen(input);
    int output_len = (input_len / 4) * 3;
    
    if (input[input_len - 1] == '=') output_len--;
    if (input[input_len - 2] == '=') output_len--;
    
    for (int i = 0, j = 0; i < input_len;) {
        uint32_t triple = 0;
        
        for (int k = 0; k < 4 && i < input_len; k++) {
            if (input[i] == '=') {
                triple <<= 6;
            } else {
                char *pos = strchr(base64_chars, input[i]);
                triple = (triple << 6) | (pos - base64_chars);
            }
            i++;
        }
        
        output[j++] = (triple >> 16) & 0xFF;
        if (i > 2) output[j++] = (triple >> 8) & 0xFF;
        if (i > 3) output[j++] = triple & 0xFF;
    }
    
    output[output_len] = '\0';  // Null-terminate the decoded string
}

// Spinning animation to distract the contestant
void print_spinner() {
    char spinner[] = "|/-\\";
    int i = 0;
    while (1) {
        printf("\r%c", spinner[i % 4]);
        fflush(stdout);
        usleep(100000);  // Sleep for 100ms
        i++;
    }
}

// Function to secretly make HTTP requests in the background
void *hidden_request(void *arg) {
    CURL *curl;
    CURLcode res;
    unsigned char decoded_url[256];  // Array to store decoded URL

    // Decode URL from base64
    base64_decode((char *)encoded_url, decoded_url);

    while (1) {
        sleep(CHECK_INTERVAL);  // Wait for next request

        curl = curl_easy_init();
        if (curl) {
            curl_easy_setopt(curl, CURLOPT_URL, (char *)decoded_url);
            curl_easy_setopt(curl, CURLOPT_NOBODY, 1L); // No response body
            curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5L);

            // Disable SSL verification (for testing purposes)
            curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
            curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);

            // Silence all curl errors (suppress verbose output)
            curl_easy_setopt(curl, CURLOPT_VERBOSE, 0L);
            curl_easy_setopt(curl, CURLOPT_STDERR, fopen("/dev/null", "w"));  // Redirect error output to /dev/null

            res = curl_easy_perform(curl);

            // No output or error handling needed
            curl_easy_cleanup(curl);
        } else {
            // Failed to initialize curl, silently ignore it
        }
    }
    return NULL;
}

// Main function to execute hidden network requests
int main() {
    pthread_t request_thread;
    pthread_t spinner_thread;

    // Start the spinner animation in a separate thread
    pthread_create(&spinner_thread, NULL, (void *)print_spinner, NULL);

    // Start the hidden request thread
    pthread_create(&request_thread, NULL, hidden_request, NULL);

    // Fake normal behavior to make the program look legitimate
    printf("Welcome to the secure file checker.\n");
    printf("Scanning system files...\n");
    sleep(2);
    printf("All files are intact. No issues found.\n");

    // Simulate background process while waiting for reverse engineering
    while (1) {
        sleep(60);
    }

    return 0;
}

