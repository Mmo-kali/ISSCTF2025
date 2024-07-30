#include "operations.h"
#include <stdexcept>

int Operations::add(int a, int b) {
    return a + b;
    }

int Operations::subtract(int a, int b) {
    return a - b;
    }

int Operations::multiply(int a, int b) {
    return a * b;
    }

int Operations::divide(int a, int b) {
    if (b == 0) {
        throw std::invalid_argument("Division by zero is not allowed");
        }
    return a / b;
    }
