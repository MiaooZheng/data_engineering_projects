import operator
import itertools

ciphertext = "gvzmyfhhebpwauvgvdnqvbohojcmlnvhcixxwntrrwialvzdtibtohouihaxzwi\
ddbqjrbrzvtonzgidfqjndrbosgrzdvobbvpvnqddsfzvnnbtdgxbfvnmrwitrr\
addcgcabvnqfsongjfsatdnsgmvnnvhracacomonbotrnhrecucplnictaqrtvr"
key_length = 5

# Divide the ciphertext into sections of length key_length
sections = [ciphertext[i:i+key_length] for i in range(0, len(ciphertext), key_length)]

# Create a list to store the possible key
possible_key = []

# For each section, count the occurrences of each letter
for section in sections:
    counts = [section.count(c) for c in "abcdefghijklmnopqrstuvwxyz"]
    # Create a list of expected frequencies of letters in English
    expected_frequencies = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
    # Find the letter that has the highest frequency in this section
    max_count = max(counts)
    # print(max_count)
    max_index = counts.index(max_count)
    # Find the letter that has the highest expected frequency in English
    max_expected = max(expected_frequencies)
    max_expected_index = expected_frequencies.index(max_expected)
    # Find the shift between the two letters
    shift = (max_index - max_expected_index) % 26
    possible_key.append(chr(shift + ord('A')))
    # print(shift)

# Print the possible key
print("Possible key: ", "".join(possible_key))

key_length = 5

# Generate all possible 5-letter keyword combinations
keywords = itertools.product("CDWZKYYJWZKWZXKZZXZXZJXXNZWBBWJWKXYYWN", repeat=key_length)
possible_key_list = []
for keyword in keywords:
    key = "".join(keyword)
    possible_key_list.append(key)
print(possible_key_list)

