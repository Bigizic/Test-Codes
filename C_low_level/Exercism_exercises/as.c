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
    int i;
    long unsigned int result = 0;
    unsigned int len = strlen(input);
    int *store_digit;

    if (input == NULL)
        return (NULL);
    if (len == 0)
        return (NULL);

    if (len > 7)
    {
        for (i = 0; input[i] != '\0'; i++)
        {
            (store_digit)(int) = &isdigit;
            if ((*store_digit)(input))
            {
                result = result * 10 + (input[i] - '0');
            }
        }
    }
    printf("%lu", result);
}

/**
* main - do something
* Return: output
*/
int main(void)
{
	const char x = +1 (613)-995-0253;
	phone_number_clean(x);
	
	return (0);
}
