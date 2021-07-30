#!/usr/bin/env python3
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert binary file to C-style escaped string.')
    parser.add_argument('-i', '--input-file', help='the file to be converted. If not specified, stdin is used.')
    parser.add_argument('-o', '--output', help='write output to a file')
    parser.add_argument('-m', '--max-symbols', type=int, default=80, help='max symbols in the line, defaults to 80')
    parser.add_argument('-L', '--linebreak-string', default='\n', help='use what to break link, defaults to "\\n"')
    parser.add_argument('-g', '--glue-string', default=' \\',
                        help='use what to glue string between new lines, defaults to " \\"')
    parser.add_argument('-q', '--quote-string', default='"',
                        help='use what to quote string, defaults to " (double quote)')
    parser.add_argument('-n', '--newline', action='store_true', help='add a newline on file end')
    parser.add_argument('-E', '--no-quote-escape', action='store_true', help='should escape quote symbol or not')
    parser.add_argument('-s', '--size', action='store_true',
                        help='print string length in the end. May lie if you close stdout on the other end')
    return parser.parse_args()


def to_escaped_string(content: bytes, quote_string: str, escape_quote: bool) -> list[str]:
    result = [str()] * len(content)
    escaped_quote_string = '\\' + '\\'.join(list(quote_string))
    escape_shortcut_table = {
        '\a': '\\a',
        '\b': '\\b',
        '\f': '\\f',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\v': '\\v',
        '\\': '\\\\',
        '\'': '\\\'',
        '\"': '\\"',
    }

    for i in range(len(content)):
        char = chr(content[i])
        if char in escape_shortcut_table:
            result[i] = escape_shortcut_table[char]
        elif chr(content[i]).isascii() and chr(content[i]).isprintable():
            result[i] = char
        else:
            result[i] = '\\{:03o}'.format(content[i])
        if escape_quote and result[i] == quote_string:
            result[i] = escaped_quote_string
    return result


def main():
    args = parse_args()

    input_file = sys.stdin.buffer
    output_file = sys.stdout
    try:
        if args.input_file:
            input_file = open(args.input_file, 'rb')
    except OSError as e:
        print(f'Cannot open file \'{args.input_file}\': {e.strerror}', file=sys.stderr)
        exit(-1)

    try:
        if args.output:
            output_file = open(args.output, 'wb')
    except OSError as e:
        print(f'Cannot open file \'{args.output}\': {e.strerror}', file=sys.stderr)
        exit(-1)
    chunk_size = args.max_symbols
    elements_wrote = 0
    symbols_wrote_in_line = 0
    service_symbols_length = len(args.glue_string) + len(args.quote_string) * 2
    try:
        for chunk in iter(lambda: input_file.read(chunk_size), b''):
            escaped_string = to_escaped_string(chunk, args.quote_string, not args.no_quote_escape)
            for escaped_char in escaped_string:
                if symbols_wrote_in_line + len(escaped_char) + service_symbols_length > args.max_symbols:
                    padding_count = args.max_symbols - symbols_wrote_in_line - service_symbols_length
                    padding = " " * padding_count
                    print(f'{args.quote_string}{padding}{args.glue_string}{args.linebreak_string}',
                          file=output_file, end='')
                    symbols_wrote_in_line = 0
                if symbols_wrote_in_line == 0:
                    print(args.quote_string, file=output_file, end='')
                print(escaped_char, file=output_file, end='')
                elements_wrote += 1
                symbols_wrote_in_line += len(escaped_char)
        print(args.quote_string, file=output_file, end='')
        if args.newline:
            print(args.linebreak_string, end='')
        output_file.flush()
    except BrokenPipeError:
        pass
    if args.size:
        print(f'\nElements wrote: {elements_wrote}', file=sys.stderr)
    if output_file != sys.stdout:
        output_file.close()
    if input_file != sys.stdin:
        input_file.close()


if __name__ == '__main__':
    main()
