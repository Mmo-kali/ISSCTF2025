#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#define MaxLEN 0x42

typedef struct {
    char name[MaxLEN];
    char admin;
    } User;

int chkDbg() {
    BOOL RemDbg = FALSE;
    BOOL Dbg = IsDebuggerPresent();
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &RemDbg);
    return ((RemDbg || Dbg) ? 1 : 0);
    }

void createUser(User* user, int i) {
    char overFlowBuff[256];
    printf("Enter user %d's name: ", i);
    char input[MaxLEN];
    scanf("%s", input);
    fflush(stdin);

    // For debugging purposes
    // printf("%d\n", strlen(input));
    // printf("%d\n", strcspn(input, "\n"));

    if (strlen(input) > MaxLEN) {
        user->name[0] = 'N';
        user->name[1] = 'U';
        user->name[2] = 'L';
        user->name[3] = 'L';
        user->name[4] = '\0';
        }
    else {
        // Copy name into user struct
        strcpy(user->name, input);
        }
    }

void printFlag() {
    char flag[12] = "r,\'w6\'2\x03*q#&";

    for (int i = 0; i < 12; i++)
        flag[i] = flag[i] ^ 0x42;

    printf("%s\n", flag);
    }

void printUser(User* user, int i) {
    LARGE_INTEGER frequency, start, end;
    if (!QueryPerformanceFrequency(&frequency)) {
        exit(1);
        }
    // Start timing
    QueryPerformanceCounter(&start);

    char head[9] = { 'h', 'h', 'h', 'b', '\x17', '1', '\'', '0' };
    char tail[4] = "hhh";
    char prmpt[5] = "\x0c#/\'";

    for (int i = 0; i < 8; i++)
        head[i] = head[i] ^ 0x42;
    head[8] = '\0';

    for (int i = 0; i < 3; i++)
        tail[i] = tail[i] ^ 0x42;
    tail[3] = '\0';

    for (int i = 0; i < 4; i++)
        prmpt[i] = prmpt[i] ^ 0x42;
    prmpt[4] = '\0';

    // End timing
    QueryPerformanceCounter(&end);

     // Calculate the elapsed time in microseconds
    double elapsedTime = (double)(end.QuadPart - start.QuadPart) * 1000000.0 / frequency.QuadPart;

    if (elapsedTime > 2.0)
        exit(1);

    printf("\n%s %d %s\n", head, i, tail);
    // Print user information
    printf("%s: %s\n", prmpt, user->name);

    // if user exploited off-by-one vuln, print flag
    if (user->admin != 'N')
        printFlag();

    }

void AltCreateUser(User* user, int i) {
    char input[MaxLEN];
Rep:
    printf("Enter user %d's name: ", i);

    scanf("%s", input);

    if (strcspn(input, "\n") <= MaxLEN) {
        // Copy name into user struct
        strncpy(user->name, input, MaxLEN - 2);
        user->name[MaxLEN - 1] = '\0';
        }
    else {
        fflush(stdin);
        goto Rep;
        }
    }

void AltPrintUser(User* user, int i) {
    char head[9] = { 'h', 'h', 'h', 'b', '\x17', '1', '\'', '0' };
    char tail[4] = "hhh";
    char prmpt[5] = "\x0c#/\'";

    for (int i = 0; i < 8; i++)
        head[i] = head[i] ^ 0x42;
    head[8] = '\0';

    for (int i = 0; i < 3; i++)
        tail[i] = tail[i] ^ 0x42;
    tail[3] = '\0';

    for (int i = 0; i < 4; i++)
        prmpt[i] = prmpt[i] ^ 0x42;
    prmpt[4] = '\0';

    printf("\n%s %d %s\n", head, 0, tail);
    printf("%s: %s\n", prmpt, "User");

    }

void garbage() {
    User altUser[3];

    for (int i = 0; i < 3; i++) {
        altUser[i].admin = 'N';
        AltCreateUser(&altUser[i], i + 1);
        }

    for (int i = 0; i < 3; i++)
        AltPrintUser(&altUser[i], i + 1);

    }


int main() {
    // Initialize user struct
    User users[3];
    // Check for debugger
    if (chkDbg() != 0) {
        garbage();
        exit(0);
        }

    // Create user
    for (int i = 0; i < 3; i++) {
        users[i].admin = 'N';
        createUser(&users[i], i + 1);
        }

    // Print user information
    for (int i = 0; i < 3; i++)
        printUser(&users[i], i + 1);

    return 0;
    }