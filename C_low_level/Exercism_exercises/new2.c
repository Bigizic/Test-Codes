#include "main.h"

unsigned int square_of_sum(unsigned int number)
{
    int count = 0, y = 0, x, add = 0;
    int new_add;
    while (number > 0)
    {
        x = number - 1;
        number = x;
        count++;
	if (count > 0)
		y = count * 1;
	add += y;
    }

    new_add = add * add;
    return (new_add);
}

int main(void)
{
	unsigned int x =  square_of_sum(5);

	printf("%u\n", x);
	return (0);
}
