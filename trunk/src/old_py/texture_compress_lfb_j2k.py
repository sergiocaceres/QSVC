#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import os
import sys
import display
import math
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

# NOTA: A�adir c�digo para que sea posible codificar todas las componentes juntas.

COMPONENTS = 3
BYTES_PER_COMPONENT = 1

file = ""
pictures = 33
pixels_in_x = 352
pixels_in_y = 288
quantization = 45000
subband = 4 # meterla en parametros !!!!!!!!!!!!!!!!!
SRLs = 5
nLayers = 5

parser = MCTF_parser(description="Compress the LFB texture data using JPEG 2000.")

parser.add_argument("--file", 
                    help="file that contains the LFB data. Default = {})".format(file))
parser.add_argument("--nLayers",
                    help="Number of layers. Logarithm controls the quality level and the bit-rate of the code-stream. (Default = {})".format(nLayers))
parser.pictures(pictures)
parser.pixels_in_x(pixels_in_x)
parser.pixels_in_y(pixels_in_y)
parser.quantization(quantization)
parser.SRLs(SRLs)

args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.nLayers:
    nLayers = args.nLayers
if args.pictures:
    pictures = int(args.pictures)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.quantization:
    quantization = str(args.quantization) # Jse: int->str
if args.SRLs:
    SRLs = int(args.SRLs)

dwt_levels = SRLs - 1

Y_size = pixels_in_y * pixels_in_x
U_size = V_size = Y_size / 4
YUV_size = Y_size + U_size + V_size

# Copy only the required images
try:
    check_call("trace dd" +
               " if=" + file + 
               " of=" + file + ".tmp"
               " bs=" + str(YUV_size) +
               " count=" + str(pictures),
               shell=True)
except CalledProcessError:
    sys.exit(-1)

# Encode Y
try:
    check_call("trace demux " + str(YUV_size) + " 0 " + str(Y_size)
               + " < " + file
               + ".tmp | /usr/bin/split --numeric-suffixes --suffix-length=4 --bytes="
               + str(Y_size) + " - " + file + "_Y_",
               shell=True)
except CalledProcessError:
    sys.exit(-1)

image_number = 0
while image_number < pictures:

    str_image_number = '%04d' % image_number
    image_filename = file + "_Y_" + str_image_number

    try:
        check_call("trace rawtopgm " + str(pixels_in_x) + " " + str(pixels_in_y)
                   + " < " + image_filename + " > "
                   + image_filename + ".pgm",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace kdu_compress"
                   + " -i " + image_filename + ".pgm"
                   + " -o " + image_filename + ".j2c"
#                   + " Creversible=yes" # !
#                   + " Qstep=0.0001"
                   + " -no_weights"
                   + " Clevels=" + str(dwt_levels)
                   + " -slope " + str(quantization)
                   + " Clayers=" + str(nLayers),
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    image_number += 1

# Encode U
try:
    check_call("trace demux "
               + str(YUV_size) + " " + str(Y_size) + " " + str(U_size)
               + " < " + file
               + ".tmp | /usr/bin/split --numeric-suffixes --suffix-length=4 --bytes="
               + str(U_size) + " - " + file + "_U_",
               shell=True)
except CalledProcessError:
    sys.exit(-1)

image_number = 0
while image_number < pictures:

    str_image_number = '%04d' % image_number
    image_filename = file + "_U_" + str_image_number

    try:
        check_call("trace rawtopgm "
                   + str(pixels_in_x/2) + " " + str(pixels_in_y/2)
                   + " < " + image_filename
                   + " > " + image_filename + ".pgm",shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace kdu_compress"
                   + " -i " + image_filename + ".pgm"
                   + " -o " + image_filename + ".j2c"
#                   + " Creversible=yes" # !
#                   + " Qstep=0.0001"
                   + " -no_weights"
                   + " Clevels=" + str(dwt_levels)
                   + " -slope " + str(quantization)
                   + " Clayers=" + str(nLayers),
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    image_number += 1

# Encode V
try:
    check_call("trace demux " + str(YUV_size) + " " + str(U_size+Y_size)
               + " " + str(V_size)
               + " < " + file
               + ".tmp | /usr/bin/split --numeric-suffixes --suffix-length=4 --bytes="
               + str(V_size) + " - " + file + "_V_",
               shell=True)
except CalledProcessError:
    sys.exit(-1)

image_number = 0
while image_number < pictures:

    str_image_number = '%04d' % image_number
    image_filename = file + "_V_" + str_image_number

    try:
        check_call("trace rawtopgm "
                   + str(pixels_in_x/2) + " " + str(pixels_in_y/2)
                   + " < " + image_filename
                   + " > " + image_filename + ".pgm",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace kdu_compress"
                   + " -i " + image_filename + ".pgm"
                   + " -o " + image_filename + ".j2c"
#                   + " Creversible=yes" # !
#                   + " Qstep=0.0001"
                   + " -no_weights"
                   + " Clevels=" + str(dwt_levels)
                   + " -slope " + str(quantization)
                   + " Clayers=" + str(nLayers),
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    image_number += 1

# Compute file sizes
file_sizes = open (file + ".j2c", 'w')
image_number = 0
total = 0
while image_number < pictures:

    str_image_number = '%04d' % image_number
    Ysize = os.path.getsize(file + "_Y_" + str_image_number + ".j2c")
    Usize = os.path.getsize(file + "_U_" + str_image_number + ".j2c")
    Vsize = os.path.getsize(file + "_V_" + str_image_number + ".j2c")
    size = Ysize + Usize + Vsize
    total += size
    file_sizes.write(str(total) + "\n")

    image_number += 1
