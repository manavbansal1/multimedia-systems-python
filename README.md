# Multimedia Systems Python Projects

A collection of Python implementations for multimedia systems concepts including image processing, compression algorithms, and color space transformations.

## 📋 Table of Contents

- [Overview](#overview)
- [Projects](#projects)
  - [BMP Image Viewer](#1-bmp-image-viewer)
  - [Arithmetic Coding and DCT](#2-arithmetic-coding-and-dct)
  - [Compression and Image Processing Fundamentals](#3-compression-and-image-processing-fundamentals)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Requirements](#requirements)

## Overview

This repository contains implementations of fundamental multimedia systems algorithms and applications, including:

- BMP image parsing and manipulation
- Arithmetic coding with E1/E2 scaling
- Discrete Cosine Transform (DCT)
- Color space conversions (YCoCg to YUV)
- Dithering algorithms
- Huffman coding and entropy calculations

## Projects

### 1. BMP Image Viewer

A GUI-based BMP image viewer and editor built with Tkinter.

**Features:**
- Load and display BMP images (including 8-bit and 24-bit formats)
- Real-time brightness adjustment using YUV color space
- Image scaling with nearest neighbor interpolation
- RGB channel toggling
- Metadata display (file size, dimensions, bits per pixel)
- Multi-threaded processing for smooth performance

**Key Implementation Details:**
- RGB to YUV conversion for brightness control
- Support for color tables in palette-based images
- Handles BMP bottom-to-top row ordering
- Parallel processing using ThreadPoolExecutor

**Usage:**
```bash
python BMPParser.py
```

### 2. Arithmetic Coding and DCT

Implementation of arithmetic coding and discrete cosine transform algorithms.

**Components:**

#### Arithmetic Coding
- Standard arithmetic coding algorithm
- E1/E2 scaling operations for numerical stability
- Handles binary symbols (A and B)
- Tracks scaling operations for debugging

**Example:**
```python
[lower_bound, upper_bound, operation_list] = Q1("ABABAAA", True)
# Returns: [0.457, 0.518, ['E2', 'E1']]
```

#### Discrete Cosine Transform (DCT)
- DCT matrix generation for any size N
- 1D DCT transformation implementation
- Frequency domain analysis

**Example:**
```python
DC_mat = Q2_1(4)  # Generate 4x4 DCT matrix
coefficients = Q2_2([0, 1, 2, 3, 4])  # Transform vector
```

**Usage:**
```bash
jupyter notebook "Arithmetic Coding and DCT/Arithmetic Coding and DCT.ipynb"
```

### 3. Compression and Image Processing Fundamentals

Implementation of various compression and image processing algorithms.

**Components:**

#### Color Space Conversion
- YCoCg to YUV conversion
- Matrix-based transformation approach

#### Dithering Algorithms
- **Standard Dithering**: Expands each pixel into a 2x2 block
- **Ordered Dithering**: Applies threshold matrix for halftoning
- Support for custom dither matrices

**Example:**
```python
dither_matrix = np.array([[0, 3], [2, 1]])
dithered_image = dithering(input_image, dither_matrix)
ordered_image = ordered_dithering(input_image, dither_matrix)
```

#### Entropy and Huffman Coding
- First-order entropy calculation
- Second-order entropy (using non-overlapping pairs)
- Single-symbol Huffman coding
- 2-symbol joint Huffman coding
- Average codeword length analysis

**Key Findings:**
- Second-order entropy is typically lower than first-order entropy
- Joint Huffman coding achieves better compression for correlated data
- Experimental results show ~25-40% improvement with joint coding

**Usage:**
```bash
jupyter notebook "Compression and Image Processing Fundamentals/301606480.ipynb"
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multimedia-systems-python.git
cd multimedia-systems-python
```

2. Install required packages:
```bash
pip install numpy tkinter
```

For Jupyter notebooks:
```bash
pip install jupyter notebook
```

## Usage

### BMP Image Viewer
1. Run the application: `python BMPParser.py`
2. Click "Browse" to select a BMP file
3. Use sliders to adjust brightness and scale
4. Toggle RGB channels using checkboxes

### Jupyter Notebooks
1. Navigate to the project directory
2. Run: `jupyter notebook`
3. Open the desired notebook (.ipynb file)
4. Execute cells sequentially
5. Input files should be placed in the same directory as the notebook

## Technical Details

### Arithmetic Coding Implementation
The arithmetic coding implementation uses cumulative distribution functions (CDF) to map symbols to intervals. E1/E2 scaling prevents numerical underflow:

- **E1 Scaling**: When upper_bound ≤ 0.5, multiply both bounds by 2
- **E2 Scaling**: When lower_bound ≥ 0.5, subtract 0.5 and multiply by 2

### DCT Formula
The DCT coefficient calculation uses:

```
C(k) = α(k) * Σ[n=0 to N-1] f(n) * cos(π(2n+1)k / 2N)
```

Where α(0) = √(1/N) and α(k) = √(2/N) for k > 0

### Dithering Process
1. Normalize input image to intensity levels (0 to n²)
2. Compare each pixel value to dither matrix threshold
3. Generate binary output based on comparison

### Huffman Tree Construction
1. Build frequency map from input
2. Create priority queue of nodes
3. Merge nodes iteratively (smallest frequencies first)
4. Calculate weighted average codeword length

## Requirements

- Python 3.7+
- numpy
- tkinter (usually included with Python)
- jupyter notebook (for .ipynb files)
- math (standard library)
- heapq (standard library)
- collections (standard library)

## Project Structure

```
multimedia-systems-python/
├── BMPParser.py
├── Arithmetic Coding and DCT/
│   ├── Arithmetic Coding and DCT.ipynb
│   ├── q1_input.txt
│   ├── q2_1_input.txt
│   └── q2_2_input.txt
├── Compression and Image Processing Fundamentals/
│   ├── 301606480.ipynb
│   ├── q1_input.txt
│   ├── q2_input.txt
│   └── q3_input.txt
├── .gitignore
└── README.md
```

## Input File Formats

### Arithmetic Coding (q1_input.txt)
```
ABABAAA
```

### DCT Matrix Size (q2_1_input.txt)
```
4
```

### DCT Vector (q2_2_input.txt)
```
[55, 1, 2, 3, 4, 5, 6]
```

### YCoCg Input (q1_input.txt)
```
100,5,5
```

### Dithering Input (q2_input.txt)
```
5,266
52,5
```

### Huffman Input (q3_input.txt)
```
AABB
```

## Observations and Challenges

### Arithmetic Coding
- Main challenge: Understanding E1/E2 scaling boundaries (≤ vs < 0.5)
- Working with multiple programming languages across courses
- Ensuring numerical stability with scaling operations

### Dithering
- Successfully implemented support for any n×n dither matrix
- Key insight: Proper normalization prevents overflow
- Ordered dithering provides better visual results for certain patterns

### Huffman Coding
- Joint coding exploits symbol correlations effectively
- Second-order entropy consistently lower than first-order
- Pattern-based inputs show dramatic compression improvements
- Alternating patterns (like "ABABAB") achieve near-zero redundancy

## License

This project is part of academic coursework. Please respect academic integrity policies when using this code.

## Acknowledgments

- Course materials and assignments from multimedia systems course
- Python documentation and community resources