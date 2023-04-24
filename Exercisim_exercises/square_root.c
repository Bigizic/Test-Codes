#include "main.h"
/* header */

/**
* square_root - prints the square root of a positive number
*
* @num: double type
*
* Description: this function takes a number and stores it in *x*
* it runs a while loop to check when *x* - *y* > 0.000001
* it updates x to x + y / 2 and updates y to num divided x
* with this method we should be able to get the square root of
* a number using the Babylonian method
*
* Return: 0
*/

double square_root(double num)
{
	double x = num;
	double y = 1;
	double tem = 0.000001;

	while (x - y > tem)
	{
		x = (x + y) / 2;
		y = num / x;
	}
	return (x);
}
