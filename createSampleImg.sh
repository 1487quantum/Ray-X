#!/bin/sh
```
[Under development]
A script to simplify opencv sample image creation (Based on https://memememememememe.me/post/training-haar-cascades/ tutorial, combined step 2c + 2d)
[Directory tree]
Images
--(srcImgDir)
----normal
----cropped
--negativeImgDir
--sampleImgDir
----des (tmp folder)

- The target image will have the format a{id}.jpg (Example: a1.jpg)
```
#Path VAR
mainpath=$PWD
bgpath=''"$mainpath"'/negativeImgDir/negatives.txt'		# Background image directory
spath=''"$mainpath"'/sampleImgDir'				# Directory path for sample image directory
dpath=''"$spath"'/des'						# Directory path for sample image description output
IPATH="$PWD/gate_img/cropped/"					# Default path for "main" image to be overlayed
clear
while true
do
  # (1) prompt user, and read command line argument
  printf "~~ Image Merger v1.0.12 ~~\nCreation of positive training images for Haar Cascade\n\n"
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
tmp="$(wc -l "$PWD/imgList.txt")"				# Get number of lines (or image files)
NUM=${tmp% *}							# Remove the file path behind
printf 'Added '"$NUM"' img file link into imgList.txt\n'
#Read imgList.txt & Split them up for image creation
while read fp; do
        echo 'Creating training images for' $fp
	fpath=''"$PWD"'/'"$fp"''				# Image to be overlayed added directory
	nameonly=${fp%.*}
	#echo $fpath
	#Create sample
	sfpath=''"$spath"'/'"$nameonly"'.txt'			# Directory path for description output
	#Sample setting: numOfImg->300, bgcolor: 255 (white), maximum angle: 0.4 (rad?)
	opencv_createsamples -img $fpath -bg $bgpath -info $sfpath \
	-num 300 -maxxangle 0.0 -maxyangle 0.0 \
	-maxzangle 0.4 -bgcolor 255 -bgthresh 8 \
	-w 48 -h 48
done < ''"$PWD"'/imgList.txt'
#Now for step 2d
printf "Sample image Creation complete, moving to step 2d -> Merging description file for more images\n\n"
cd $spath							# Goto sampleImgDir
cat a*.txt > positives.txt					# Combine all images description into positive.txt
#Create des directory if it does not exist
if [ ! -d "$dpath" ]; then
	mkdir $dpath
fi
mv *.txt $dpath							# Create & Move all description files into a new directory (des)
tmp_i="$(ls "$spath" | wc -l )"					# Get number of image files
tmp_i=$(($tmp_i-1))						# Remove count of the directory (as ls consider directory as one item)
echo 'Number of IMG:'$tmp_i					
mv ''"$dpath"'/positives.txt' .					# Move positives.txt up one directory (where the main images are in)
#Combine the description files above into one vector file 
opencv_createsamples -info ''"$spath"'/positives.txt' -bg $bgpath \
-vec ''"$spath"'/cropped.vec' \
-num $tmp_i -w 48 -h 48
