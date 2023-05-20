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
		return (c + ('a' - 'a'))
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
