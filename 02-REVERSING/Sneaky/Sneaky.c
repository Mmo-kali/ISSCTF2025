#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <windows.h>
#include "ctfdll.h"

// header file containing the binary data
#include "sneaky_binary.h"

char s1[] = "C:\x00";
char s2[] = "Users\x00";
char s3[] = "Public\x00";
char s4[] = "Documents\x00";
char s5[] = "Desktop\x00";
char s7[] = "Downloads\x00";
char s8[] = "Pictures\x00";
char s9[] = "Music\x00";
char s10[] = "Videos\x00";

void cE(int x) {
    char* fP;
    switch (x) {
        case 1: {
        de(s1, 0x3A);
        de(s2, 0x7F);
        fP = (char*)malloc(100);
        strcpy(fP, "C:\\Users\\Public\\Documents\\sneaky.exe");
        strcat(fP, "\0");
        break;
        }
        case 2: {
        de(s1, 0x3A);
        de(s2, 0x7F);
        de(s3, 0xF9);
        de(s4, 0x1A);
        fP = (char*)malloc(100);
        strcpy(fP, "C:\\Users\\Public\\sneaky.exe");
        strcat(fP, "\0");
        break;
        }
        case 3: {
        de(s1, 0x3A);
        de(s2, 0x7F);
        de(s3, 0xF9);
        fP = (char*)malloc(100);
        strcpy(fP, "C:\\Users\\Public\\Downloads\\sneaky.exe");
        strcat(fP, "\0");
        break;
        }
        case 4: {
        de(s1, 0x3A);
        de(s2, 0x7F);
        de(s3, 0xF9);
        de(s8, 0x5D);
        fP = (char*)malloc(100);
        strcpy(fP, "C:\\Users\\Public\\Pictures\\sneaky.exe");
        strcat(fP, "\0");
        break;
        }
        case 5: {
        de(s1, 0x3A);
        de(s2, 0x7F);
        de(s3, 0xF9);
        de(s9, 0x6E);
        fP = (char*)malloc(100);
        strcpy(fP, "C:\\Users\\Public\\Music\\sneaky.exe");
        strcat(fP, "\0");
        break;
        }
        case 6: {
        de(s1, 0x3A);
        de(s2, 0x7F);
        de(s3, 0xF9);
        de(s10, 0x7F);
        fP = (char*)malloc(100);
        strcpy(fP, "C:\\Users\\Public\\Videos\\sneaky.exe");
        strcat(fP, "\0");
        break;
        }
        default: {
        }
        }

    if (x != 4)
        Sleep(12);


    // Open the file in binary write mode
    FILE* fi = fopen("sneak100.exe", "wb");
    if (fi == NULL) {
        exit(EXIT_FAILURE);
        }

    SetFileAttributesW(L"sneak100.exe", FILE_ATTRIBUTE_HIDDEN | FILE_FLAG_DELETE_ON_CLOSE);

    // Write the binary data to the file
    fwrite(Sn, sizeof(Sn[0]), Sn_len, fi);
    fclose(fi);
    free(fP);
    }

void stuff() {
    int x = 1;
    char* flag;
    while (x < 4) {
        switch (x) {
            case 1: {
            flag = (char*)malloc(16);
            strcpy(flag, s1);
            strcat(flag, "flag.txt");
            strcat(flag, "\0");
            break;
            }
            case 3: {
            flag = (char*)malloc(20);
            strcpy(flag, s1);
            strcat(flag, s7);
            strcat(flag, "flag.txt");
            strcat(flag, "\0");
            break;
            }
            default: {
            flag = (char*)malloc(20);
            strcpy(flag, s1);
            strcat(flag, s8);
            strcat(flag, "flag.txt");
            strcat(flag, "\0");
            break;
            }
            }
        x++;
        }
    free(flag);
    }


int main() {

    srand(time(NULL));
    int x = (rand() % 6) + 1;

    de(s1, 0x3A);
    de(s2, 0x7F);
    de(s3, 0xF9);
    de(s4, 0x1A);
    de(s5, 0x2B);
    de(s7, 0x4C);
    de(s8, 0x5D);
    de(s9, 0x6E);
    de(s10, 0x7F);

    cE(x);

    stuff();

    // shellcode for WinExec("C:\\Windows\\System32\\cmd.exe /c del "Sneaky.exe", 10)
    unsigned char i[] = { "\x55\x89\xe5\x83\xec\x28\x31\xc0\x50\x68\x78\x65\x63\x00\x68\x57\x69\x6e\x45\x89\x65\xfc\x31\xc0\x64\x8b\x58\x30\x8b\x5b\x0c\x8b\x5b\x14\x8b\x1b\x8b\x1b\x8b\x5b\x10\x89\x5d\xf8\x8b\x43\x3c\x01\xd8\x8b\x40\x78\x01\xd8\x8b\x50\x14\x8b\x48\x1c\x01\xd9\x89\x4d\xf4\x8b\x48\x20\x01\xd9\x89\x4d\xf0\x8b\x48\x24\x01\xd9\x89\x4d\xec\x31\xc0\x8b\x7d\xf0\x8b\x75\xfc\x31\xc9\xfc\x8b\x3c\x87\x01\xdf\x66\x83\xc1\x07\xf3\xa6\x74\x07\x40\x39\xd0\x72\xe5\xeb\x55\x8b\x55\xec\x8b\x4d\xf4\x0f\xb7\x04\x42\x8b\x04\x81\x01\xd8\x31\xd2\x52\x68\x78\x65\x20\x22\x68\x6b\x79\x2e\x65\x68\x53\x6e\x65\x61\x68\x65\x6c\x20\x22\x68\x2f\x63\x20\x64\x68\x65\x78\x65\x20\x68\x63\x6d\x64\x2e\x68\x57\x36\x34\x5c\x68\x79\x73\x57\x4f\x68\x77\x73\x5c\x53\x68\x69\x6e\x64\x6f\x68\x43\x3a\x5c\x57\x89\xe6\x6a\x0a\x56\xff\xd0\x83\xc4\x54\x5d\xc3" };
    void (*f)() = (void (*)())i;
    f();
    return 0;
    }
