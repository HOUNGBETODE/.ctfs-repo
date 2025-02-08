from pwn import *
from Crypto.Util.number import *
from hashlib import *
import base64
import re

while True:
    try:
        host ="challenges.hackday.fr"
        port =  41523

        # Connexion à l'hote distante
        conn = remote(host, port)

        texte=conn.recvuntil(b'Would you care to spend some time with me ...?\n')

        print(texte.decode())

        conn.send('yes'.encode())
        texte=conn.recvuntil(b"Excellent, so we can start talking!")
        print(texte.decode('utf8'))
        
        # first play
        # -----------

        # second play

        # Rock-Paper-Scissors playing
        for i in range(2):
            texte = conn.recvuntil(b"yours?")
            print(texte.decode('utf8'))
            bot_move = texte.decode('utf8').split("\n")[-1].split("!")[0].split()[-1]
            print(f"{bot_move = }")
            if bot_move == "P":
                conn.send(b"S,S")
            elif bot_move == "R":
                conn.send(b"P,P")
            else:
                conn.send(b"R,R")

        # Guess-The-Number playing
        a, b = 0, 20
        texte = conn.recvuntil(b"start!")
        print(texte.decode('utf8'))
        for i in range(5):
            if not i:
                print(str((a+b)//2))
                conn.send(str((a+b)//2))
            else:
                texte = conn.recvuntil(b"!")
                print(texte.decode('utf8'))
                if b"bigger" in texte:
                    a = (a+b)//2
                elif b"smaller" in texte:
                    b = (a+b)//2
                else:
                    break
                print(str((a+b)//2))
                conn.send(str((a+b)//2))

        # translating texts from one language to another according to the bot's will...
        if b"found it" in texte:
            # pip install deep-translator
            from deep_translator import GoogleTranslator

            def translate_text(text, source_language, target_language):
                try:
                    translator = GoogleTranslator(source=source_language, target=target_language)
                    translated_text = translator.translate(text)
                    return translated_text
                except Exception as e:
                    return f"An error occurred during translation: {e}"

            texte = conn.recvuntil(b"/") + conn.recvuntil(b"/") + conn.recvuntil(b"/") + conn.recvuntil(b"/")
            print(texte.decode('utf8'))
            word = texte.decode('utf8').split("/")[-4]
            target = texte.decode('utf8').split("/")[-2]
            print(f"{word = }")
            print(f"{target = }")
            conn.send(translate_text(word, "english", target).encode())

        # HACKDAY{So0ooOOo0_KNOW|LED,GE4BLE}

        # third play
        # -----------
        break

    except:
        conn.close()
        continue
    else:
        exit()

conn.interactive()
conn.close()