import re

def match_phone_number(pattern, phone_number):
    pattern = re.compile(pattern)

    match = pattern.match(phone_number)

    if match:
        return True
    else:
        return False\
        
pattern_chad = r'(^\+[0-9]{2}|^\+[0-9]{2}\(0\)|^\(\+[0-9]{2}\)\(0\)|^00[0-9]{2}|^0)([0-9]{9}$|[0-9\-\s]{10}$|^0[0-9]{2}-[0-9]{7,8}$)'
pattern_chad2 = r'\b(?:\+\d{2}|^\+[0-9]{2}\(0\)|^\(\+[0-9]{2}\)\(0\)|^00[0-9]{2}|^0[1-9][0-9]?[ -]?)?([0-9]{9}$|[0-9\-\s]{10}$|^0[0-9]{2}-[0-9]{7,8}$)\b'
# pattern_internet = r'(^\+[0-9]{2}|^\+[0-9]{2}\(0\)|^\(\+[0-9]{2}\)\(0\)|^00[0-9]{2}|^0)([0-9]{9}$|[0-9\-\s]{10}$)'

# Examples
base = '12267974'
base_land_3 = '5218803'
base_land_4 = '516830'

mobile_phone_numbers_correct = [
    "06"+base,
    "06-"+base,
    "06 "+base,
    "+316"+base,
    "+31 6"+base,
    "+31(0)6"+base,
]

land_line_numbers_correct = [
    "078"+base_land_3,
    "078-"+base_land_3,
    "078 "+base_land_3
]


land_line_numbers_correct = [
    "0575"+base_land_4,
    "0575-"+base_land_4,
    "0575 "+base_land_4,
    '0887702491',
    '0201748374',
]
should_be_invalid = [
    "088 - 770 2491",
    '088',
    '000',
    '000 0',
    '088 00',
]

for number in mobile_phone_numbers_correct+land_line_numbers_correct + land_line_numbers_correct + should_be_invalid:
    if match_phone_number(pattern_chad, number):
        print(f"{number} is a valid phone number.")
    else:
        print(f"{number} is not a valid phone number.")