#include "monty.h"

/**
* _pall - prints stack n
*
* @stack: pointer to head
*
* @line_number: line number for error
*
* Return: void
*/
void _pall(stack_t **stack, unsigned int line_number)
{
	stack_t *current = *stack;

	(void)line_number;

	while (current)
	{
		printf("%d\n", current->n);
		current = current->next;
	}
}
