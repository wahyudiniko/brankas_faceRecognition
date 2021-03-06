import RPi.GPIO as GPIO
from rpi_lcd import LCD
import time
import os

buzzer = 4
ledRed = 23
ledGreen = 24
relay = 18


lcd = LCD()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)


MATRIX = [ [1, 2, 3, "A"],
	   [4, 5, 6, "B"],
           [7, 8, 9, "C"],
           ["*", 0, "#", "D"] ]

ROW = [5, 6, 13, 19]
COL = [16, 20, 21, 12]

password = "1D"
passEnter = ""
passStars = ""

GPIO.output(ledGreen, 0)
GPIO.output(ledRed, 0)
GPIO.output(buzzer, 0)

time.sleep(1)
lcd.text("MASUKKAN PIN: ",1)

def benar():
	time.sleep(0.1)
	lcd.text("BRANKAS TERBUKA", 1)
	lcd.text("",2)
	GPIO.output(relay, 0)
	GPIO.output(ledGreen, 1)
	GPIO.output(ledRed, 0)
	
	GPIO.output(buzzer, 1)
	time.sleep(0.1)
	GPIO.output(buzzer, 0)
	time.sleep(0.1)
	GPIO.output(buzzer, 1)
	time.sleep(0.3)
	GPIO.output(buzzer, 0)
	
	time.sleep(1)
	lcd.text("'D' UNTUK KUNCI ", 2)


def salah():
	lcd.text("   PASSWORD", 1)
	lcd.text("    SALAH   ", 2)
	GPIO.output(relay, 1)
	GPIO.output(ledGreen, 0)
	GPIO.output(ledRed, 1)

	GPIO.output(buzzer, 1)
	time.sleep(1)
	GPIO.output(buzzer, 0)



for j in range(4):
	GPIO.setup(COL[j], GPIO.OUT)
	GPIO.output(COL[j], 1)

for i in range(4):
	GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

# ISI 
try:
	while True:
		GPIO.output(relay, 1)
		for j in range(4):
			GPIO.output(COL[j], 0)

			for i in range(4):
				if GPIO.input(ROW[i]) == 0:
					passEnter = passEnter + str(MATRIX[i][j])
					print(MATRIX[i][j])
					GPIO.output(buzzer, 1)
					time.sleep(0.1)
					GPIO.output(buzzer, 0)
					passStars = passStars + "*"

					if MATRIX[i][j] == "A":
						passEnter = ""
						passStars = ""
					if MATRIX[i][j] == "D":
						
						if passEnter == password:
							benar()
							pause = True
							while pause == True:
								#if MATRIX[i][j] == "B":
								if (GPIO.input(ROW[i])) == 0:
									pause = False
									break
								pass
						if passEnter != password:
							salah()
						passEnter = ""
						passStars = ""
					time.sleep(0.1)
					lcd.text("MASUKKAN PIN:",1)
					GPIO.output(ledGreen, 0)
					GPIO.output(ledRed, 0)
					GPIO.output(buzzer, 0)
					while(GPIO.input(ROW[i])) == 0:
						pass
			time.sleep(0.01)
			lcd.text(passStars, 2)
			GPIO.output(COL[j],1)

except KeyboardInterrupt:
	lcd.clear()
	GPIO.cleanup()

