#ifndef MAIN_H
#define MAIN_H

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>


/* function prototypes */
bool is_armstrong_number(int candidate);
double square_root(double num);

/* isogram */
bool is_isogram(const char phrase[]);
int _tolower(int c);
int result(const char in[]);
bool isogram_prompt(void);

int compute(const char *lhs, const char *rhs);

#endif
