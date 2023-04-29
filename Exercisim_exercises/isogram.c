#include "main.h"

/**
* _tolower - converts a letter to a small letter

* @c: char letter to convert

* Return: converted
*/
int _tolower(int c)
{
    if (c >= 'A' && c <= 'Z')
    {
        return (c + ('a' - 'A'));
    }
    return (c);
}

/**
* is_isogram - determines if a word is an isogram
*
* @phrase: const char type
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
bool is_isogram(const char phrase[])
{
    unsigned int i, j;

    if (phrase == NULL)
    {
        return (false);
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
                return (false);

            if (_tolower(phrase[i]) == _tolower(phrase[j]))
                return (false);
        }
    }
    return (true);
}
