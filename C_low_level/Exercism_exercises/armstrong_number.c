#include "main.h"
/* header */

#define BUFFER_SIZE 1024

/**
* is_armstrong_number - determines if a number is an amstrong type or not
*
* @candidate: int type
*
* Descriptin: This function determines if a
* number is an amstrong number by receing input
* in char format, it stores the input and convert
* to int type. It makes a call to the is_armstrong
* function and converts the integer input to char
* in a str variable of 1024 characters. It gets the
* length of the char and runs a while loop afterwards.
* it uses modulo 10 to access the last digit of the number
* and it runs a for loop that's lesser than the length of the
* number (this for loop allows the use of the raise to power function)
* in the for loop it multiplies 1 with the last digit and stores it
* in mul then adds it with 0 and stores it in x. It divides the
* number inputed, by 10 to have access to the next number and it repeates
* the same proccess as long as the number inputed is greater than 0.
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
