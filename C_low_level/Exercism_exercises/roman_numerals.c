#include "main.h"
/* header */

/**
* roman_numeral - converts a positive number to it's roman numeral
*
* Return: converted
*/

int main(void)
{
	int i;
	const char *roman_symbols[] = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
	unsigned int roman_values[] = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
	char *numerals = malloc(20 * sizeof(char));
	char *num, buffer[BUFFER_SIZE];
	unsigned int len, number;

	printf("Enter a number form 1 - 31000: ");
	num = fgets(buffer, sizeof(buffer), stdin);
	if (num == NULL)
		return (-1);
	len = strlen(buffer);

	if (len > 0 && buffer[len - 1] == '\n') /* checks if end of buffer = a new line */
		buffer[len - 1] = '\0'; /* updates last char of buffer to indicate end of line */

	numerals[0] = '\0';
	number = atoi(buffer);
	if (number == '\0')
	{
		printf("Error: enter a number\n");
		return (0);
	}

	for (i = 0; i < 13; i++)
	{
		while (number >= roman_values[i])
		{
			strcat(numerals, roman_symbols[i]);
			number -= roman_values[i];
		}
	}
	printf("The roman numeral for %s is %s\n", buffer, numerals);
	return (0);
}
