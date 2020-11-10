# Chapter4 Q1
#  Grammar:
#  <S> -> 'a' <S> 'b'
#  <S> -> 'c'
# converts to <S> -> ('a')* 'c' 'b'
#
# Graham Hopkins
#
# 21 Oct 2020
#
# From Writing Interpreters and Compilers for the Raspberry Pi Using Python
#
# By Anthony J, Dos Reis
#
import sys

tokenindex = -1
token = ''


def main():
    try:
        parser()
    except RuntimeError as emsg:
        print(emsg)


def advance():
    global token, tokenindex
    tokenindex += 1  # move tokenindex to next token
    # check for null string or end of string
    if len(sys.argv) < 2 or tokenindex >= len(sys.argv[1]):
        token = ''  # signal end by returning ''
    else:
        token = sys.argv[1][tokenindex]


def consume(expected):
    if expected == token:
        advance()
    else:
        raise RuntimeError(f'Expecting {expected}')


def parser():
    advance()  # prime token with first character
    S()  # call function for start symbol
    # test if end of input string
    if token != '':
        print('Garbage following <S>-string')


def S():
    if token == 'a':
        A()
    elif token == 'c':
        C()
    else:
        raise RuntimeError('Expecting a or c')


def A():
    while token == 'a':
        advance()
    consume('c')
    B()


def B():
    if token == 'b':
        advance()  # perform actions for production 2
    else:
        raise RuntimeError('Expecting b')

def C():
    if token == 'c':
        advance()  # perform actions for production 2
    else:
        raise RuntimeError('Expecting c')

if __name__ == '__main__':
    main()
