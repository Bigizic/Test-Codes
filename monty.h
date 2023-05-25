#ifndef _MONTY_H_
#define _MONTY_H_
#define _GNU_SOURCE

/* headers */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <errno.h>

#define UNUSED __attribute__((unused));
#define BUFFER_SIZE 1024

extern char *data;

/**
* struct stack_s - doubly linked list representation of a stack (or queue)
* @n: integer
* @prev: points to the previous element of the stack (or queue)
* @next: points to the next element of the stack (or queue)
*
* Description: doubly linked list node structure
* for stack, queues, LIFO, FIFO
*/
typedef struct stack_s
{
	int n;
	struct stack_s *prev;
	struct stack_s *next;
} stack_t;


/**
* struct instruction_s - opcode and its function
* @opcode: the opcode
* @f: function to handle the opcode
*
* Description: opcode and its function
* for stack, queues, LIFO, FIFO
*/
typedef struct instruction_s
{
	char *opcode;
	void (*f)(stack_t **stack, unsigned int line_number);
} instruction_t;


typedef struct {
	char *data;
	char *buffer;

	FILE *file;
	int lifi;
} bus_t;


/* opcode prototypes */
void _push(stack_t **stack, unsigned int line_number);
void _pall(stack_t **stack, unsigned int line_number);
void _pint(stack_t **stack, unsigned int line_number);
void _pop(stack_t **stack, unsigned int line_number);





/* function prototypes */
void execute_opcode(stack_t **stack, unsigned int line_number, char *op_code, FILE *monty_ptr);
void _free_stack(stack_t *stack);
void add_node(stack_t **stack, int i);
void add_queue(stack_t **stack, int i);


#endif
