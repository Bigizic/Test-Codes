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
    int count = 0, y, x, add = 0;

    while (number > 0)
    {
        x = number - 1;
        number = x;
        count++;
        if (count > 0)
        {
            y = pow(count, 2);
        }
	add += y;
    }
    printf("%d\n", add);
    return (0);
}

int main(void)
{
	sum_of_squares(5);
	return (0);
}
