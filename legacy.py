#!/usr/bin/python
# -*- coding:utf-8 -*-

try:
	import pylab
	import time
	import os
	import random
	import matplotlib.pyplot as plt
	import signal		# pegando sinais como em C
	import serial		# métodos para a serial
	import sys			# para ter acesso aos parâmetros
except ImportError as e:
	print "\n------------\n"+"A seguinte biblioteca não esta instalada:"
	print "-> " + str(e).split(' ')[3] + "\n------------\n"
	quit()
	
# Declaração de macros
MAX=250
N_ADC = 4
# Declaração da	serial como global
try:
	if(sys.argv[1]):
		sys.stderr.write('Abrindo porta ' + sys.argv[1] + ': ')
		ser = serial.Serial(sys.argv[1],9600)
		ser.open()
		sys.stderr.write(' Aberta!\n')
except IndexError:
	try:
		ser = serial.Serial('/dev/ttyACM0',9600)
		ser.open()
	except :
		print "Passe uma porta existente como parâmetro!"
		print "\teg.: ./" + sys.argv[0] + " /dev/ttyACM0"
		print "\teg.: python " + sys.argv[0] + " /dev/ttyUSB0\n"
		print "\tPadrão --> porta \'/dev/ttyACM0\'"
		sys.exit(0)

except IOError as e:
	sys.stderr.write("Porta "+ sys.argv[1] + " indisponível\n")
	sys.exit(0)
	raise


def signal_handler(signal, frame):
    sys.stderr.write('\nCtrl+C pressionado!\n\n')
    ser.close()
    sys.exit(0)

def do_graph(ser):
	sys.stderr.write("Iniciando gráfico...\n")
	fig = plt.figure(figsize=(16, 10))
	axis = fig.add_subplot(111)
	axis.set_xlim([0,MAX])
	plt.ion()
	plt.show()
	sys.stderr.write("Esperando primeiro dado\n")
	msg = ser.readline()
	msg = ser.readline()
	msg = msg[msg.find('MEDIDAS:')+8:]
	if (len(msg.split(' '))) < N_ADC:
		sys.stderr.write("Espera-se mais quantidade de valores ADC\n")
	ADC = {"label":[],'values':[],'axis':range(N_ADC)}
	for i in range(N_ADC):
		ADC['label'].append ("ADC_"+str(i))
		ADC['values'].append ([]
		)
		ADC['axis'][i],=(axis.plot(ADC['values'][i]))
	fig.legend(ADC['axis'],ADC['label'])
	while True:
		try:
			msg = ser.readline()
			msg = msg[msg.find('MEDIDAS:')+8:]
			for i in range(N_ADC):
				ADC['values'][i].append(float(msg.split(' ')[i]))
				#ADC['values'][i].append(random.uniform(0,1))
				if(len(ADC['values'][i])>MAX):
					ADC['values'][i]=ADC['values'][i][1:]
				ADC['axis'][i].set_ydata(ADC['values'][i])
				ADC['axis'][i].set_xdata(range(len(ADC['values'][i])))
				axis.relim()
				axis.autoscale_view(True,True,True)
			plt.draw()
			print msg,
		except ValueError:
			sys.stderr.write("Dado mal formatado [" + msg[:len(msg)-1] + "]\n")
		except IndexError: 
			sys.stderr.write( "\rÍndice " + str(i) +" inexistente\n")
			plt.draw()
		
	plt.pause(5)
	
	
if __name__ == "__main__":
	#segura o sinal do CTRL+C
	signal.signal(signal.SIGINT, signal_handler)
		
	if ser.isOpen() & ser.readable():
		sys.stderr.write("Porta legível!\n")
		try:
			do_graph(ser)
		except Exception, ex:
			ser.close()
			sys.exit(0)

	else:
		print "Porta não acessível"
		ser.close()
		sys.exit(0)
		
