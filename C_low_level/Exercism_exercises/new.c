#include "main.h"
#include <math.h>

/**
* sum_of_squares - a function that tells the sum of the squares of
* the first N natural numbers
*
* @number: unsigned int type also the N number to work on
*
* Return: sum of squares of number
*/

unsigned int sum_of_squares(unsigned int number)
{
    int count = 0, y = 0, x, add = 0;

    while (number > 0)
    {
        x = number - 1;
        number = x;
        count++;
	if (count > 0)
	{
		y = count * count;
	}
	add += y;
    }
    return (add);
}

int main(void)
{
	unsigned int x = sum_of_squares(5);
	printf("%u\n", x);
	return (0);
}
