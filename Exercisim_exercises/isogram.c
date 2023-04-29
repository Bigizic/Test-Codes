#include "main.h"

/**
* _convert_to_lower - converts a letter to a small letter
*
* @c: char letter to convert
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
* main - determines if a word is an isogram
*
* Description: an isogram is a letter that doesn't repeat
* itself twice in a word or sentence, includeing symbols and spcace.
* so this function converts a word or words to small letters 
* and checks if the converted repeats itself by iterating through
* the word and interating through the word again but this time it
* adds one to the iterated word. It returns false if a word or
* symbol repeats itself otherwise it returns true.
*
* Return: boolen value
*/
int main(void)
{
    unsigned int i, j;
    size_t len;
    char input[1024];
    char *phrase;

    printf("Enter a word or phrase: ");
    phrase = fgets(input, sizeof(input), stdin);

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
                printf("The input: %s, is not an isogram because the ""%s"" repeats\n", input, phrase[i]);
                return (-1);
            }

            if (_convert_to_lower(phrase[i]) == _convert_to_lower(phrase[j]))
            {
                printf("The input: %s, is not an isogram because the ""%s"" repeats\n", input, phrase[i]);
                return (-1);
            }
        }
    }
    printf("The input: %s, is an isogram", input);
    return (0);
}
