#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int main(int ac, char *av[])
{
	int y = atoi(av[1]);
	int x;
	int i = 0;

	(void)ac;

	if (y < 0)
		y += 24;
	x = y % 24;

	if (x < 10 && x != 0)
		printf("The hour is 0%d\n", x);

	else if (x > 9 && x != 0)
		printf("The hour is %d\n", x);
	else
		printf("The hour is 0%d\n", i);

	return (0);
}
