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


/**
* isogram_prompt - function that prints a prompt and read user prompt
*
* Description: this function prints a prompt message
* it takes an input with limit of 1024 characters
* then gets the length of the input and minus one
* from the last char to check if the input has
* a new-line char, normally the input always ends with
* new-line. It minus one to have access to the last
* char and tells the compiler to remove the new-line
* and update it to NULL terminated which indicates
* end of the string.
*
* Return: 0 if success
*/
bool isogram_prompt(void)
{
	const char user_input[1024];
	size_t len;
	bool status;

	printf("Enter a word or phrase: ");
	fgets(user_input, sizeof(user_input), stdin);

	len = strlen(user_input); /* gets length of input */
	if (len > 0 && user_input[len -1] == '\n')
	{
		user_input[len - 1] = '\0';
	}
	status = is_isogram(user_input);
	result(user_input);
	return (status);
}


/**
* result - result msg
*
* @in: input
*
* Return: void
*/
int result(const char in[])
{
	bool x = isogram_prompt();

	if (x)
	{
		printf("The input: %s, is an isogram.\n", in);
	}
	else
	{
		printf("The input: %s, is not an isogram.\n", in);
	}
}
