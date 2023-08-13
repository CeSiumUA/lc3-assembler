from io import TextIOWrapper
import sys

def parse_asm_file(file_descriptor: TextIOWrapper):
    pass

def main():
    if len(sys.argv) < 2:
        print('File name not provided')
        return
    file_name = sys.argv[1]
    file_desc = open(file_name, 'r')
    if file_desc:
        parse_asm_file(file_desc)
    else:
        print('File {} not found'.format(file_name))
    file_desc.close()

if __name__ == '__main__':
    main()