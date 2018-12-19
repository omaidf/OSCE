#!/bin/bash

function reverseBytes() {
    echo -n "$1" | sed 's/\(..\)/ \\x\1/g' | awk '{print $4$3$2$1}'
}

function hexing() {
    echo -n "$1" | sed 's/\(..\)/\\x\1/g'
} 

function help {
	echo "-s: calculate space between 2 memory address"
	echo "-c: add or subtract bytes from memory address"
	echo "-h: convert dec to hex"
	echo "-d: convert hex to dec"
	echo "-b: Convert hex to binary"
	echo "-r: reverse bytes"
	echo "-v: Convert memory address to \x00\x00"
	echo ""
	echo "Usage: $0 -s 00121978 00121902"
	echo "Usage: $0 -c 00121978 58 -"
	echo "Usage: $0 -c 00121978 58 +"
	echo "Usage: $0 -h 58"
	echo "Usage: $0 -d 0x3A"
	echo "Usage: $0 -b 55554D66"
	echo "Usage: $0 -r 776f6f74"
	echo "Usage: $0 -v 776f6f74"
	

	exit
}

function size() {
	M1=$(printf "%d" 0x$1)
	M2=$(printf "%d" 0x$2)
	if [[ $M1 > $M2 ]]; then
		true
	else
		false
	fi
}
case "$1" in

	-s) 
		MEM1=$2
		MEM2=$3
		if [[ ! -z $MEM1 ]] || [[ ! -z $MEM2 ]]; then
			MEM1=${MEM1:2}
			MEM2=${MEM2:2}
			if size $MEM1 $MEM2; then
				echo "Calculating space between 00$MEM1 and 00$MEM2 memory addresses:"
				printf "0x%X" $((0x$MEM1 - 0x$MEM2)) | xargs printf "%d" ;echo " bytes" 
				printf "0x%X Hex\n" $((0x$MEM1 - 0x$MEM2))  
			else
				echo "Calculating space between 00$MEM2 and 00$MEM1 memory addresses:"
				printf "0x%X" $((0x$MEM2 - 0x$MEM1)) | xargs printf "%d" ;echo " bytes"
				printf "0x%X Hex\n" $((0x$MEM2 - 0x$MEM1)) 
			fi
		else
			help
		fi
    		;;
	-c) 
		MEM1=$2
		OFFSET=$3
		SUBADD=$4
		if [[ ! -z $OFFSET ]] && [[ ! -z $MEM1 ]] && [[ ! -z $SUBADD ]]; then
			echo "Calculating expected memory address:" 
    			printf "00%X\n" $(( 0x$MEM1 $SUBADD $OFFSET ))
		else
			help
		fi
		;;
	-b)
		echo "ibase=16; obase=2; "${2}  | bc -l
		;;
	-h)
		VAL=$2
		if [[ ! -z $VAL ]]; then
			echo "Convert $VAL to hex:"
			printf "0x%X\n" $(($VAL))
	
		fi
		;;	
	-d)
		VAL=$2
		if [[ ! -z $VAL ]]; then
			echo -n "Convert $VAL to dec: "
			if [[ $VAL == "0x"* ]] || [[ $VAL == "0X"* ]]; then
				M=`printf "%d\n" $(($VAL))`
				echo $M 
				echo "For short JMP use: $((M -2))"
			else
				M=`printf "%d\n" $((0x$VAL))`
				echo $M
				echo "For short JMP use: $((M -2))"
				
			fi
	
		fi
		;;	
	-r)
		REV=$2
		reverseBytes $REV	
		;;
	-v)
		hexing $2
		;;
	*)
		help
esac

