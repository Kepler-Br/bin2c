# bin2c

Convert any binary file or stdin into c style array with this script.  
Inspired by  [James Swineson's](https://github.com/Jamesits) [repository](https://github.com/Jamesits/bin2array) but turned out to be completely rewritten.  
**Warning:** this script will implicitly change trailing `/\` at the end of comment block to `.` so C preprocessor would not escape new line.  

## What you'll need

Python 3.6  
If you remove type hinting, version might be even lower.

## Usage
```
usage: bin2c.py [-h] [-i INPUT_FILE] [-o OUTPUT] [-m MAX_SYMBOLS]
                [-L LINEBREAK_STRING] [-S SEPARATOR_STRING]
                [-H ELEMENT_PREFIX] [-T ELEMENT_SUFFIX] [-U] [-n] [-c]
                [-C COMMENT_STRING] [-s]

Convert binary file to C-style array initializer.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        the file to be converted. If not specified, stdin is
                        used.
  -o OUTPUT, --output OUTPUT
                        write output to a file
  -m MAX_SYMBOLS, --max-symbols MAX_SYMBOLS
                        max symbols in the line, defaults to 80
  -L LINEBREAK_STRING, --linebreak-string LINEBREAK_STRING
                        use what to break link, defaults to "\n"
  -S SEPARATOR_STRING, --separator-string SEPARATOR_STRING
                        use what to separate elements, defaults to ", "
  -H ELEMENT_PREFIX, --element-prefix ELEMENT_PREFIX
                        string to be added to the head of element, defaults to
                        "0x"
  -T ELEMENT_SUFFIX, --element-suffix ELEMENT_SUFFIX
                        string to be added to the tail of element, defaults to
                        none
  -U, --force-uppercase
                        force uppercase HEX representation
  -n, --newline         add a newline on file end
  -c, --write-comments  write text representation of the data
  -C COMMENT_STRING, --comment-string COMMENT_STRING
                        what to use as begin of comment block, defaults to "//
                        "
  -s, --size            print array length in the end. May lie if you close
                        stdout on the other end
```

## Output example:

```
0x23, 0x21, 0x2f, 0x75, 0x73, 0x72, 0x2f, 0x62, 0x69, 0x6e, 0x2f, // #!/usr/bin/
0x65, 0x6e, 0x76, 0x20, 0x70, 0x79, 0x74, 0x68, 0x6f, 0x6e, 0x33, // env python3
0x0a, 0x69, 0x6d, 0x70, 0x6f, 0x72, 0x74, 0x20, 0x62, 0x69, 0x6e, // .import bin
0x61, 0x73, 0x63, 0x69, 0x69, 0x0a, 0x69, 0x6d, 0x70, 0x6f, 0x72, // ascii.impor
```
