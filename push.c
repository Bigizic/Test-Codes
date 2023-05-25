#include "monty.h"

/**
* _push - pushes an element to the stack
*
* @stack: head list
*
* @line_number: unsigned int type
*
* Return: void
*/
void _push(stack_t **stack, unsigned int line_number)
{
	int i, j = 0, x = 0;

	if (bus.data)
	{
		if (bus.data[0] == '-')
			j++;
		for (; bus.data[j] != '\0'; j++)
		{
			if (bus.data[j] > 57 || bus.data[j] < 48)
				x = 1;
		}
		if (x == 1)
		{
			fprintf(stderr, "L%d: usage: push integer\n", line_number);
			fclose(bus.file);
			free(bus.buffer);
			_free_stack(*stack);
			exit(EXIT_FAILURE);
		}
	}
		else
		{
			fprintf(stderr, "L%d: usage: push integer2: %s\n", line_number, data);
			fclose(bus.file);
			free(bus.buffer);
			_free_stack(*stack);
			exit(EXIT_FAILURE);
		}
		i = atoi(bus.data);
		if (bus.lifi == 0)
			add_node(stack, i);
		else
			add_queue(stack, i);
}

void add_node(stack_t **stack, int i)
{
	stack_t *new_node, *current;

	current = *stack;

	new_node = malloc(sizeof(stack_t));
	if (new_node == NULL)
	{
		printf("ERROR\n");
		exit(0);
	}
	if (current)
		current->prev = new_node;

	new_node->n = i;
	new_node->next = *stack;
	new_node->prev = NULL;
	*stack = new_node;
}

void add_queue(stack_t **stack, int i)
{
	stack_t *new_node, *current;

	current = *stack;

	new_node = malloc(sizeof(stack_t));
	if (new_node == NULL)
	{
		printf("ERROR\n");
		exit(0);
	}
	new_node->n = i;
	new_node->next = NULL;

	if (current)
	{
		while (current->next)
			current = current->next;
	}
	if (!current)
	{
		*stack = new_node;
		new_node->prev = NULL;
	}
	else
	{
		current->next = new_node;
		new_node->prev = current;
	}
}
