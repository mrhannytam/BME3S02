from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
while True:
	id, text = reader.read()
	card = int(text)
	print(card)

