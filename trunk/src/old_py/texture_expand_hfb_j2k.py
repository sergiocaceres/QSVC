#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import math
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

file = ""
rate = 0.0
pictures = 33
pixels_in_x = 352
pixels_in_y = 288

parser = MCTF_parser(description="Expands the the HFB texture data using JPEG 2000.")
parser.add_argument("--file", help="file that contains the LFB data. Default = {})".format(file))
parser.add_argument("--rate", help="read only the initial portion of the code-stream, corresponding to an overall bit-rate of \"rate\" bits/sample. Default = {})".format(rate))
parser.pictures(pictures)
parser.pixels_in_x(pixels_in_x)
parser.pixels_in_y(pixels_in_y)

args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.rate:
    rate = float(args.rate)
if args.pictures:
    pictures = int(args.pictures)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)


# Decode YUV
image_number = 0
while image_number < pictures:

    #####
    # Y #
    try: # Jse. Sino existe se crea a movimiento lineal. # no se comprueba si existe el H_maximo donde apoyar dicho movimiento.
        f = open(file + "_Y_" + str('%04d' % image_number) + ".j2c", "rb")
        f.close()

        try: # expand
            if rate <= 0.0 :
                check_call("trace kdu_expand"
                           + " -i " + file + "_Y_" + str('%04d' % image_number) + ".j2c"
                           + " -o " + file + "_Y_" + str('%04d' % image_number) + ".raw"
                           , shell=True)
            else :
                check_call("trace kdu_expand"
                           + " -i " + file + "_Y_" + str('%04d' % image_number) + ".j2c"
                           + " -o " + file + "_Y_" + str('%04d' % image_number) + ".raw"
                           + " -rate " + rate
                           , shell=True)

        except CalledProcessError:
            sys.exit(-1)

    except:
        f = open(file + "_Y_" + str('%04d' % image_number) + ".raw", "wb")
        for a in xrange(pixels_in_x * pixels_in_y):
            f.write('%c' % 128)
        f.close()

    try:
        check_call("trace cat " + file + "_Y_" + str('%04d' % image_number) + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)


    #####
    # U #
    try:
        f = open(file + "_U_" + str('%04d' % image_number) + ".j2c", "rb")
        f.close()

        try: # expand
            if rate <= 0.0 :
                check_call("trace kdu_expand"
                           + " -i " + file + "_U_" + str('%04d' % image_number) + ".j2c"
                           + " -o " + file + "_U_" + str('%04d' % image_number) + ".raw"
                           , shell=True)
            else :
                check_call("trace kdu_expand"
                           + " -i " + file + "_U_" + str('%04d' % image_number) + ".j2c"
                           + " -o " + file + "_U_" + str('%04d' % image_number) + ".raw"
                           + " -rate " + rate
                           , shell=True)

        except CalledProcessError:
            sys.exit(-1)

    except:
        f = open(file + "_U_" + str('%04d' % image_number) + ".raw", "wb")
        for a in xrange((pixels_in_x * pixels_in_y)/4):
            f.write('%c' % 128)
        f.close()

    try:
        check_call("trace cat " + file + "_U_" + str('%04d' % image_number) + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)


    #####
    # V #
    try:
        f = open(file + "_V_" + str('%04d' % image_number) + ".j2c", "rb")
        f.close()

        try: # expand
            if rate <= 0.0 :
                check_call("trace kdu_expand"
                           + " -i " + file + "_V_" + str('%04d' % image_number) + ".j2c"
                           + " -o " + file + "_V_" + str('%04d' % image_number) + ".raw"
                           , shell=True)
            else :
                check_call("trace kdu_expand"
                           + " -i " + file + "_V_" + str('%04d' % image_number) + ".j2c"
                           + " -o " + file + "_V_" + str('%04d' % image_number) + ".raw"
                           + " -rate " + rate
                           , shell=True)

        except CalledProcessError:
            sys.exit(-1)

    except:
        f = open(file + "_V_" + str('%04d' % image_number) + ".raw", "wb")
        for a in xrange((pixels_in_x * pixels_in_y)/4):
            f.write('%c' % 128)
        f.close()


    try:
        check_call("trace cat " + file + "_V_" + str('%04d' % image_number) + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)


    image_number += 1
