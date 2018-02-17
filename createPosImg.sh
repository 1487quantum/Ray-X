#!/bin/sh
# [Under development]
# A script to simplify opencv sample image creation (Based on https://memememememememe.me/post/training-haar-cascades/ tutorial, step 2c)
mainpath=$PWD
IPATH="$PWD/gate_img/cropped/"
clear
while true
do
  # (1) prompt user, and read command line argument
  printf "~~ Image Merger v1.0.0 ~~\nCreation of positive training images for Haar Cascade\n\n"
  read -p "Use default image directory path? [Y/n] (Default: $IPATH)" answer

  # (2) handle the input we were given
  case $answer in
   [yY]* ) break;;

   [nN]* ) echo "Enter image directory path, followed by [ENTER]:"
	   read ipath
	   if [ ! -d "$ipath" ]; then
  		# Control will enter here if $DIRECTORY exists.
		echo "Directory does not exist! Exiting.."
		exit;
	   fi
	   IPATH=$ipath
           break;;

   * )     printf "**Please enter (Y)es or (N)o\n\n\n";;
  esac
done
printf "\nUsing path: $IPATH\n"
cd $IPATH
#Save all the images into a text file
ls -1 *.jpg > imgList.txt
#echo $PWD
#Get number of lines (or image files)
tmp="$(wc -l "$PWD/imgList.txt")"
#Remove th efile path behind
NUM=${tmp% *}
printf 'Added '"$NUM"' img file link into imgList.txt\n'
#Read imgList.txt & Split them up for image creation
while read fp; do
        echo 'Creating training images for' $fp
	fpath=''"$PWD"'/'"$fp"''				# Image to be overlayed added directory
	nameonly=${fp%.*}
	#echo $fpath
	bgpath=''"$mainpath"'/negativeImgDir/negatives.txt'			# Background image directory
	dpath=''"$mainpath"'/imgDes/'"$nameonly"'.txt'		# Directory path for description output
	#Create sample
	opencv_createsamples -img $fpath -bg $bgpath -info $dpath \
	-num 128 -maxxangle 0.0 -maxyangle 0.0 \
	-maxzangle 0.3 -bgcolor 255 -bgthresh 8 \
	-w 48 -h 48
done < ''"$PWD"'/imgList.txt'