#include "main.h"

/* test codes for phone_number.c and hone_number_alternate.c */
static void test_cleans_the_number(void)
{
   const char input[] = "(223) 456-7890";
   const char expected[] = "2234567890";
   char *result = phone_number_clean(input);
   if (strcmp(result, expected) == 0) {
       printf("test_cleans_the_number: PASSED\n");
   } else {
       printf("test_cleans_the_number: FAILED\n");
   }
}

static void test_cleans_numbers_with_dots(void)
{
   const char input[] = "223.456.7890";
   const char expected[] = "2234567890";
   char *result = phone_number_clean(input);
   if (strcmp(result, expected) == 0) {
       printf("test_cleans_numbers_with_dots: PASSED\n");
   } else {
       printf("test_cleans_numbers_with_dots: FAILED\n");
   }
}

static void test_cleans_numbers_with_multiple_spaces(void)
{
   const char input[] = "223 456   7890   ";
   const char expected[] = "2234567890";
   char *result = phone_number_clean(input);
   if (strcmp(result, expected) == 0) {
       printf("test_cleans_numbers_with_multiple_spaces: PASSED\n");
   } else {
       printf("test_cleans_numbers_with_multiple_spaces: FAILED\n");
   }
}

static void test_invalid_when_9_digits(void)
{
   const char input[] = "123456789";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
   if (strcmp(result, expected) == 0) {
       printf("test_invalid_when_9_digits: PASSED\n");
   } else {
       printf("test_invalid_when_9_digits: FAILED\n");
   }
}

static void test_invalid_when_11_digits_does_not_start_with_a_1(void)
{
   const char input[] = "22234567890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
   if (strcmp(result, expected) == 0) {
       printf("test_invalid_when_11_digits_does_not_start_with_a_1: PASSED\n");
   } else {
       printf("test_invalid_when_11_digits_does_not_start_with_a_1: FAILED\n");
   }
}

static void test_valid_when_11_digits_and_starting_with_1(void)
{
   const char input[] = "12234567890";
   const char expected[] = "2234567890";
   char *result = phone_number_clean(input);
   if (strcmp(result, expected) == 0) {
       printf("test_valid_when_11_digits_and_starting_with_1: PASSED\n");
   } else {
       printf("test_valid_when_11_digits_and_starting_with_1: FAILED\n");
   }
}

static void test_valid_when_11_digits_and_starting_with_1_even_with_punctuation(void)
{
   const char input[] = "+1 (223) 456-7890";
   const char expected[] = "2234567890";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
	{
		printf("PASSED\n");
	}
	else
		printf("FAILED\n");
}

static void test_invalid_when_more_than_11_digits(void)
{
   const char input[] = "321234567890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");

}

static void test_invalid_with_letters(void)
{
   const char input[] = "523-abc-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}

static void test_invalid_with_punctuations(void)
{
   const char input[] = "523-@:!-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}

static void test_invalid_if_area_code_starts_with_0(void)
{
   const char input[] = "(023) 456-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}

static void test_invalid_if_area_code_starts_with_1(void)
{
   const char input[] = "(123) 456-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}

static void test_invalid_if_exchange_code_starts_with_0(void)
{
   const char input[] = "(223) 056-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}

static void test_invalid_if_exchange_code_starts_with_1(void)
{
   const char input[] = "(223) 156-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}

static void test_invalid_if_area_code_starts_with_0_on_valid_11_digit_number(void)
{
   const char input[] = "1 (023) 456-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}

static void test_invalid_if_area_code_starts_with_1_on_valid_11_digit_number(void)
{
   const char input[] = "1 (123) 456-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}
static void test_invalid_if_exchange_code_starts_with_0_on_valid_11_digit_number(void)
{
   const char input[] = "1 (223) 056-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}

static void test_invalid_if_exchange_code_starts_with_1_on_valid_11_digit_number(void)
{
   const char input[] = "1 (123) 156-7890";
   const char expected[] = "0000000000";
   char *result = phone_number_clean(input);
	if (strcmp(result, expected) == 0)
        {
                printf("PASSED\n");
        }
        else
                printf("FAILED\n");
}


int main(void)
{
   test_cleans_the_number();
   test_cleans_numbers_with_dots();
   test_cleans_numbers_with_multiple_spaces();
   test_invalid_when_9_digits();
   test_invalid_when_11_digits_does_not_start_with_a_1();
   test_valid_when_11_digits_and_starting_with_1();
   test_valid_when_11_digits_and_starting_with_1_even_with_punctuation();
   test_invalid_when_more_than_11_digits();
   test_invalid_with_letters();
   test_invalid_with_punctuations();
   test_invalid_if_area_code_starts_with_0();
   test_invalid_if_area_code_starts_with_1();
   test_invalid_if_exchange_code_starts_with_0();
   test_invalid_if_exchange_code_starts_with_1();
   test_invalid_if_area_code_starts_with_0_on_valid_11_digit_number();
   test_invalid_if_area_code_starts_with_1_on_valid_11_digit_number();
   test_invalid_if_exchange_code_starts_with_0_on_valid_11_digit_number();
   test_invalid_if_exchange_code_starts_with_1_on_valid_11_digit_number();
   return (0);
}
