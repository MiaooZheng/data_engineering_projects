import pprint
import matplotlib
import matplotlib.pyplot as plt
import numpy as np



text = 'gvzmyfhhebpwauvgvdnqvbohojcmlnvhcixxwntrrwialvzdtibtohouihaxzwiddbqjrbrzvtonzgidfqjndrbosgrzdvobbvpvnqddsfzvnnbtdgxbfvnmrwitrraddcgcabvnqfsongjfsatdnsgmvnnvhracacomonbotrnhrecucplnictaqrtvr'

def count_frequency_sIndco(text):
    # follows the order from a to z
    alph = "abcdefghijklmnopqrstuvwxyz"
    letterCounts = []
    for i in range(len(alph)):
        count = 0
        for j in text:
            if j == alph[i]:
                count += 1
        letterCounts.append(count)  
    # print(letterCounts)
    total = 0
    for i in range(len(letterCounts)):
        ni = letterCounts[i]
        total += ni * (ni - 1)
    # print(total)
    N = len(text)
    Indco = 1/(N*(N-1))*total
    return Indco

# split s up into m different substrings as per Vigenere
def split(s,m):
    return([s[ii::m] for ii in range(m)])


def break_string_find_keylength(text, max_key_length = 30):
    org_Indco= count_frequency_sIndco(text)
    max_key_length = max_key_length
    if org_Indco < 0.6:
        print("We're going to break the text into k pieces!")
        # key has at least 2 length
        for x in range(1, max_key_length + 1): 
            try:
                subtotal =0
                pieces = split(text, x)
                print(x)
                for piece in pieces:
                    subtotal += count_frequency_sIndco(piece)
                mean_Indco = subtotal/len(pieces)
                print(x,mean_Indco)
                print('-----------------')
            except:
                pass
    else:
        print("You can use simple substitution English to decrypt the text!")
    
def get_substring_split_by_k(k):
    substring_list=[]
    pieces = split(text, k)
    for i in range(len(pieces)):
        substring_list.append(pieces[i])
        print(f"s{i+1}: {pieces[i]}")
    return substring_list

def frequency_analysis(key_length):
    alph = "abcdefghijklmnopqrstuvwxyz"
    english_frequency = [0.0815, 0.0144, 0.0276, 0.0379, 0.1311, 0.0292, 0.0199, 0.0526, 0.0635, 0.0013, 0.0042, 0.0339, 0.0254, 0.0710, 0.08, 0.0198, 0.00012, 0.0683, 0.0610, 0.1047, 0.0246, 0.0092, 0.0154, 0.0017, 0.0198, 0.0008]
   


    substring_list = get_substring_split_by_k(key_length)
    shift_list = []
    for substring in substring_list:
        letter_count_dict = {}
        for i in range(len(alph)):
            count = 0
            for j in substring:
                if j == alph[i]:
                    count += 1
            letter_count_dict[alph[i]] = count
        # print(letter_count_dict)
        letter_frequency ={}
        for letter_count in letter_count_dict:
            # print(letter_count)
            letter_frequency[letter_count] = letter_count_dict[letter_count]/len(substring)
        # print(letter_frequency)
        # e is the most frequent letter in English
        for i in range(key_length):
            max_freq = 0
            max_letter = ""
            for j in range(26):
                if list(letter_frequency.values())[j] > max_freq:
                    max_freq = list(letter_frequency.values())[j]
                    max_letter = chr(j + ord('a'))
        shift = ord(max_letter) - ord('e')
        shift_list.append(shift)
    return shift_list
       

def decrypt(ciphertext, keyword, key_length):
    # first, we still need to convert letter to digit, so we can shift and get plaintext
    keyword_to_digit = [ord(i) for i in keyword]
    ctext_to_digit= [ord(i) for i in ciphertext]
    plaintext = ''
    for i in range(len(ctext_to_digit)):
        value = (ctext_to_digit[i] - keyword_to_digit[i % key_length]) % 26
        plaintext += chr(value + 65)
    return plaintext


split_string = get_substring_split_by_k(k=5)
# k1 = shift(split_string[0], -(ord('r')-ord('e')))

# print(decrypt(ciphertext = text, key='novak'))
shift_list = frequency_analysis(key_length=5)
print(shift_list)
# we get the corresponding key letter: NYZJK as a keyword

print(decrypt(ciphertext = text, keyword = 'NYZJK', key_length = 5))
