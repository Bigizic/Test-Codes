#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int ac, char *av[])
{
	int i, count = 0;
	int x = atoi(av[1]);

	(void)ac;

	while (x >= 60)
	{
		i = x - 60;
		x = i;
		count++;
	}
	printf("number of hour: %d, remainning minute: %d\n",count, x);
	return (0);
}
