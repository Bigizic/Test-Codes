#include "main.h"
/* header */
/**
* compute - calculates hamming distance between two DNA strands
*
* @lhs: const char type
*
* @rhs: const char type
*
* Return: number of hamming distance
*/
int compute(const char *lhs, const char *rhs)
{
    unsigned int i;
    unsigned long int count;
    if (lhs == rhs)
    {
        printf("Both dna, lhs: %s and rhs: %s are alike", lhs, rhs);
        return (0);
    }
    else if (lhs == NULL || rhs == NULL)
    {
        printf("Error: enter a valid DNA");
        return (0);
    }
    else if (strlen(lhs) == 0 && strlen(rhs) == 0)
    {
        printf("Error: enter a valid DNA");
        return (0);
    }
    else if (strlen(lhs) != strlen(rhs))
    {
        printf("DNA length aren't equal");
        return (-1);
        exit(EXIT_FAILURE);
    }
    count = 0;
    for (i = 0; lhs[i] != '\0'; i++)
    {
            if (lhs[i] != rhs[i])
            {
                count++; 
            }
    }
    return (count);
}
