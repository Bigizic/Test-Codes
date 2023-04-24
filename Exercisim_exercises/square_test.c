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
		perror("Error: enter a number\n");
		return (1);
	}

	read_num = read(STDIN_FILENO, buffer, BUFFER_SIZE);
	if (read_num == -1)
	{
		perror("Error reading what you eneter");
		return (1);
	}

	if (av != NULL)
	{
		x = atoi(buffer);
		if (isdigit(x))
		{
			square_root(x);
		}
		else
		{
			perror("Number you entered is not a digit");
			return (0);
		}
	}
	return (0);
}			
