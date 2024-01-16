# Huffman Coding Project

This project implements Huffman coding, a popular algorithm for lossless data compression. The implementation includes both compression and decompression functionalities.

## Overview

Huffman coding is a widely used algorithm for data compression. It works by assigning variable-length codes to input characters based on their frequencies of occurrence. This allows more frequent characters to be represented using shorter codes, leading to more efficient compression.

## Project Structure

- **`huffman_coding.py`**: Contains the implementation of the HuffmanCoding class.
- **`sample.txt`**: An example text file used for testing the compression and decompression.

## Usage

To compress a text file, you can use the following code:

```python
path = "path/to/your/text/file.txt"
h = HuffmanCoding(path)
output_path = h.compress()
```

To decompress a text file, you can use the following code:
```
h.decompress(output_path)
```
