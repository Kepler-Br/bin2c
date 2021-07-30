# bin2c

Convert any binary file or stdin into c style array with this script.  
Inspired by  [James Swineson's](https://github.com/Jamesits) [repository](https://github.com/Jamesits/bin2array) but turned out to be completely rewritten.  
**Warning:** this script will implicitly change trailing `/\` at the end of comment block to `.` so C preprocessor would not escape new line.  

## What you'll need

Python 3.6  
If you remove type hinting, version might be even lower.  

## Output example:

### bin2c
```
0x23, 0x21, 0x2f, 0x75, 0x73, 0x72, 0x2f, 0x62, 0x69, 0x6e, 0x2f, // #!/usr/bin/
0x65, 0x6e, 0x76, 0x20, 0x70, 0x79, 0x74, 0x68, 0x6f, 0x6e, 0x33, // env python3
0x0a, 0x69, 0x6d, 0x70, 0x6f, 0x72, 0x74, 0x20, 0x62, 0x69, 0x6e, // .import bin
0x61, 0x73, 0x63, 0x69, 0x69, 0x0a, 0x69, 0x6d, 0x70, 0x6f, 0x72, // ascii.impor
```

### bin2str
```
"\377\330\377\340\000\020JFIF\000\001\001\001\001,\001,\000\000\377\3414@Exif" \
"\000\000II*\000\010\000\000\000\013\000\016\001\002\000%\000\000\000\222\000" \
"\000\000\017\001\002\000\022\000\000\000\270\000\000\000\020\001\002\000\012" \
"\000\000\000\312\000\000\000\022\001\003\000\001\000\000\000\001\000\000\000" \
"\032\001\005\000\001\000\000\000\324\000\000\000\033\001\005\000\001\000\000"
```