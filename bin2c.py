#!/usr/bin/env python3
import binascii
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Convert binary file to C-style array initializer.')
    parser.add_argument("-i", "--input-file", help="the file to be converted. If not specified, stdin is used.")
    parser.add_argument("-o", "--output", help="write output to a file")
    parser.add_argument("-m", "--max-symbols", type=int, default=80, help="max symbols in the line, defaults to 80")
    parser.add_argument("-L", "--linebreak-string", default="\n", help="use what to break link, defaults to \"\\n\"")
    parser.add_argument("-S", "--separator-string", default=", ",
                        help="use what to separate elements, defaults to \", \"")
    parser.add_argument("-H", "--element-prefix", default="0x",
                        help="string to be added to the head of element, defaults to \"0x\"")
    parser.add_argument("-T", "--element-suffix", default="",
                        help="string to be added to the tail of element, defaults to none")
    parser.add_argument("-U", "--force-uppercase", action='store_true', help="force uppercase HEX representation")
    parser.add_argument("-n", "--newline", action='store_true', help="add a newline on file end")
    parser.add_argument("-c", "--write-comments", action='store_true', help="write text representation of the data")
    parser.add_argument("-C", "--comment-string", default="// ",
                        help="what to use as begin of comment block, defaults to \"// \"")
    parser.add_argument("-s", "--size", action='store_true',
                        help="print array length in the end. May lie if you close stdout on the other end")
    return parser.parse_args()


def to_printable_string(content: bytes) -> str:
    result = [str()] * len(content)
    for i in range(len(content)):
        character = chr(content[i])
        character = character if character.isprintable() else '.'
        result[i] = character
    return "".join(result)


def to_hex_string(content: bytes, prefix: str, suffix: str, uppercase: bool) -> list[str]:
    result = [str()] * len(content)
    hexified_content = binascii.hexlify(content).decode("UTF-8")
    if uppercase:
        hexified_content = hexified_content.upper()
    for i in range(0, len(hexified_content), 2):
        hex_string = hexified_content[i: i + 2]
        result[i // 2] = f"{prefix}{hex_string}{suffix}"
    return result


def calculate_element_length(prefix: str, suffix: str, separator: str) -> int:
    meaningful_part_len = len('00')

    return len(prefix) + meaningful_part_len + len(suffix) + len(separator)


def replace_char_by_index(string: str, target: str, index: int) -> str:
    if index < 0 or index >= len(string):
        return string
    if len(string) == 1:
        return target
    if len(string) - 1 == index:
        return string[:index] + target
    return string[:index] + target + string[index + 1:]


def calculate_elements_per_line(element_length: int, comment_block_length: int, max_line_length: int,
                                write_comments: bool) -> int:
    comment_min_length = comment_block_length + 1
    if max_line_length <= element_length:
        return 0
    if write_comments and max_line_length <= (element_length + comment_min_length):
        return 0
    count = 0
    symbols_total = 0
    if write_comments:
        symbols_total = comment_block_length
    while (symbols_total + element_length) < max_line_length:
        symbols_total += element_length + 1
        count += 1
    return count


def main():
    args = parse_args()

    input_file = sys.stdin.buffer
    output_file = sys.stdout
    try:
        if args.input_file:
            input_file = open(args.input_file, 'rb')
    except OSError as e:
        print(f"Cannot open file '{args.input_file}': {e.strerror}", file=sys.stderr)
        exit(-1)

    try:
        if args.output:
            output_file = open(args.output, 'wb')
    except OSError as e:
        print(f"Cannot open file '{args.output}': {e.strerror}", file=sys.stderr)
        exit(-1)

    element_length = calculate_element_length(args.element_prefix, args.element_suffix, args.separator_string)
    max_elements_per_line = calculate_elements_per_line(element_length, len(args.comment_string), args.max_symbols,
                                                        args.write_comments)
    chunk_size = max_elements_per_line
    elements_wrote = 0
    try:
        for chunk in iter(lambda: input_file.read(chunk_size), b''):
            hex_strings = to_hex_string(chunk, args.element_prefix, args.element_suffix, args.force_uppercase)
            hex_string = args.separator_string.join(hex_strings)
            print(f'{hex_string}{args.separator_string}', file=output_file, end='')
            elements_wrote += len(hex_strings)
            if args.write_comments:
                printable_strings = to_printable_string(chunk)
                padding = ''
                if len(hex_strings) < max_elements_per_line:
                    padding_count = (max_elements_per_line - len(hex_strings)) * element_length
                    padding = ' ' * padding_count
                print(f'{padding}{args.comment_string}{printable_strings}', file=output_file, end='')
            print(file=output_file, end=args.linebreak_string)
        output_file.flush()
    except BrokenPipeError:
        pass
    if args.size:
        print(f"\nElements wrote: {elements_wrote}", file=sys.stderr)
    if output_file != sys.stdout:
        output_file.close()
    if input_file != sys.stdin:
        input_file.close()


if __name__ == "__main__":
    main()
