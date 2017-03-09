import telepot
import time
import sys

machine_state = 0

# Crediti per la gestione della conversione Morse - Alphabet a https://gist.github.com/ebuckley/1842461

morseAlphabet = {
    "A" : ".-",
    "B" : "-...",
    "C" : "-.-.",
    "D" : "-..",
    "E" : ".",
    "F" : "..-.",
    "G" : "--.",
    "H" : "....",
    "I" : "..",
    "J" : ".---",
    "K" : "-.-",
    "L" : ".-..",
    "M" : "--",
    "N" : "-.",
    "O" : "---",
    "P" : ".--.",
    "Q" : "--.-",
    "R" : ".-.",
    "S" : "...",
    "T" : "-",
    "U" : "..-",
    "V" : "...-",
    "W" : ".--",
    "X" : "-..-",
    "Y" : "-.--",
    "Z" : "--..",
    " " : "  ", # SPAZIO TRA DUE PAROLE
    "1" : ".----",
    "2" : "..---",
    "3" : "...--",
    "4" : "....-",
    "5" : ".....",
    "6" : "-....",
    "7" : "--...",
    "8" : "---..",
    "9" : "----.",
    "0" : "-----",
    "." : ".-.-.-",
    "," : "--..--",
    ":" : "---...",
    "?" : "..--..",
    "'" : ".----.",
    "-" : "-....-",
    "/" : "-..-.",
    "@" : ".--.-.",
    "=" : "-...-"
    }

inverseMorseAlphabet=dict((v,k) for (k,v) in morseAlphabet.items())

# Codifica un messaggio da Morse in alfabeto
def decodeMorse(code, positionInString = 0):

    if positionInString < len(code):
        morseLetter = ""
        for key,char in enumerate(code[positionInString:]):
            if char == " ":
                positionInString = key + positionInString + 1
                letter = inverseMorseAlphabet[morseLetter]
                return letter + decodeMorse(code, positionInString)
            else:
                morseLetter += char
    else:
        return ""

# Codifca un messaggio in codice Morse, lo spazio è rapressentato dal simbolo '/'
def encodeToMorse(message):
    encodedMessage = ""
    for char in message[:]:
        encodedMessage += morseAlphabet[char.upper()] + " "

    return encodedMessage

# Funzione che viene eseguita all'arrivo di ogni nuovo messaggio
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    global machine_state
    str_testo_morse = ""
    str_testo_alphabet = ""

    chat_id = msg['chat']['id']
    command_input = msg['text']

    print(chat_id, content_type)

    if machine_state == 0 and content_type == 'text':

        if command_input == '/start' or command_input == '/start@MorsetorBot':

            start_text = '''Benvenuto nel futuro! Inzia a digitare un comando per cominciare un'esperienza metafisica'''
            bot.sendMessage(chat_id, start_text)

            machine_state = 1

    elif machine_state == 1 and content_type == 'text':

        if command_input == '/help' or command_input == '/help@FrazionetorBot':

            help_text = "Salve, puoi utilizzare il comando /atm per convertire un qualsiasi"
            help_text += "messaggio in codice Morse mentre puoi utilizzare il comando /mta per convertire un codice Morse "
            help_text += "in un messaggio di testo.\nPuoi contattare lo sviluppatore su github.com/Azzeccagarbugli"
            bot.sendMessage(chat_id, help_text)

            machine_state = 1

        elif command_input == '/atm' or command_input == '/atm@FrazionetorBot':

            morse_text = "Inserisci il messaggio che vuoi convertire in codice Morse"
            bot.sendMessage(chat_id, morse_text)

            machine_state = 2

        elif command_input == '/mta' or command_input == '/mta@FrazionetorBot':

            alphabet_text = "Inserisci il codice Morse che vuoi convertire in un messagio"
            bot.sendMessage(chat_id, alphabet_text)

            machine_state = 3

    elif machine_state == 2 and content_type == 'text':

        str_testo_morse = command_input.lower()
        str_morse = encodeToMorse(str_testo_morse)
        str_answer_morse = ("Il messaggio convertito in codice Morse è: {0}".format(str_morse))

        bot.sendMessage(chat_id, str_answer_morse, parse_mode = "Markdown")
        print(str_answer_morse)
        machine_state = 1

    elif machine_state == 3 and content_type == 'text':

        str_testo_alphabet = command_input.lower()
        str_alphabet = decodeMorse(str_testo_alphabet, 0)
        str_answer_alphabet = ("Il messaggio convertito in codice Morse è: {0}".format(str_alphabet))

        bot.sendMessage(chat_id, str_answer_alphabet, parse_mode = "Markdown")
        print(str_answer_alphabet)
        machine_state = 1

bot = telepot.Bot('TOKEN')
bot.message_loop(handle)

print('Vediamo quello che succede ...')

while 1:
    time.sleep(10)
