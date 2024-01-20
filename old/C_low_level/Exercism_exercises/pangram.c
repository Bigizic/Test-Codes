#include "main.h"
/* header */

/**
* _convert_to_lower - converts an alphabet to small
*
* @c: int type
*
* Return: converted
*/
int _convert_to_lower(int c)
{
	if (c >= 'A' && c <= 'Z')
		return (c + ('a' - 'A'));

	else if (c >= 'a' && c <= 'z')
	{
		return (c + ('a' - 'a'));
	}
	return (c);
}

/**
* is_pangram - checks if a sentence is a pangram
*
* @sentence: const char type also the sentence to check
*
* Return: true or false
*/
bool is_pangram(const char* sentence)
{
	char c;
	int i, sentence_cp = 0, j;
	
	if (sentence == NULL)
		return false;
	if (strlen(sentence) == 0)
		return false;

	for (i = 0; sentence[i] != '\0'; i++)
	{
		c = _convert_to_lower(sentence[i]);
		if (isalpha(c))
		{
			j = c - 'a';
			sentence_cp |= (1 << j);
		}
	}
	return sentence_cp == ((1 << 26) - 1);
}

/**
* main - main code for is_pangram, takes input and compares it
*
* Return: void
*/
int main(void)
{
        char *phrase, phrase_buffer[1024];

        printf("NOTE: A pangram is a sentence using every letter\nof the alphabet at least once. It doesn't matter\nif a letter is lower-case or upper-case.\nThe best known English pangram is:\nThe quick brown fox jumps over the lazy dog.\nNow enter a sentence! \n\n");

        phrase = fgets(phrase_buffer, sizeof(phrase_buffer), stdin);
        if (phrase == NULL)
        {
                printf("Error: Enter a word or sentence\n");
                return (-1);
        }
        if (strlen(phrase_buffer) == 0)
        {
                printf("Error: Enter a word or sentence\n");
                return (-1);
        }

        if (strlen(phrase_buffer) > 0 &&
                        phrase_buffer[strlen(phrase_buffer) - 1] == '\n')
                phrase_buffer[strlen(phrase_buffer) - 1]  = '\0';

        if (is_pangram(phrase_buffer))
        {
                printf("Your input: {%s}, is a Pangram\n", phrase_buffer);
                return (0);
        }
        else
        {
                printf("Your input: {%s}, is not a Pangram\n", phrase_buffer);
                return (0);
        }
        return (0);
}
