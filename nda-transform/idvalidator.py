def validate(some_id):
    # Basic checks: len == 7, first two chars are not numbers,
    # all other chars are numbers
    if len(some_id) != 7:
        return False

    if not (some_id[0].isalpha() and some_id[1].isalpha()):
        return False

    if not all([n.isdecimal() for n in some_id[2:6]]):
        return False

    # Convert ID to array of numbers, excluding check digit
    id_array = []
    id_array.append(ord(some_id[0].upper()))
    id_array.append(ord(some_id[1].upper()))
    id_array = id_array + list(some_id[2:6])

    # Use check digit algorithm to generate correct check digit
    check_digit_array = []

    for pos in range(len(id_array)):
        check_digit_array.append(int(id_array[pos]) * (pos+1))
    check_digit = sum(check_digit_array) % 10

    # Check correct check digit against entered ID
    if int(some_id[6]) != check_digit:
        return False

    return True
