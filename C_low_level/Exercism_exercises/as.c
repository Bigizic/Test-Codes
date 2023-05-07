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
	unsigned int len = strlen(input), str_len;
	int (*store_digit)(int) = &isdigit;
	char str[BUFFER_SIZE];
	char *zeros = "0000000000";

	if (input == NULL)
		return (NULL);
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
	sprintf(str, "%lu", result);
	str_len = strlen(str);

	if (str_len == 10)
	{
		printf("%s\n", str);
	}
	else if (str[0] == '1' && str_len > 10)
	{
		printf("%s\n", &str[1]);
	}
	else if (str_len < 10)
        {
		printf("%s\n", zeros);
        }
	else if (str[0] != 1 && str_len > 10)
	{
		printf("%s\n", zeros);
	}
	return (NULL);

}

/**
* main - do something
* Return: output
*/
int main(void)
{
	const char *x = "(023) 456-7890";
	phone_number_clean(x);	
	return (0);
}
