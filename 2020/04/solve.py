#!/usr/bin/env python

import re

passports = []
passport = {}
passports.append(passport)

with open('04/input.txt') as f:
    for line in f:
        line = line.strip()

        if not line:
            passport = {}
            passports.append(passport)

            continue

        for group in line.split(' '):
            key, value = group.split(':')
            passport[key] = value

required_fields = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # 'cid',
]

def valid_number(string, digits, lower, upper):
    if len(string) != digits:
        return False
    try:
        if not lower <= int(string) <= upper:
            return False
    except:
        return False

    return True


def validpassport(passport):
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    if not valid_number(passport['byr'], 4, 1920, 2002):
        return False

    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    if not valid_number(passport['iyr'], 4, 2010, 2020):
        return False

    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if not valid_number(passport['eyr'], 4, 2020, 2030):
        return False

    # hgt (Height) - a number followed by either cm or in:
    if not passport['hgt'].endswith(('cm', 'in')):
        return False

    # If cm, the number must be at least 150 and at most 193.
    if passport['hgt'].endswith('cm'):
        if not valid_number(passport['hgt'][:-2].strip(), 3, 150, 193):
            return False
    
    # If in, the number must be at least 59 and at most 76.
    if passport['hgt'].endswith('in'):
        if not valid_number(passport['hgt'][:-2].strip(), 2, 59, 76):
            return False

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    hcl = re.compile('^\#[0-9a-f]{6}$')
    if not hcl.match(passport['hcl']):
        return False

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if not passport['ecl'] in 'amb blu brn gry grn hzl oth'.split():
        return False

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    pid = re.compile('^[0-9]{9}$')
    if not pid.match(passport['pid']):
        print(passport['pid'])
        return False

    return True

c = 0
valid = 0
for passport in passports:
    if not all(field in passport for field in required_fields):
        continue

    c += 1

    if validpassport(passport):
        valid += 1

print("Total passports", len(passports))
print("Have all fields", c)
print("Valid", valid)