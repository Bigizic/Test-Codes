## Files are insipred from exercism https://exercism.org

##### Most files are prompt alike i.e you receive a prompt before result of the file.

##### email: olalekanisaac75@gmail.com


## 1: Armstrong number:

### Instructions

An Armstrong number is a number that is the sum of its own digits each raised to the power of the number of digits.

For example:

    30 is not an Armstrong number, because 30 != 3^2 + 0^2 = 9

    2 is an Armstrong number, because 2 == 2^1 = 2

    370 is an Armstrong number, because 370 == 3^3 + 7^3 + 0^3 = 370

--------------------------------------------------------------------

## 2: isogram:

### Instructions

Determine if a word or phrase is an isogram

An isogram (also known as a "non-pattern word") is a word or phrase without a repeating letter, however spaces and hyphens are allowed to appear multiple times.

Examples of isograms:

    timber
    
    house
    
    stream
    
    six-year-old

The word isograms, however, is not an isogram, because the s repeats.

----------------------------------------------------------------

## 3: dna_hamming:

### Instructions

Calculate the Hamming Distance between two DNA strands.

Your body is made up of cells that contain DNA. Those cells regularly wear out and need replacing, which they achieve by dividing into daughter cells. In fact, the average human body experiences about 10 quadrillion cell divisions in a lifetime!

When cells divide, their DNA replicates too. Sometimes during this process mistakes happen and single pieces of DNA get encoded with the incorrect information. If we compare two strands of DNA and count the differences between them we can see how many mistakes occurred. This is known as the "Hamming Distance".

We read DNA using the letters C,A,G and T. Two strands might look like this:

        GAGCCTACTAACGGGAT
        CATCGTAATGACGGCCT
        ^ ^ ^  ^ ^    ^^
        
They have 7 differences, and therefore the Hamming Distance is 7.

The Hamming Distance is useful for lots of things in science, not just biology, so it's a nice phrase to be familiar with :)

### Implementation notes

The Hamming distance is only defined for sequences of equal length, so an attempt to calculate it between sequences of different lengths should not work.

---------------------------------------------------------------------------------------------------


## 4: roman_numerals:

### instructions:

Write a function to convert from normal numbers to Roman Numerals.

The Romans were a clever bunch. They conquered most of Europe and ruled it for hundreds of years. They invented concrete and straight roads and even bikinis. One thing they never discovered though was the number zero. This made writing and dating extensive histories of their exploits slightly more challenging, but the system of numbers they came up with is still in use today. For example the BBC uses Roman numerals to date their programs.

The Romans wrote numbers using letters - I, V, X, L, C, D, M. (notice these letters have lots of straight lines and are hence easy to hack into stone tablets).

		 1  => I
		10  => X
		 7  => VII

The maximum number supported by this notation is 3,999. (The Romans themselves didn't tend to go any higher)

Wikipedia says: Modern Roman numerals ... are written by expressing each digit separately starting with the left most digit and skipping any digit with a value of zero.

To see this in practice, consider the example of 1990.

In Roman numerals 1990 is MCMXC:

1000=M 900=CM 90=XC

2008 is written as MMVIII:

2000=MM 8=VIII

----------------------------------------------------------------------------

## 5: Square_root: 

### Instructions

Given a natural radicand, return its square root.

Note that the term "radicand" refers to the number for which the root is to be determined. That is, it is the number under the root symbol.

Check out the Wikipedia pages on <a href="https://en.wikipedia.org/wiki/Square_root">square root</a> and <a href="https://en.wikipedia.org/wiki/Methods_of_computing_square_roots">methods of computing square roots</a>.

Recall also that natural numbers are positive real whole numbers (i.e. 1, 2, 3 and up).

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 6: Phone_number:
### Instructions

Clean up user-entered phone numbers so that they can be sent SMS messages.

The North American Numbering Plan (NANP) is a telephone numbering system used by many countries in North America like the United States, Canada or Bermuda. All NANP-countries share the same international country code: 1.

NANP numbers are ten-digit numbers consisting of a three-digit Numbering Plan Area code, commonly known as area code, followed by a seven-digit local number. The first three digits of the local number represent the exchange code, followed by the unique four-digit number which is the subscriber number.

The format is usually represented as

		(NXX)-NXX-XXXX
where N is any digit from 2 through 9 and X is any digit from 0 through 9.

Your task is to clean up differently formatted telephone numbers by removing punctuation and the country code (1) if present.

For example, the inputs

		+1 (613)-995-0253
		613-995-0253
		1 613 995 0253
		613.995.0253
should all produce the output

		6139950253

Note: As this exercise only deals with telephone numbers used in NANP-countries, only 1 is considered a valid country code.
