import AES
import RSA 
import os

clear = lambda : os.system('clear')

def chiffrementAES() :
    print(' ||=====================================================||\n',
          '||                      CryptoBib                      ||\n',
          '||=====================================================||\n') 
    
    message = input('\nChoisissez un message à chiffrer via la méthode AES :')
    messageAES = AES.MessageAES(message)
    lastBlock = 1
    if(len(message) % 16 != 0) :
        lastBlock = 1
    else :
        lastBlock = 0
    print('le message est d une longueur de ', len(message), 
          'caractères, il possède ', len(message) // 16, 
          'blocks de 16 caractères et possède ', lastBlock, 
          'block incomplet de ', len(message) % 16, 'caractères\n')
    
    key = input('\nChoisissez une clé de cyptage de 16 caractères :')
    while (len(key) != 16) :
        key = input('\nLongueur de clé incorrect, choisissez en une autre :')
    keyAES = AES.CleAES(key)
    keyAES.keySchedule()
    
    print('\nChiffrement en cours...\n')
    
    messageAES.addRoundKey(keyAES.originalCle)
    for rounds in range(9) :
        messageAES.subBytes()
        messageAES.shiftRows()
        messageAES.mixColumn()
        keyAES.currentKey = keyAES.subCleList[rounds]
        messageAES.addRoundKey(keyAES.currentKey)
    messageAES.subBytes()
    messageAES.shiftRows()
    messageAES.addRoundKey(keyAES.subCleList[9])
    
    print('\n')
    messageAES.turnIntoChar()
    
    saveMessageData = input('\nVoulez-vous sauvegarder les données du message crypter ? (y/n)\n') 
    if (saveMessageData == 'y') :
        return messageAES.messageHacher
    elif (saveMessageData == 'n') :
        return None
    else :
        return None
    
def dechiffrementAES(savedData) :
    print(' ||=====================================================||\n',
          '||                      CryptoBib                      ||\n',
          '||=====================================================||\n') 
    
    print('\nChoisissez un message à déchiffrer via la méthode AES\n')
    choice = input('\nVoulez-vous écrire le message (1) ou charger les données sauvegarder (2) :')
    if (choice == '1') :
        message = input('\nEcrivez un message à décrypter :')
    elif (choice == '2') :
        if (savedData == None) :
            print('\nAucune donnée sauvegardé')
            message = input('\nEcrivez un message à décrypter :')
        else :
            message = savedData
    else :
        message = input('\nEcrivez un message à décrypter :')
    messageAES = AES.DecryptMessageAES(message)
    
    key = input('\nChoisissez une clé de décyptage de 16 caractères :')
    while (len(key) != 16) :
        key = input('\nLongueur de clé incorrect, choisissez en une autre :')
    keyAES = AES.CleAES(key)
    keyAES.keySchedule()
    
    print('\nDechiffrement en cours...\n')
    
    messageAES.reverseAddRoundKey(keyAES.subCleList[9])
    messageAES.reverseShiftRows()
    messageAES.reverseSubBytes()
    for rounds in range(9) :
        keyAES.currentKey = keyAES.subCleList[8 - rounds]
        messageAES.reverseAddRoundKey(keyAES.currentKey)
        messageAES.reverseMixColumn()
        messageAES.reverseShiftRows()
        messageAES.reverseSubBytes()
    messageAES.reverseAddRoundKey(keyAES.originalCle)
    
    print('\n')
    messageAES.turnIntoChar()
    
    input('Rentrer n importe quoi pour revenir au menu princpal :')
    
