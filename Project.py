# Final Project
# Created by Zachary Roth for CS1800. 4/20/21
# This program will take in a text file and create a square image of pixels, visualizing the hexadecimal content inside the text.

# Import needed modules
import math
from PIL import Image
import numpy as np

# List definining valid hexadecimal characters.
hex_digit_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f']

# Adjust scale of darkened variant. Can be changed, but must be between 0 and 1.
brightness = .75

# Loop through string, in this case the entire text, and append given character to list if it is a valid hexadecimal digit.
def get_hex_list():
    hex_list = []

    for x in text:
        if (x in hex_digit_list):
            hex_list.append(x)

    return hex_list

# Loop through list of hexadecimals, convert each digit to its decimal digit equivalent.
def hex_to_decimal_list(hex_list):
    decimal_list = []
    switcher = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, # This is essentially a switch case, with the associated decimal value for a hex digit.
                'A': 10, 'a': 10,
                'B': 11, 'b': 11,
                'C': 12, 'c': 12,
                'D': 13, 'd': 13,
                'E': 14, 'e': 14,
                'F': 15, 'f': 15}

    for x in hex_list:
        decimal_list.append(switcher.get(x))

    return decimal_list

# Using a selection sort algorithm, sort a list of numbers in descending order.
def selection_sort_descending(num_list):
    for x in range(len(num_list)):
        max_index = x

        for y in range(x+1, len(num_list)):
            if (num_list[max_index] < num_list[y]):
                max_index = y

        temp = num_list[x] # Swap operation
        num_list[x] = num_list[max_index]
        num_list[max_index] = temp

    return num_list
                  
# Using an insertion sort algorithm, sort a list of numbers in ascending order.
def insertion_sort_ascending(num_list):
    for x in range(1, len(num_list)):

        while (x > 0) and (num_list[x] < num_list[x - 1]):
            temp = num_list[x]
            num_list[x] = num_list [x - 1] # Swap operation
            num_list[x - 1] = temp
            x = x - 1

    return num_list
        
# Create an "eight bit" list - take every two decimal representations of hexadecimals and calculate their decimal equivalent.
# Example: 6, 13 = 6D = 6*16 + 13 = 109
def decimal_to_eightbit_list(decimal_list):
    eightbit_list = []

    if ((len(decimal_list) % 2) != 0): # If list is odd length,
        decimal_list = decimal_list[:len(decimal_list)-1] # Remove last element

    for x in range(0, len(decimal_list), 2):    
        eightbit_list.append((16*decimal_list[x]) + decimal_list[x+1])

    return eightbit_list

# Multiply each 8-bit value by a number between 0 and 1 to decrease brightness of image.
def darken_eightbits(eightbit_list):
    darkened_bits = []

    for x in eightbit_list:
        x = round(x * brightness) 
        darkened_bits.append(x)

    return darkened_bits
            
def create_pixel_array(eightbit_list):
    if ((len(eightbit_list) % 3) != 0): # If list of eight bit characters is not a multiple of three,
        eightbit_list = eightbit_list[:(3 * (math.floor(len(eightbit_list) / 3)))] # Make list of eight bit characters divisible by three by removing extra elements.

    array = [eightbit_list[x:x+3] for x in range(0, len(eightbit_list), 3)] # Divide list into list of 3 grouped 8 bits.

    window_dimension = math.floor(math.sqrt(len(array))) # Dimensions of image 
    
    array = array[:pow(window_dimension, 2)] # Omit extra 24 bit elements to make perfect square array of pixels.
    array = [array[x:x+window_dimension] for x in range(0, len(array), window_dimension)] # Reshape array to a square array that can be read by the program.
    array = np.array(array, dtype=np.uint8) # Make array in proper array data format.
    return array

# Ask user to input file name.
print("Please input valid text filename (including .txt extension) that you would like to visualize.")
filename = input()
print("Loading...") # The below sorting algorithms, when given large inputs, can become quite intensive, and may need some time to compute. This is explained by insertion and selection sorts being O(n^2)
file = open(filename, "r")
name = filename[:len(filename)-4]
text = file.read()
file.close()

# Creating decimal lists from hexidecimal lists for an unsorted, sorted by descending selection sort, sorted by ascending insertion
hexlist = get_hex_list()
declist = hex_to_decimal_list(hexlist)
selection_declist = selection_sort_descending(declist[:])
insertion_declist = insertion_sort_ascending(declist[:])

unsorted_eightbit_list = decimal_to_eightbit_list(declist)
selection_eightbit_list = decimal_to_eightbit_list(selection_declist)
insertion_eightbit_list = decimal_to_eightbit_list(insertion_declist)
darkened_unsorted_eightbit_list =  darken_eightbits(unsorted_eightbit_list[:])

unsorted_pixel_array = create_pixel_array(unsorted_eightbit_list)
selection_sorted_pixel_array = create_pixel_array(selection_eightbit_list)
insertion_sorted_pixel_array = create_pixel_array(insertion_eightbit_list)
unsorted_darkened_pixel_array = create_pixel_array(darkened_unsorted_eightbit_list)

# Create and save images based on RGB array values for each 

image_unsorted =  Image.fromarray(unsorted_pixel_array)
image_unsorted.save('{}-unsorted.png'.format(name))

image_selection =  Image.fromarray(selection_sorted_pixel_array)
image_selection.save('{}-selection-sort.png'.format(name))

image_insertion =  Image.fromarray(insertion_sorted_pixel_array)
image_insertion.save('{}-insertion-sort.png'.format(name))

image_darkened = Image.fromarray(unsorted_darkened_pixel_array)
image_darkened.save('{}-darkened.png'.format(name))
print("Done.")
k = input("Press enter to exit.")
        
    
    
    
    
    



