#!/bin/bash
export DISPLAY=:0
wid=1920
hei=1080
echo "VNC Resolution output "
echo -e "Enter VNC output width (Default: $wid):  \c"
#If not empty, update wid
read w
if ! [ -z "$w" ]
then
  wid=$w
fi
echo -e "Enter output height (Default: $hei): \c"
read h
if ! [ -z "$h" ]
then 
  hei=$h
fi
res="$wid""x$hei"
echo "Starting VNC with $res output..."
sleep 3 #Wait 3s before starting
xrandr --fb $res
x11vnc -create
