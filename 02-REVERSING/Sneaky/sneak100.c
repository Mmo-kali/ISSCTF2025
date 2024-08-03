#include <windows.h>
#include <stdio.h>
#include <string.h>
void __();


// the file dropped by the Sneaky.exe program, 2nd stage of challenge
int main() {
    if (LoadLibraryW(L"kernel32.dll") == NULL) {
        MessageBox(0, "Uh something broke, try again maybe?", "Error", MB_ICONERROR | MB_OK);
        return 1;
        }
    if (MessageBox(0, "hewwo, hii there! welcome to absolutely not shady malware >w<", "helpa >w<'", MB_ICONINFORMATION | MB_YESNO) == IDYES) {
        MessageBox(0, "hewwo, cutie x3\ni suggest you twy jumping awound > :3", "helpa > w < '", MB_ICONINFORMATION | MB_OK);
        }
    else {
        MessageBox(0, "h-hewwo, pwease don't ignore me x3  i-i'll twy my best to help you, i pwomise :3 pwease give me a chance to show you >///< i-i weawwy want to be thewe fow you, pwease x3", "helpa > w < '", MB_ICONINFORMATION | MB_OK);
        }
    return 0;
    }

// uncallled function, users will have to manually call it by extracting the address
void __() {
    char str1[] = "congwatu";
    char str12[] = "lations";
    char str15[] = "cess ";
    char str13[] = ", the";
    char str14[] = " pwin";
    char str18[] = "hew ";
    char str16[] = "is i";
    char str17[] = "n anot";
    char str19[] = "castwe ";
    char str10[] = ">w<";

    char str2[] = "hehe, jkjk, ";
    char str22[] = "the ";
    char str23[] = "fla";
    char str24[] = "ggy-wa";
    char str25[] = "ggy";
    char str26[] = " will";
    char str29[] = "g.txt";
    char str27[] = " be in";
    char str28[] = " fla";


    char* con = (char*)malloc(120);
    char* con2 = (char*)malloc(69);

    strncpy(con, str1, strlen(str1));
    strncat(con, str12, strlen(str12));
    strncat(con, str13, strlen(str13));
    strncat(con, str14, strlen(str14));
    strncat(con, str15, strlen(str15));
    strncat(con, str16, strlen(str16));
    strncat(con, str17, strlen(str17));
    strncat(con, str18, strlen(str18));
    strncat(con, str19, strlen(str19));
    strncat(con, str10, strlen(str10));
    strncat(con, "\0", 1);
    MessageBox(0, con, "UwU!", MB_ICONINFORMATION | MB_OK);

    free(con);

    strncpy(con2, str2, strlen(str2));
    strncat(con2, str22, strlen(str22));
    strncat(con2, str23, strlen(str23));
    strncat(con2, str24, strlen(str24));
    strncat(con2, str25, strlen(str25));
    strncat(con2, str26, strlen(str26));
    strncat(con2, str27, strlen(str27));
    strncat(con2, str28, strlen(str28));
    strncat(con2, str29, strlen(str29));
    strncat(con2, "\0", 1);
    MessageBox(0, con2, "UwU!", MB_ICONINFORMATION | MB_OK);

    free(con2);

    // shell code to call WinExec("C:\\Windows\\System32\\cmd.exe /c "ShadowCTF{Cookie_FOR_your_hardWork}" > flag.txt", 10);
    unsigned char sc[] = { "\x55\x89\xe5\x83\xec\x28\x31\xc0\x50\x68\x78\x65\x63\x00\x68\x57\x69\x6e\x45\x89\x65\xfc\x31\xc0\x64\x8b\x58\x30\x8b\x5b\x0c\x8b\x5b\x14\x8b\x1b\x8b\x1b\x8b\x5b\x10\x89\x5d\xf8\x8b\x43\x3c\x01\xd8\x8b\x40\x78\x01\xd8\x8b\x50\x14\x8b\x48\x1c\x01\xd9\x89\x4d\xf4\x8b\x48\x20\x01\xd9\x89\x4d\xf0\x8b\x48\x24\x01\xd9\x89\x4d\xec\x31\xc0\x8b\x7d\xf0\x8b\x75\xfc\x31\xc9\xfc\x8b\x3c\x87\x01\xdf\x66\x83\xc1\x07\xf3\xa6\x74\x0a\x40\x39\xd0\x72\xe5\xe9\x82\x00\x00\x00\x8b\x55\xec\x8b\x4d\xf4\x0f\xb7\x04\x42\x8b\x04\x81\x01\xd8\x31\xd2\x52\x68\x2e\x74\x78\x74\x68\x66\x6c\x61\x67\x68\x22\x20\x3e\x20\x68\x6f\x72\x6b\x7d\x68\x61\x72\x64\x57\x68\x75\x72\x5f\x68\x68\x52\x5f\x79\x6f\x68\x65\x5f\x46\x4f\x68\x6f\x6f\x6b\x69\x68\x54\x46\x7b\x43\x68\x64\x6f\x77\x43\x68\x22\x53\x68\x61\x68\x63\x68\x6f\x20\x68\x2f\x63\x20\x65\x68\x65\x78\x65\x20\x68\x63\x6d\x64\x2e\x68\x6d\x33\x32\x5c\x68\x79\x73\x74\x65\x68\x77\x73\x5c\x53\x68\x69\x6e\x64\x6f\x68\x43\x3a\x5c\x57\x89\xe6\x6a\x0a\x56\xff\xd0\x83\xc4\x54\x5d\xc3" };
    void (*fp)() = (void (*)())sc;
    fp();
    }