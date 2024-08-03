#include <string.h>
#include <stdio.h>
#include <windows.h>

// A simple DLL that contains two functions: msg and de
// gcc -shared -o ctfdll.dll ctfdll.c -Wl,--out-implib,libctfdll.a
BOOL APIENTRY DllMain(HANDLE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {
    return TRUE;
    }


__declspec(dllexport)
void msg() {
    MessageBox(0, "Hello from DLL!", "DLL Message", MB_ICONINFORMATION | MB_OK);
    }


__declspec(dllexport)
void de(char* s, int k) {
    int i = 0;
    while (s[i] != '\0') {
        s[i] = s[i] ^ k;;
        i++;
        }
    }