def creationCleRSA() :
    print(' ||=====================================================||\n',
          '||                      CryptoBib                      ||\n',
          '||=====================================================||\n') 
    
    keyRSA = RSA.CleRSA()
    
    choice = False
    keyRSA.printPrimeList()
    p = int(input('\nChoisissez un nombre premier :'))
    q = int(input('\nChoisissez en un deuxième distinct du premier :'))
    while (choice == False) :
        if (p != q) :
            if (RSA.arithmetic.isPrime(p) == True and RSA.arithmetic.isPrime(q) == True) :
                choice = True
        if (choice == False) :
            print('\nLes choix ne sont pas valides')
            p = int(input('\nChoisissez un nombre premier :'))
            q = int(input('\nChoisissez en un deuxième distinct du premier :'))
    keyRSA.calculPhiN(p, q)
    
    choice = False
    print('\nChoisissez un exposant qui est premier avec ', keyRSA.PhiN, ' : ')
    e = int(input())
    while (choice == False) :
        if (RSA.arithmetic.pgcd(e, keyRSA.PhiN) == 1) :
            choice = True
        if (choice == False) :
            print('\nCe choix n est pas valide')
            print('\nChoisissez un exposant qui est premier avec ', keyRSA.PhiN, ' : ')
            e = int(input())
    keyRSA.chooseExponent(e)
    
    keyRSA.calculPublicKey()
    keyRSA.calculPrivateKey()
    
    print('\nIMPORTANT A NOTER !!')
    print('\nVotre clé publique est ', keyRSA.publicKey)
    print('\nVotre clé privé est ', keyRSA.privateKey)
    
    input('\nRentrer n importe quoi pour revenir au menu princpal :')

def chiffrementRSA() :
    print(' ||=====================================================||\n',
          '||                      CryptoBib                      ||\n',
          '||=====================================================||\n') 
    
    message = input('\nChoisissez un message à chiffrer via la méthode RSA :')
    messageRSA = RSA.MessageRSA(message)
    
    e = int(input('\nRentrer le premier élément de votre clé publique :'))
    n = int(input('\nRentrer le deuxième élément de votre clé publique :'))
    
    print('\nChiffrement en cours...\n')
    
    messageRSA.encryption((e, n))
    
    print('\n')
    messageRSA.turnIntoChar()
    
    saveMessageData = input('\nVoulez-vous sauvegarder les données du message crypter ? (y/n)\n') 
    if (saveMessageData == 'y') :
        return messageRSA.encryptedMessage
    elif (saveMessageData == 'n') :
        return None
    else :
        return None
    
def dechiffrementRSA(savedData) :
    print(' ||=====================================================||\n',
          '||                      CryptoBib                      ||\n',
          '||=====================================================||\n') 
    
    print('\nChoisissez un message à déchiffrer via la méthode RSA\n')
    choice = input('\nVoulez-vous écrire le message (1) ou charger les données sauvegarder (2) :')
    if (choice == '1') :
        message = input('\nEcrivez un message à décrypter :')
    elif (choice == '2') :
        if (savedData == None) :
            print('\nAucune donnée sauvegardé')
            message = input('\nEcrivez un message à décrypter :')
        else :
            message = savedData
    else :
        message = input('\nEcrivez un message à décrypter :')
    messageRSA = RSA.DecryptMessageRSA(message)
    
    d = int(input('\nRentrez votre clé privée :'))
    n = int(input('\nRentrez n :'))
    
    print('\nDechiffrement en cours...\n')
    
    messageRSA.decryption(d, n)
    
    print('\n')
    messageRSA.turnIntoChar()
    
    input('\nRentrer n importe quoi pour revenir au menu princpal :')
    
savedData = None
loop = True
while (loop == True) :
    clear()
    print('\n ||=====================================================||\n',
            '||                      CryptoBib                      ||\n',
            '||=====================================================||\n')
    print('\n',
          '___________________1   Chiffrer AES   1___________________\n',
          '___________________2  Déchiffrer AES  2___________________\n',
          '___________________3  Créer clés RSA  3___________________\n',
          '___________________4   Chiffrer RSA   4___________________\n',
          '___________________5  Déchiffrer RSA  5___________________\n',
          '___________________6     Quitter      6___________________\n')
    inputLoop = True
    while (inputLoop == True) :
        choice = input('Choisissez une action à réaliser :')
        if (choice == '1') :
            clear()
            savedData = chiffrementAES()
            inputLoop = False
        elif (choice == '2') :
            clear()
            dechiffrementAES(savedData)
            inputLoop = False
        elif (choice == '3') :
            clear()
            creationCleRSA()
            inputLoop = False
        elif (choice == '4') :
            clear()
            savedData = chiffrementRSA()
            inputLoop = False
        elif (choice == '5') :
            clear()
            dechiffrementRSA(savedData)
            inputLoop = False
        elif (choice == '6') :
            print('Arret de CryptoBib\n')
            inputLoop = False
            loop = False
        else :
            print('Choix invalide\n')     