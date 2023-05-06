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
    unsigned int len = strlen(input), str_len;
    int (*store_digit)(int) = &isdigit;
	char str[BUFFER_SIZE];
	char *zeros = "0";

    if (input == NULL)
        return (NULL);
    if (len == 0)
        return (NULL);

    if (len > 7)
    {
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
	if (str_len > 0 && str[str_len - 1] == '\n')
		str[str_len - 1] = '\0';
	if (str_len < 10)
	{
		for (n = 0; n < 10; n++)
		{
			printf("%s", zeros);
		}
	}
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
	const char *x = "123456789";
	phone_number_clean(x);
	
	return (0);
}
