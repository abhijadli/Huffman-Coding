""" Implementation of huffman coding 

Steps:
1. Read text from file.
2. Make a frequency hashmap for the present text.
3. Build heap for the frequency data.
4. Build tree from the heap.
5. Build codes for elements.
6. Encode the text with created codes.
7. Pad the text with zeroes to make multiple of 8 bits
8. Convert codes into bytes.
"""
import heapq
import os


# Structure of a binary tree node
class BinaryTreeNode:
    # Constructor
    def __init__(self, value, freq) -> None:
        self.value = value
        self.freq = freq
        self.left = self.right = None

    # Magic methods
    def __eq__(self, __value: object) -> bool:
        return self.freq == __value.freq

    def __lt__(self, __value: object) -> bool:
        return self.freq < __value.freq


# Implementation of huffman coding
class HuffmanCoding:
    # Constructor
    def __init__(self, path) -> None:
        self.path = path
        # Empty heap
        self.__heap = []
        # Empty dictionary for storing codes for compression
        self.__codes = {}
        # Empty decitionary to store reverse codes for decompression
        self.__reverse_codes = {}

    # Frequency dictionary
    def __buildFrequencyDictionary(self, text):
        # Empty frequency dictionary
        freq_dict = {}
        # Traverse through text
        for char in text:
            # Create entry in dictionary if not there
            if char not in freq_dict:
                freq_dict[char] = 0
            # Increment in dictionary if there
            freq_dict[char] += 1
        # Return that dictionary
        return freq_dict

    # Build heap from data
    def __buildHeap(self, freq_dict):
        # Access key value pairs in dictionary
        for key in freq_dict:
            # Create a new binary tree node
            node = BinaryTreeNode(key, freq_dict[key])
            # Push into heap array
            self.__heap.append(node)
        # Heapify the array to create a min heap
        heapq.heapify(self.__heap)

    # Build tree from heap
    def __buildTree(self):
        # Till only one value remains in heap
        while len(self.__heap) > 1:
            # Get two nodes with least frequency
            node1 = heapq.heappop(self.__heap)
            node2 = heapq.heappop(self.__heap)
            # Calculate sum of their frequencies
            freq_sum = node1.freq + node2.freq
            # Create a new binary tree node with no key but with sum of frequencies
            newNode = BinaryTreeNode(None, freq_sum)
            # Make connections with left and right nodes
            newNode.left = node1
            newNode.right = node2
            # Push the new node into the heap
            heapq.heappush(self.__heap, newNode)
        # Return None when done
        return

    # Create codes helper function
    def __buildCodesHelper(self, root, bits_string):
        if root is None:
            return
        if root.value is not None:
            # Store codes for compression
            self.__codes[root.value] = bits_string
            # Store reverse codes for decompression
            self.__reverse_codes[bits_string] = root.value
            return
        # Recursively build codes for left and right leaf nodes
        self.__buildCodesHelper(root.left, bits_string + "0")
        self.__buildCodesHelper(root.right, bits_string + "1")

    # Create code main function
    def __buildCodes(self):
        # Last value of the heap will be the root of the tree
        root = heapq.heappop(self.__heap)
        # Call helper function to create codes
        self.__buildCodesHelper(root, "")

    # Function to encode text from the codes build
    def __encodeText(self, text):
        # Empty string to store encoded text
        encoded_text = ""
        # Traverse through the text
        for char in text:
            # Use codes dictionary to get codes and add them to the string
            encoded_text += self.__codes[char]
        # Return that encoded text
        return encoded_text

    # Padding the encoded text
    def __padText(self, encoded_text):
        # Calculate the paddin amount
        pad_amount = 8 - (len(encoded_text) % 8)
        # Add zeroes to encoded text
        for i in range(pad_amount):
            encoded_text += "0"
        # Create pad info which will be having 8 bits
        padded_info = "{0:08b}".format(pad_amount)
        # Return concatenation of pad info and encoded text
        return padded_info + encoded_text

    # Get bytes array out of padded encoded text
    def __getBytesArray(self, padded_info_text):
        # Empty array to store bytes
        array = []
        # Traverse the padded text with a step of 8
        for i in range(0, len(padded_info_text), 8):
            # Store each 8 length text in a variable
            byte = padded_info_text[i : i + 8]
            # Append that to the array
            array.append(int(byte, 2))
        # Return the array
        return array

    # Main function to compress the text file given
    def compress(self):
        # Get file name and extension from the path
        file_name, file_extension = os.path.splitext(self.path)
        # Create output file name
        output_path = file_name + ".bin"
        # Open bith input and output file
        # Input file in read mode, output file in write as bytes mode
        with open(self.path, "r+") as file, open(output_path, "wb") as output:
            # Read text from the file
            text = file.read()
            text = text.rstrip()
            # Make frequency dictionary from text
            freq_dict = self.__buildFrequencyDictionary(text)
            # Build heap for the frequency data.
            self.__buildHeap(freq_dict)
            # Build tree from the heap.
            self.__buildTree()
            # Build codes for elements.
            self.__buildCodes()
            # Encode the text with created codes.
            encoded_text = self.__encodeText(text)
            # Pad the text with zeroes to make multiple of 8 bits
            final_padded_text = self.__padText(encoded_text)
            # Convert codes into bytes
            bytes_array = self.__getBytesArray(final_padded_text)
            # Get final bytes array using inbuilt function
            final_bytes = bytes(bytes_array)
            # Write the final bytes array into output file
            output.write(final_bytes)
        # Print compressed and return the output path
        print("Compressed")
        return output_path

    # Remove padding from encoded text
    def __removePadding(self, text):
        # First 8 bits represents padded info
        padded_info = text[0:8]
        # Convert extra padding into number
        extra_padding = int(padded_info, 2)
        # Get remaining text
        text = text[8:]
        # Remove extra padding from slice and return
        text_after_padding_removal = text[0 : -1 * extra_padding]
        return text_after_padding_removal

    # Decode unpadded text
    def __decodeText(self, text):
        # Initialize variable decoded text and bits
        decoded_text = ""
        current_bits = ""
        # Traverse through text
        for bit in text:
            # Get reverse codes
            current_bits += bit
            # IF reverse codes available, add to decoded text and start again
            if current_bits in self.__reverse_codes:
                char = self.__reverse_codes[current_bits]
                decoded_text += char
                current_bits = ""
        # Return final decoded text
        return decoded_text

    # Decompress the compressed file
    def decompress(self, input_path):
        # Get file name and extension from the path
        file_name, file_extension = os.path.splitext(input_path)
        # Create output file name
        output_path = file_name + "_decompressed.txt"

        # Open both input and output file
        # Input file in read binary mode, output file in write mode
        with open(input_path, "rb") as file, open(output_path, "w") as output:
            # Initialize an empty string to store the bits
            bit_string = ""

            # Read each byte one by one from the compressed file
            byte = file.read(1)

            # Convert byte to bits and concatenate to the bit string
            while byte:
                # Convert the byte to its integer representation
                byte = ord(byte)
                # Convert the integer to a binary string representation
                bits = bin(byte)[2:].rjust(8, "0")
                # Concatenate the bits to the bit string
                bit_string += bits
                # Read the next byte
                byte = file.read(1)

            # Get the actual text by removing the padding from the bit string
            actual_text = self.__removePadding(bit_string)

            # Decompress the file by decoding the text using Huffman codes
            decompressed_text = self.__decodeText(actual_text)

            # Write the decompressed text to the output file
            output.write(decompressed_text)


path = "D:\Abhishek-Important\Personal development\Coding Ninjas course\Data structures and algorithms\huffman_coding\sample.txt"
h = HuffmanCoding(path)
output_path = h.compress()
h.decompress(output_path)
