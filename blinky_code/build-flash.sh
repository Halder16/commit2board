#!/bin/bash

make clean
make


st-flash write build/not_first_blinky.bin 0x8000000