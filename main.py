from Pumpensteuerung.PumpController import PumpController
from Pumpensteuerung.Logwriter import Log
from time import sleep
import json
import requests


def main() -> None:
	pump: PumpController = PumpController()	# Initialisierung der Klasse PumpController
	duration: int = 10             			# Pumpzyklus in Sekunden
	pump_speed: int = 100          			# Pumpgeschwindigkeit in Prozent
	pause: int = (20 - duration)   			# Pausenzeit in Sekunden - Pumpzyklus
	min_capacity: float = 0.40     			# Behälterkapazität in Prozent / 100
	min_moisture: float = 0.30     			# Bodenfeuchtigkeit in Prozent / 100
	random_number: int = None      			# zufällige Nummer vordefiniert
	log: Log = Log()						# Initialisierung der Klasse Log

	while True:
		try:
			old_random_number: int = random_number

			request = requests.get('http://192.168.189.31:65500/api/sensordaten.json')										# Anforderung der Daten der API
			content = json.loads(request.text)																				# Laden der JSON-Datei der API

			moisture: float = content['moisture']																			#
			capacity: float = content['capacity']																			#
			random_number: int = content['random_number']																	#

			if old_random_number == None:																					# Logik für Programmstart-Nachricht
				log.write({'Status': 'Programm wurde gestartet.'})

			if random_number == old_random_number:																			# Logik zum abgleichen von alten Daten
				log.write({'Status': 'Daten sind veraltet.'})
			else:
				if moisture <= min_moisture and capacity >= min_capacity:													# Logik für die Pumpfunktion
					pump.set_speed(pump_speed)
					sleep(duration)
					pump.stop()

					log.write({'Status': 'Pumpe wurde gestartet.', 'Geschwindigkeit': f'{pump_speed}%'})

				else:
					if capacity < min_capacity:																				# Logik zum abgleichen des Behälterstands
						log.write({'Status': 'Behälter befüllen.', 'Füllstand': f'{capacity*100}%'})
					elif moisture > min_moisture:																			# Logik zum abgleichen der Bodenfeuchte
						log.write({'Status': 'Bodenfeuchtigkeit ist ausreichend.', 'Bodenfeuchte': f'{moisture*100}%'})

		except KeyboardInterrupt:																							#
			log.write({'Status': 'Pumpe wurde vom Nutzer ausgeschaltet.'})
			pump.close()

		except (ValueError) as error:																						#
			log.write({'Status': 'fehlerhafte Daten in der API.', 'Error-Code': f'{error}'})

		except (requests.exceptions.RequestException) as error:																#
			log.write({'Status': 'API nicht erreichbar.', 'Error-Code': f'{error}'})

		except (RuntimeError) as error:																						#
			log.write({'Status':'Programmabsturz.', 'Error-Code': f'{error}'})

		except (ConnectionError) as error:																					#
			log.write({'Status':'Verbindungsfehler.', 'Error-Code': f'{error}'})


		print(f'Zwangspause der Pumpe! {pause}s warten...')																	# Logik für eine Zwangspause
		sleep(pause)


if __name__ == '__main__':
	main()