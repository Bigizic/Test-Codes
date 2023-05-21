#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int main(int ac, char *av[])
{
	unsigned long int y = atoi(av[1]);
	unsigned long int x;
	unsigned long int i = 0;

	(void)ac;

	x = y % 24;
	if (x < 10 && x != 0)
		printf("The hour is 0%lu\n", x);

	else if (x > 9 && x != 0)
		printf("The hour is %lu\n", x);
	else
		printf("The hour is 0%lu\n", i);

	return (0);
}
