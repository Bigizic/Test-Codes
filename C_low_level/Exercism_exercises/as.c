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
	int i, c, n;
	long unsigned int result = 0;
	unsigned int len = strlen(input), str_len, j;
	int (*store_digit)(int) = &isdigit;
	char str[BUFFER_SIZE];
	char *zeros = "0";

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
	sprintf(str, "%d", c);
	str_len = strlen(str);

	if (str_len < 10 || str_len > 10)
	{
		for (n = 0; n < 10; n++)
		{
			if (str[0] != 1)
				printf("%s", zeros);
			else
				printf("%s", zeros);
		}
	}

	if (str[0] == 1 && str_len >= 10)
	{
		for (j = 0; j < str_len - 1; j++)
		{
			strcpy(&str[j], &str[j + 1]);
		}
		str[str_len- 1] = '\0';
		printf("%s", str);
	}
	printf("\n");
	printf("%lu\n", result);
	return (0);

}

/**
* main - do something
* Return: output
*/
int main(void)
{
	const char *x = "(223) 456-7890";
	phone_number_clean(x);
	
	return (0);
}
