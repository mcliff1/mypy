#!/bin/python
"""
From youtube DrapsTV
https://www.youtube.com/watch?v=6fPnZiTqcpc&list=PL1A2CSdiySGLtKwqBnqj9BON6QQjWkP4n&index=3&t=0s
"""

import crypt


def testPass(cryptPass, dname):
    salt = cryptPass[0:2]
    dictFile = open(dname, 'r')
    for word in dictFile.readLines():
        word = word.strip('\n')
        crypt_word = crypt.crypt(word, salt)
        if (crypt_word == crypt_pass):
            print '[*] found password {}'.format(word)
            return
    print '[-] password not found'
    return


def main():
    passwd_file = open('/etc/passwd', 'r')
    for line in passwd_file.readLines():
        if ':' in line:
            user, password, _ = line.split(':')
            print '[.] cracking password for {}'.format(user)
            test_pass(password, 'dictonary.txt')

if __name__ == '__main__':
    main()
    
