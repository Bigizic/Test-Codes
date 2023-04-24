#include "main.h"
/* header */

#define BUFFER_SIZE 1024

/**
* main - test code for square_root.c
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
	if (buffer[0] == '\0')
	{
		printf("Error no input entered\n");
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
