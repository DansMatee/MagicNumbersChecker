# MagicNumbersChecker
This project was created to explore how file types can be identified using magic numbers and how compressed archive formats can be further classified.

Magic numbers are byte sequences within a file that help determine its true format. They are commonly used in file validation to detect cases where a file’s extension does not match its actual content.

## How it works
The program takes in a file and then does the following:
1. Gets the current file extension and checks if the extension has any aliases, if so we take the normalized version. E.g if a file has an extension of .jpeg, the system converts it from the .jpeg alias to the normalized .jpg.
2. The file gets sent to our magic_numbers_check function, which is where we compare our list of hex signatures and offsets against the files hex signature, seeing if we can identify the file type.
    - If the file is determined to be a ZIP compressed file, we run it through our detect_zip_subtype function to find out what the subtype is.
3. After identifying the real file type with the signature and offset, we return it to our program, and then check the found file type against the file extension type, if we get a mismatch, we show a warning.

## Notes
This is a PoC tool.

It can detect:
- Basic file extension spoofing
- Mismatches between file extensions and actual file formats
- Common ZIP-based subtypes (Excel Spreadsheets, Word Documents)

It does not:
- Validate full file structure
- Detect malicious payloads
- Guarantee that a file is safe

## Running the program
After downloading this repo, run the program with ``python checker.py`` and input a file path.
Example: ``input file name and extension: image.jpeg``