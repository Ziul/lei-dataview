# lei-dataview

## Dependencies

### Packages

- package 'python2.7'
- package 'python-matplotlib'
- package 'python-serial'
- package 'python-mock'

### Setting up ambient

 **Install Chef**

    # apt install chef

 **Install packages**

	# chef-apply dependencies.rb

 **It's ready to go!**

## Using

### Setup Mock Input

First of all you need a data comming from a serial port to use the aplication.
If you don't have a device to help you on it, you can use **socat**  to mock up a serial
port to you.

To create two virtual ports, run the script  [./Mock/run.sh](https://github.com/Ziul/lei-dataview/blob/master/Mock/run.sh)

    ./Mock/run.sh 21 22

This will create the ports   **/dev/ttyUSB21** and  ** /dev/ttyUSB22** who are linked
to each other by echo. Now if you you want to send some message to port **/dev/ttyUSB21**
you just need to do:

    echo "Hello World" > /dev/ttyUSB22

##### Stoping Mock Ports

To close the ports, just use<sup>**1**</sup>:

    ./Mock/unlinking.sh 21 22

<sub>**1:** Care! Using it will kill all **socat** runing daemon. </sub>


### Running application

With a port ready to be readen, just run the program with:

    ./main.py

Or

    python main.py

### Stoping application

The application do not have support to save stop yet. To stop it, you will have to send a
signal to kill the process.
