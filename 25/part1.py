INPUT_FILE = r'input_file.txt'

def iterate_input_file_lines(input_file=INPUT_FILE):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            yield line.replace('\n', '')

def char_to_multiplier(character):
    return {
        '=':-2,
        '-':-1,
        '0':0,
        '1':1,
        '2':2,
    }[character]

def base5_to_snafu(base5_num):
    return {
        0:'0',
        1:'1',
        2:'2',
        3:'1=',
        4:'1-',
    }[base5_num]
    
def dec_to_snafu(dec_num):
    result, remainder = divmod(dec_num, 5)
    remainder_snafu = base5_to_snafu(remainder)
    if result==0: return remainder_snafu
    return dec_to_snafu(result+len(remainder_snafu)-1) + remainder_snafu[-1]

def snafu_to_dec(snafu_digit):
    if not snafu_digit:
        return 0
    return 5*snafu_to_dec(snafu_digit[:-1]) + char_to_multiplier(snafu_digit[-1])

def main():
    print(dec_to_snafu(sum([snafu_to_dec(line) for line in iterate_input_file_lines()])))

if __name__=='__main__':
    main()