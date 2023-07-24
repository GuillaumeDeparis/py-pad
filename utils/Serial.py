import serial

# Configuration du port série
port = 'COM3'  # Remplacez 'COM3' par le port série approprié pour votre Arduino
baud_rate = 9600  # Le même débit que celui défini dans votre programme Arduino

# Ouvrir une connexion série
ser = serial.Serial(port, baud_rate)

# Lire les données de l'Arduino
data_from_arduino = ser.readline()  # Lire une ligne complète envoyée par l'Arduino
print("Données reçues de l'Arduino :", data_from_arduino.decode())

# Fermer la connexion série
ser.close()