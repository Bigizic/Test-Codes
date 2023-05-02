#include "main.h"
/* header */

#define BUFFER_SIZE 1024

/**
* is_armstrong_number - determines if a number is an amstrong type or not
*
* @candidate: int type
*
* Descriptin: This function determines if a
* number is an amstrong number by storing the number
* in the *candidate*, it converts the number to
* a string using the sprintf and stores the converted
* number in a char array of 1024 chars. it gets the
* length of the array using strlen and stores it in the
* *len*. It uses a while loop to traverse through *candidate*
* it stores the *candidate* in a *duplicate* variable
* it sets *mul* to 1 every time the while loop runs.
* it updates *digit* to be the modulo of the *candidate* which
* gets the last digit of the *candidate*, it uses a for loop
* to multiply 1 by digit in number of times of the length
* of the *candidate* number. it stores *mul* in the *x* by adding *mul*
* to *x*. It updates *duplicate* to be equal to *candidate* multiplied
* by 10 which gives us access to the next number, because
* an int type won't store a decimal number, it uses the
* *i* to restart the loop to check if *duplicate* still > 0
*
* Return: 0
*/
bool is_armstrong_number(int candidate)
{
	int i = 0, n, mul, x = 0;
	int duplicate = candidate;
	char str[1024];
	int len, digit;

	sprintf(str, "%d", duplicate);
	len = strlen(str);
	while (duplicate > 0)
	{
		mul = 1;
		digit = duplicate % 10;
		for (n = 0; n < len; n++)
		{
			mul *= digit;
		}
		x += mul;
		duplicate /= 10;
		i++;
	}
	if (x == candidate)
	{
		printf("%d is an amstrong number because it's %d \n", candidate, x);
	}
	else
	{
		printf("%d is not an amstrong number, because it's %d \n", candidate, x);
	}
	return (0);
}


/**
* main - receives user input and check if it's an armstrong number
*
* Return: 0
*/
int main(void)
{
	const char prompt[] = "Enter a number: ";
	int len = sizeof(prompt);
	ssize_t read_num;
	char buffer[BUFFER_SIZE];
	int x;

	write(STDOUT_FILENO, prompt, len);
	read_num = read(STDIN_FILENO, buffer, BUFFER_SIZE);
	if (read_num == -1)
	{
		printf("Error reading input\n");
		exit(98);
	}
	buffer[read_num] = '\0';
	if (!isdigit(buffer[0]))
	{
		printf("Error enter a number\n");
		exit(98);
	}
	x = atoi(buffer);
	if (x < 0)
	{
		printf("Number must be greater than 0\n");
		exit(98);
	}

	is_armstrong_number(x);
	return (0);
}
