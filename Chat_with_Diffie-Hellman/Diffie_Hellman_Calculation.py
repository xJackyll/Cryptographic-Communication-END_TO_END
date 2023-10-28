import random
import re


# Fuctions
def generate_random_32_digits():
    # Generate the first random digit between 1 and 9
    # and the other 31 random digits between 0 and 9
    first_digit = random.randint(1, 9)  # The first digit is not zero
    number = [str(first_digit)]
    for _ in range(31):
        number.append(str(random.randint(0, 9)))
    bignum = ''.join(number)
    return int(bignum)


# This function is used to check the message you receive is the right number for diffie hellman
def check_32_digit_number(variable):
    # Convert the variable to a string
    variable_str = str(variable)

    # Define the regular expression pattern for a 30-digit number
    pattern = r'^\d{32}$'

    # Check if the variable matches the pattern
    if re.match(pattern, variable_str):
        print("Variable is a 32-digit number")
        return True
    else:
        print("Variable is not a 32-digit number")
        return False


def pow_mod(num_to_pow, a, h):
    # Giving an intermediate number to calculate too high complicates the calculation exponentially.
    # We then perform the "mod" operation at both factors before multiplication.
    # Thanks to the distributive property we will eventually get the same result
    # A = g ** a % h
    # B ** a % h
    result = pow(num_to_pow, a, h)
    return result


def SecretNumber(rand_num_chosen):
    min_number = 10 ** 31
    a = random.randint(min_number, rand_num_chosen)
    return a
