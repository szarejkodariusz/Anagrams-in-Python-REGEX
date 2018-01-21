#!/usr/bin/python
import csv
import re
import argparse
import json

default_json_file_name =  "podpowiedzi.json"
default_anagram_file_name = None

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-a', type=str, help = 'Plik anagramowy', default = default_anagram_file_name)
parser.add_argument('-o', type=str, help = 'Plik wynikowy', default = default_json_file_name)
parser.add_argument('dictionary', type=str, help='Slownik')
parser.add_argument('pattern', type=str, help='Wzorzec')
args = parser.parse_args()
dictionary_file = args.dictionary
pattern_file = args.pattern
json_file = args.o
anagram_file = args.a

# READ DICTIONARY INTO LIST
print("Wczytuję plik: " + dictionary_file)
input_data = []
with open(dictionary_file, newline='') as csvfile:
	input_data = list(csv.reader(csvfile, skipinitialspace=True, delimiter=','))

# READ FILE WITH PATTERNS
print("Wczytuję plik: " + pattern_file)
patterns_list = [line.rstrip('\n') for line in open(pattern_file)]
user_patterns = list(patterns_list)
# CREATE ANAGRAM REGEX
if args.a is not None:
	anagram_patterns = []
	for i, pattern in enumerate(patterns_list):
		str_list = list(filter(None, re.split("([\*\.])", pattern))) # Split string bettween star and dot into list of strings
		# Loop oves splited string list
		for idx, p in enumerate(str_list):
			# Change star to any character regex
			if (p == '*'):
				str_list[idx] = '.*'
			# Don't change dot and change anything else
			elif (p != '.'):
				n = len(p)
				str_list[idx] = ''
				part_regex = r'(?:(['+ re.escape(p) + r'])(?!.*\1)){' + re.escape(str(n)) + r'}'
				str_list[idx] += part_regex
		# Add end and beggin matching symbols and join list of strings ionto one string
		joined = '^' + ''.join(str_list) + '$'
		anagram_patterns.append(joined)
		#print(joined)

# FIND PATTERN IN THE POLISH DICCTIONARY
print("Szukam dopasowań...")
pattern_dic = {} # Empty dictionary

for i, x in enumerate(patterns_list):
	pattern_dic.update({x: {}}) # Creade didtionary element with empty value
	x = x.replace('*', '.*') # Transform user pattern scheme to REGEX scheme
	x = '^' + x + '$' # Add begining of the string and end of the string
	patterns_list[i] = x

for i, pattern in enumerate(patterns_list):
	r = re.compile(pattern) # Compile pattern for faster data processing
	# Loop over rows
	for row in input_data:
		matches = list(filter(r.search, row)) # Check if the pattern in the row exists
		if len(matches) != 0:
			element = {row[0]: matches} # Create dictionary element
			pattern_dic[user_patterns[i]].update(element) # Add dictrionary element to the outer dictionary

# FIND ANAGRAM PATTERN IN THE POLISH DICCTIONARY
if args.a is not None:
	print("Szukam dopasowań anagramów...")
	anagram_pattern_dic = {} # Empty dictionary
	pattern_dic = {} # Empty dictionary
	for i, x in enumerate(user_patterns):
		anagram_pattern_dic.update({x: {}}) # Creade didtionary element with empty value
		#x = x.replace('*', '.*') # Transform user pattern scheme to REGEX scheme
		#x = '^' + x + '$' # Add begining of the string and end of the string
		patterns_list[i] = x

	for i, pattern in enumerate(anagram_patterns):
		r = re.compile(pattern) # Compile pattern for faster data processing
		# Loop over rows
		for row in input_data:
			matches = list(filter(r.search, row)) # Check if the pattern in the row exists
			if len(matches) != 0:
				element = {row[0]: matches} # Create dictionary element
				anagram_pattern_dic[user_patterns[i]].update(element) # Add dictrionary element to the outer dictionary

# SAVE TO THE OUTPUT FILE
print("Zapisuję do: " + json_file)
with open(json_file, 'w') as fh:
	json.dump(pattern_dic, fh, ensure_ascii=False)
if args.a is not None:
	print("Zapisuję do: " + anagram_file)
	with open(anagram_file, 'w') as fh:
		json.dump(anagram_pattern_dic, fh, ensure_ascii=False)
