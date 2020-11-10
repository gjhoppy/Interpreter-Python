# sp.py parser
#  Grammar:
#  <S> -> <A><C>
#  <A> -> 'a' 'b'
#  <C> -> 'c' <C>
#  <C> -> 'd'
#
#
# Graham Hopkins
#
# 20 Oct 2020
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
    A()
    C()


def A():
    consume('a')
    consume('b')


def C():
    if token == 'c':
        # perform actions for production 3
        advance()
        C()
    elif token == 'd':
        # perform actions for production 4
        advance()
    else:
        raise RuntimeError('Expecting c or d')


if __name__ == '__main__':
    main()
