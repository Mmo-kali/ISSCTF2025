#ifndef CTFDLL_H
#define CTFDLL_H

// header to be included with programs that use the DLL
// add [-L. -lctfdll] to gcc compile command
#ifdef __cplusplus
extern "C" {
#endif

    __declspec(dllimport) void msg();
    __declspec(dllimport) void de(char* s, int k);

#ifdef __cplusplus
    }
#endif

#endif // CTFDLL_H