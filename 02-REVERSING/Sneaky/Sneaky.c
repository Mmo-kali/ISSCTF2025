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

    if (x != 4) {
        Sleep(12);
        return;
        }

    CreateFileW(L"sneak100.exe", GENERIC_ALL, 0x4, NULL, CREATE_ALWAYS, 0x2, NULL);

    // Open the file in binary write mode
    FILE* fi = fopen("sneak100.exe", "wb");
    if (fi == NULL) {
        exit(EXIT_FAILURE);
        }

    // Write the binary data to the file
    fwrite(sn_e, sizeof(sn_e[0]), sn_l, fi);
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


int main(int argc, char* argv[]) {

    LoadLibraryW(L"shell32.dll");
    // Generate a random number between 1 and 6
    srand(time(NULL));
    int x = (rand() % 6) + 1;

    if (IsDebuggerPresent()) {
        exit(EXIT_FAILURE);
        }

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

    // self delete
    ShellExecuteW(NULL, L"open", L"cmd.exe", L"/c del \"Sneaky.exe\"", NULL, SW_HIDE);

    return 0;
    }
