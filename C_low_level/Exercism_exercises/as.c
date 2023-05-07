#include "main.h"
/**
* phone_number_clean - cleans up user-entered phone numbers
*
* @input: const char type
*
* Return: converted
*/

char *phone_number_clean(const char *input)
{
	int i, c;
	long unsigned int result = 0;
	unsigned int len, str_len;
	int (*store_digit)(int) = &isdigit;
	char *str,*zeros = "0000000000";

	if (input == NULL)
		return (NULL);
	len = strlen(input);
	if (len == 0)
		return (NULL);

	for (i = 0; input[i] != '\0'; i++)
        {
		c = (*store_digit)(input[i]);
		if (c)
		{
			result = result * 10 + (input[i] - '0');
		}
	}
	str = malloc(12);
	sprintf(str, "%lu", result);
	str_len = strlen(str);

	if ((str_len == 10 && str[3] < '2') || (str_len == 11 && str[1] < '2'))
	{
		free(str);
		return (zeros);
	}
	if (str_len == 11 && str[4] < '2')
	{
		free(str);
		return (zeros);
	}
	if (str_len == 10 && str[0] >= '2')
	{
		return (str);
		free(str);
	}
	else if (str[0] == '1' && str_len > 10)
	{
		return (&str[1]);
		free(str);
	}
	else if (str_len < 10)
        {
		free(str);
		return (zeros);
        }
	else if (str[0] != '1' && str_len > 10)
	{
		free(str);
		return (zeros);
	}
	else if (str[0] < '2' && str_len == 10)
        {
		free(str);
		return (zeros);
	}
	return (NULL);

}
