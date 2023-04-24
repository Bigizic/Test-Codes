#include "main.h"
/* header */

#define BUFFER_SIZE 1024

/**
* main - test code for square_root.c
*
* Description: this is a function that allows user to enter a positive number
* right after the prompt, it read the prompt to buffer, it adds NULL
* i.e '\0' to end of buffer with size of what it read already.
* it converts the buffer using strtod to a double type and stores it in x
*
* Return: 0
*/

int main(void)
{
	const char prompt[] = "Enter a positive number: ";
	int len = sizeof(prompt);
	ssize_t read_num;
	char buffer[BUFFER_SIZE];
	double x;

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
		printf("Error enter a positive number\n");
		exit(98);
	}
	x = strtod(buffer, NULL);
	if (x < 0)
	{
		printf("Number must be positive\n");
		exit(98);
	}

	printf("The square root of %g is %g\n", x, square_root(x));

	return (0);
}
