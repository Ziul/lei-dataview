 #unlinks the symbolic links of the pseudoterminals
echo "unlinking the ttyUSBs..."
 sudo unlink /dev/ttyUSB$1
 sudo unlink /dev/ttyUSB$2
echo "done, see: ls /dev/ttyUSB*"
ls /dev/ttyUSB*
echo "killing socat..."
sudo killall socat
echo "done."