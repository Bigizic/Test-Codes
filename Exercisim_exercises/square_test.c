#include "main.h"
/* header */

#define BUFFER_SIZE 1024

/**
* main - test code for square_root.c
*
* Return: 0
*/

int main(int ac, char *av[])
{
	const char prompt[] = "Enter a positive number: ";
	int len = sizeof(prompt);
	ssize_t read_num;
	char buffer[BUFFER_SIZE];
	double x;

	write(STDOUT_FILENO, prompt, len);

	if (ac != 1)
	{
		printf("Error: enter a number\n");
		exit(98);
	}

	read_num = read(STDIN_FILENO, buffer, BUFFER_SIZE);
	if (read_num == -1)
	{
		printf("Error reading what you eneter\n");
		exit(98);
	}

	if (av != NULL)
	{
		x = atoi(buffer);
		if (x >= 0)
		{
			square_root(x);
		}
		else
		{
			printf("Number you entered is not a digit\n");
			exit(98);
		}
	}
	return (0);
}
