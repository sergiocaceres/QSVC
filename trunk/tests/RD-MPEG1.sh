#!/bin/bash

# Calcula un punto de la curva RD y lo envía a la salida estándar.

VIDEO=mobile_352x288x30x420x300
PICTURES=33
Y_DIM=288
X_DIM=352
FPS=30
Q_SCALE=20
GOP_SIZE=32
TIME=`echo "$PICTURES/$FPS" | bc -l`

usage() {
    echo $0
    echo "  [-v video file name ($VIDEO)]"
    echo "  [-p pictures to compress ($PICTURES)]"
    echo "  [-x X dimension ($X_DIM)]"
    echo "  [-y Y dimension ($Y_DIM)]"
    echo "  [-f frames/second ($FPS)]"
    echo "  [-q quantization scale ($Q_SCALE)]"
    echo "  [-g GOP size ($GOP_SIZE)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "v:p:x:y:f:q:g:?" opt; do
    case ${opt} in
	v)
	    VIDEO="${OPTARG}"
	    ;;
	p)
	    PICTURES="${OPTARG}"
	    ;;
	x)
	    X_DIM="${OPTARG}"
	    ;;
	y)
	    Y_DIM="${OPTARG}"
	    ;;
	f)
	    FPS="${OPTARG}"
	    ;;
	q)
	    Q_SCALE="${OPTARG}"
	    ;;
	g)
	    GOP_SIZE="${OPTARG}"
	    ;;
	?)
            usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -${OPTARG}" >&2
            usage
            exit 1
            ;;
        :)
            echo "Option -${OPTARG} requires an argument." >&2
	    usage
            exit 1
            ;;
    esac
done

set -x

ffmpeg -y -s ${X_DIM}x${Y_DIM} -i $DATA/$VIDEO.yuv -vcodec mpeg1video -g $GOP_SIZE -qscale $Q_SCALE -vframes $PICTURES 1.avi
echo "ffmpeg -y -s ${X_DIM}x${Y_DIM} -i $DATA/$VIDEO.yuv -vcodec mpeg1video -g $GOP_SIZE -qscale $Q_SCALE -vframes $PICTURES 1.avi" >> trace
CODESTREAM_BYTES=`wc -c < 1.avi`
rate=`echo "$CODESTREAM_BYTES*8/$TIME/1000" | bc -l`
ffmpeg -y -i 1.avi 1.yuv
rm 1.avi
# Hacemos que la primera imagen de la secuencia descomprimida sea
# igual a a segunda porque ffmpeg inexplicablemente, para este
# número de imágenes, no genera la imagen 0 en la salida.
FRAME_SIZE=`echo "${X_DIM}*${Y_DIM}" | bc` 
dd if=1.yuv of=1 bs=`echo "($FRAME_SIZE*3)/2" | bc` count=1
cat 1.yuv >> 1
mv 1 1.yuv
RMSE=`snr --file_A=$DATA/$VIDEO.yuv --file_B=1.yuv 2> /dev/null | grep RMSE | cut -f 3`
rm 1.yuv
echo -e $rate'\t'$RMSE
#mplayer 1.yuv -demuxer rawvideo -rawvideo w=352:h=288 > /dev/null 2> /dev/null

set +x
