 #Terminal emulation script by Adam Harris
 
#create the two linked pseudoterminals
# socat -d -d pty,raw,echo=0 pty,raw,echo=0 &
rm log.log
socat -lflog.log -d -d pty,raw,echo=0 pty,raw,echo=0 &
 
# #now create symbolic links to these terminals
# sudo ln -s /dev/pts/1 /dev/ttyUSB$1
# sudo ln -s /dev/pts/2 /dev/ttyUSB$2
 
sudo python linking.py $1 $2
 
# echo""
# echo "setting permissions..."
# sudo chmod 666 /dev/ttyUSB$1
# sudo chmod 666 /dev/ttyUSB$2
 
echo""
echo "symbolic links created, see for yourself:"
ls /dev/ttyUSB*

for i in `seq 1 10`;
do
        cat message.txt > /dev/ttyUSB$1
done 

# ./unlinking.sh