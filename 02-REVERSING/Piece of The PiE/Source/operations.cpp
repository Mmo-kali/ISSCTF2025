#include "operations.h"
#include <stdexcept>

int Operations::a(int a, int b) {
    return a + b;
    }

int Operations::s(int a, int b) {
    return a - b;
    }

int Operations::m(int a, int b) {
    return a * b;
    }

int Operations::d(int a, int b) {
    if (b == 0) {
        throw std::invalid_argument("Division by zero is not allowed");
        }
    return a / b;
    }
