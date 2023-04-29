#include "main.h"

/**
 * _convert_to_lower - converts an aplhabet to small letter
 *
 * @c: int type
 *
 * Return: converted
 */

int _convert_to_lower(int c)
{
	if (c >= 'A' && c <= 'Z')
	{
		return (c + ('a' - 'A'));
	}
	return (c);
}

/**
* main - do something
*
* Description: this function prints a prompt message
* it takes an input with limit of 1024 characters
* then gets the length of the input and minus one
* from the last char to check if the input has
* a new-line char, normally the input always ends with
* new-line. It minus one to have access to the last
* char and tells the compiler to remove the new-line
* and update it to NULL terminated which indicates
* end of the string.
*
* Return: void
*/

int main(void)
{
	unsigned int i, j;
	size_t len;
	char input[1024];
	char *phrase;

	printf("Enter a word or phrase: ");
	phrase = fgets(input, sizeof(input), stdin);
	len = strlen(input); /* gets length of input */

	if (len > 0 && input[len -1] == '\n')
	{
		input[len - 1] = '\0';
	}

	if (phrase == NULL)
	{
		printf("Error: enter a word or phrase\n");
		return (0);
	}

	for (i = 0; phrase[i] != '\0'; i++)
	{
		if (phrase[i] == ' ' || phrase[i] == '-')
		{
			continue;
		}
		for (j = i + 1; phrase[j] != '\0'; j++)
		{
			if (phrase[j] == ' ' || phrase[j] == '-')
			{
				continue;
			}
			if (phrase[i] == phrase[j])
			{
				printf("The input: %s, is not an isogram because the ""%d"" repeats\n", input, phrase[i]);
				return (-1);
			}
			if (_convert_to_lower(phrase[i]) == _convert_to_lower(phrase[j]))
			{
				printf("The input: %s, is not an isogram because the ""%d"" repeats\n", input, phrase[i]);
				return (-1);
			}
		}
	}
	printf("The input: %s, is an isogram\n", input);
	return (0);
}
