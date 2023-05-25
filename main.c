#include "monty.h"
bus_t bus = {NULL, NULL, NULL, 0};

/**
* main - entry point
*
* @ac: vector counter
*
* @av: char
*
* Return: 0 if success
*/
int main(int ac, char *av[])
{
	FILE *monty_ptr;
	char *buffer;
	size_t size = 0;
	ssize_t get_line = 1;
	stack_t *stack = NULL;
	unsigned int line_number = 1;

	if (ac != 2)
	{
		fprintf(stderr, "USAGE: monty file\n");
		free(stack);
		exit(EXIT_FAILURE);
	}
	monty_ptr = fopen(av[1], "r");
	bus.file = monty_ptr;
	if (!monty_ptr)
	{
		fprintf(stderr, "Error: can't open file %s\n", av[1]);
		exit(EXIT_FAILURE);
	}
	while (get_line > 0)
	{
		buffer = NULL;
		get_line = getline(&buffer, &size, monty_ptr);
		bus.buffer = buffer;
		line_number++;

		if (get_line > 0)
			execute_opcode(&stack, line_number, buffer, monty_ptr);
		free(buffer);
	}
	_free_stack(stack);
	fclose(monty_ptr);
	return (0);
}

/**
* execute_opcode - compares op_code
*
* @stack: header to head
*
* @line_number: unsigned int type
*
* @op_code: char type
*
* Return: void
*/
void execute_opcode(stack_t **stack, unsigned int line_number, char *op_code, FILE *monty_ptr)
{
	instruction_t func[] = {
		{"push", _push},
		{"pall", _pall},
		{"pint", _pint},
		{"pop", _pop},
		{NULL, NULL}
	};

	unsigned int i = 0;
	char *code;

	code = strtok(op_code, " \n\t");
	if (code && code[0] == '#')
		return;
	bus.data = strtok(NULL, " \n\t");

	while (func[i].opcode && code)
	{
		if (strcmp(code, func[i].opcode) == 0)
		{
			func[i].f(stack, line_number);
			return;
		}
		i++;
	}
	if (code && func[i].opcode == NULL)
	{
		fprintf(stderr, "L%u: unknown instruction %s\n", line_number, code);
		fclose(monty_ptr);
		free(op_code);
		_free_stack(*stack);
		exit(EXIT_FAILURE);
	}
	return;
}

/**
* _free_stack - frees allocated memory
*
* @stack: stack_t type
*
* Return: void
*/
void _free_stack(stack_t *stack)
{
	stack_t *current;

	current = stack;
	while (stack)
	{
		current = stack->next;
		free(stack);
		stack = current;
	}
}
