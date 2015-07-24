#
# This bash-scripts uses sed, wc and grep to 
# expand an IPv6 Address and check if its seems valid.
#
# Needs some review.
# Author:  Florian Streibelt <florian@f-streibelt.de>
# Date:    08.04.2012
# License: Public Domain, but please be fair and
#          attribute the original author(s) and provide
#          a link to the original source for corrections:
#          https://github.com/mutax/IPv6-Address-checks
# 
# Wrapped in function for ASMD

validate_ipv6() {
  INPUT=$1

  # fill all words with zeroes
  INPUT="$( sed  's|:\([0-9a-f]\{3\}\):|:0\1:|g' <<< "$INPUT" )"
  INPUT="$( sed  's|:\([0-9a-f]\{3\}\)$|:0\1|g'  <<< "$INPUT")"
  INPUT="$( sed  's|^\([0-9a-f]\{3\}\):|0\1:|g'  <<< "$INPUT" )"

  INPUT="$( sed  's|:\([0-9a-f]\{2\}\):|:00\1:|g' <<< "$INPUT")"
  INPUT="$( sed  's|:\([0-9a-f]\{2\}\)$|:00\1|g'  <<< "$INPUT")"
  INPUT="$( sed  's|^\([0-9a-f]\{2\}\):|00\1:|g'  <<< "$INPUT")"

  INPUT="$( sed  's|:\([0-9a-f]\):|:000\1:|g'  <<< "$INPUT")"
  INPUT="$( sed  's|:\([0-9a-f]\)$|:000\1|g'   <<< "$INPUT")"
  INPUT="$( sed  's|^\([0-9a-f]\):|000\1:|g'   <<< "$INPUT")"

  # now expand the ::
  grep -qs "::" <<< "$INPUT"
  if [ "$?" -eq 0 ]; then
    ZEROES=
    GRPS="$(sed  's|[0-9a-f]||g' <<< "$INPUT" | wc -m)"
    ((GRPS--)) # carriage return
    ((MISSING=8-GRPS))
    for ((i=0;i<$MISSING;i++)); do
            ZEROES="$ZEROES:0000"
            done

    # be careful where to place the :
    INPUT="$( sed  's|\(.\)::\(.\)|\1'$ZEROES':\2|g'   <<< "$INPUT")"
    INPUT="$( sed  's|\(.\)::$|\1'$ZEROES':0000|g'   <<< "$INPUT")"
    INPUT="$( sed  's|^::\(.\)|'$ZEROES':0000:\1|g;s|^:||g'   <<< "$INPUT")"

  fi

  # an expanded address has 39 chars + CR
  if [ $(echo $INPUT | wc -m) != 40 ]; then
    return 1
  fi
  
  return 0
}

mask2cidr() {
    nbits=0
    IFS=.
    for dec in $1 ; do
        case $dec in
            255) let nbits+=8;;
            254) let nbits+=7;;
            252) let nbits+=6;;
            248) let nbits+=5;;
            240) let nbits+=4;;
            224) let nbits+=3;;
            192) let nbits+=2;;
            128) let nbits+=1;;
            0);;
            *) echo "Error: $dec is not recognised"; exit 1
        esac
    done
    echo "$nbits"
}
