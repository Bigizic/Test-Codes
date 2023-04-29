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
int _convert_to_lower(int c);
bool is_isogram(char phrase[]);
int result(char in[]);
bool isogram_prompt(void);

int compute(const char *lhs, const char *rhs);

#endif
