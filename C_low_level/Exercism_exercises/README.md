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


