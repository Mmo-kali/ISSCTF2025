#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

BOOL chkDbg();
BOOL chkTrp();
char* decoy();
char* real();
void inject(char* str);


int main() {

    // Check for trap flag
    if (chkTrp())
        return 1;

    // initialize random number generator
    int randNum;
    srand(time(NULL));

    // Random number between 1 & 10 (inclusive)
    int rnd1 = rand() % 10 + 1;
    int rnd2 = rand() % 10 + 1;

    // skew the random number to be the larger of the two
    randNum = (((rnd1) > (rnd2)) ? (rnd1) : (rnd2));

    // Check for debugger
    if (chkDbg())
        return 1;

    // initialize loop counter and flag string
    int i = 0;
    char* fL;

    // single iteration loop to inject the flag (real or decoy) into the target process
    while (i < 1) {
        switch (randNum) {
            case 1:
                fL = decoy();
                inject(fL);
                break;
            case 2:
                fL = real();
                inject(fL);
                break;
            case 3:
                fL = decoy();
                inject(fL);
                break;
            case 4:
                fL = decoy();
                inject(fL);
                break;
            case 5:
                fL = decoy();
                inject(fL);
                break;
            case 6:
                fL = decoy();
                inject(fL);
                break;
            case 7:
                fL = decoy();
                inject(fL);
                break;
            case 8:
                fL = decoy();
                inject(fL);
                break;
            case 9:
                fL = decoy();
                inject(fL);
                break;
            case 10:
                fL = decoy();
                inject(fL);
                break;
            }
        i++;
        }

    // Delete Self
    ShellExecute(NULL, "open", "cmd.exe", "/c del Jackpot.exe", NULL, SW_HIDE);

    return 0;
    }

BOOL chkDbg() {
    LARGE_INTEGER frequency, start, end;
    if (!QueryPerformanceFrequency(&frequency)) {
        return FALSE;
        }

    // Start timing
    QueryPerformanceCounter(&start);

    // Code to measure
    for (int i = 0; i < 100000; i++) {
        asm("nop");
        }

    // End timing
    QueryPerformanceCounter(&end);

    // Calculate the elapsed time in microseconds (27.30-31.90)
    double elapsedTime = (double)(end.QuadPart - start.QuadPart) * 1000000.0 / frequency.QuadPart;

    // If the elapsed time is significantly longer than expected, a debugger might be present
    return (elapsedTime > 32.0); // Adjust the threshold as needed
    }

BOOL chkTrp() {
    // check for the trap flag
    char flg = 0;
    /*
    pushing all flags onto the stack and popping the trap flag into eax
    __volatile__ is used to prevent the compiler from optimizing the assembly code
    */
    __asm__ __volatile__(
        "pushf\n\t"
        "pop %%eax\n\t"
        : "=r"(flg)
        :
        : "eax"
    );

    // checking if the 9th bit (TF) is set
    return (flg & 0x100);
    }

char* decoy() {
    // initialize random number generator
    srand(time(NULL));

    // initialize loop counter and allocate memory for the flag string
    int chr, i = 0;
    char* fL = malloc(11);

    // generate a random flag string, alternating between uppercase and lowercase characters
    while (i < 10) {
        switch (i % 2) {
            case 0:
                chr = rand() % 26 + 65;
                break;
            case 1:
                chr = rand() % 26 + 97;
                break;
            }
        fL[i] = chr;
        i++;
        }

    fL[i] = '\0';

    return fL;
    }

char* real() {
    // base64 encoded flag string
    char f3[] = "YMDsA";
    char f1[] = "AQS2C6+";
    char f2[] = "g5ALBOB";
    char f4[] = "IOJgrg";
    char f5[] = "Vg+wFIA";
    // allocate memory for the flag string and concatenate the parts
    char* fL = (char*)malloc(34);
    strcpy(fL, f1);
    strcat(fL, f2);
    strcat(fL, f3);
    strcat(fL, f4);
    strcat(fL, f5);
    strcat(fL, "\0");
    return fL;
    }

void inject(char* str) {
    // Open a handle to the target process
    HANDLE hx = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, GetCurrentProcessId() + 1);
    // If the handle is NULL, return
    if (hx == NULL) {
        return;
        }
    // Allocate memory in the target process and write the flag string
    LPVOID ax = VirtualAllocEx(hx, NULL, strlen(str), MEM_COMMIT | MEM_RESERVE, PAGE_READONLY);
    WriteProcessMemory(hx, ax, str, strlen(str), NULL);
    // Sleep for 1 second
    Sleep(1000);
    // Free the allocated memory and close the handle
    VirtualFreeEx(hx, ax, 0, MEM_RELEASE);
    CloseHandle(hx);

    }
