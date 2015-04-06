#!/usr/bin/python
# -*- coding: utf-8 -*-

# Rubén Díaz <outime@gmail.com>
# https://github.com/outime/tpb

import getpass

from classes.tpb import Tpb

INPUT_USER_MSG = 'User (e-mail or phone): '

def init():
    user = raw_input(INPUT_USER_MSG)
    while not user:
        user = raw_input(INPUT_USER_MSG)

    password = getpass.getpass()
    while not password:
        password = getpass.getpass()

    t_inst = Tpb(user, password)

    if t_inst.is_authenticated:
    	t_inst.download_photos()

if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        pass
