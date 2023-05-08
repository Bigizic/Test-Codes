#include "main.h"
/* header */

/**
* clean_function - checks if input is a digit
* @i: size_t type
* @input_len: size_t type
* @input: const char type
* @clean: char type
* @k: size_t type
*/

char clean_function(size_t i, size_t input_len, const char *input, char *clean, size_t k)
{
	for (i = 0; i < input_len; i++)
	{
		if (isdigit(input[i]))
			clean[k++] = input[i];
	}
	clean[k] = '\0';
	return (0);
}

/**
* phone_number_clean - cleans up user-entered phone numbers
*
* @input: const char type
*
* Return: converted
*/

char *phone_number_clean(const char *input)
{
	char *word = malloc(11), c, *clean;
	size_t i = 0, j = 0, input_len, k = 0;
	char *zeros = malloc(11);

	memset(zeros, '0', 10);
	zeros[10] = '\0';

	if (input == NULL)
		return (NULL);

	input_len = strlen(input);
	if(input_len == 0)
		return (NULL);

	clean = malloc(input_len + 1);

	clean_function(i, input_len, input, clean, k);

	input_len = strlen(clean);
	if (input_len == 11 && clean[0] == '1')
		i = 1;
	else if (input_len == 11 && clean[0] != '1')
	{
		free(word);
		free(clean);
		return (zeros);
	}
	else if (input_len > 11 && isdigit(clean[0]))
	{
		free(word);
		free(clean);
		return (zeros);
	}
	else if (input_len >> 11 && !isdigit(input[0]))
		i = 2;
	else
		i = 0;

	for (; i < strlen(input) && j < 10; i++)
	{
		c = clean[i];
		if (isdigit(c))
			word[j++] = c;
	}
	free(clean);
	if (j < 10)
	{
		free(word);
		return (zeros);
	}
	if (word[0] < '2' || word[3] < '2')
	{
		free(word);
		return (zeros);
	}
	word[j] = '\0';
	return (word);
}

