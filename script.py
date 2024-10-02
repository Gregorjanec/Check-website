import requests
from bs4 import BeautifulSoup
import os

# URL spletne strani, ki jo bomo preverjali
url = 'https://www.fe.um.si/aktualna-obvestila.html?option=com_customproperties&view=search&Itemid=427&lang=sl&cp%5Bprogram%5D%5B%5D=mag&cp%5Bprogram%5D%5B%5D=&cp%5Bletnik%5D%5B%5D=1_letnik&cp%5Bletnik%5D%5B%5D=&cp%5Bnacin%5D%5B%5D=redni&cp%5Bnacin%5D%5B%5D=&cp%5Blokacija%5D%5B%5D=krsko&cp%5Blokacija%5D%5B%5D=&submit_search='

def preveri_nova_obvestila():
    try:
        # Pošlji zahtevo na spletno stran
        response = requests.get(url)
        response.raise_for_status()  # Preveri, če je bila zahteva uspešna
        soup = BeautifulSoup(response.content, 'html.parser')

        # Poišči obvestila na strani
        obvestila = soup.find_all('div', class_='customproperties-items')

        # Pridobi število obvestil
        stevilo_obvestil = len(obvestila)
        print(f"Število obvestil: {stevilo_obvestil}")

        # Preveri, ali so nova obvestila
        if not os.path.exists('stevilo_obvestil.txt'):
            with open('stevilo_obvestil.txt', 'w') as f:
                f.write(str(stevilo_obvestil))
            return

        with open('stevilo_obvestil.txt', 'r+') as f:
            prejsnje_stevilo_obvestil = int(f.read().strip())

            # Če je trenutno število obvestil večje, pošlji e-pošto
            if stevilo_obvestil > prejsnje_stevilo_obvestil:
                poslji_mail_o_novih_obvestilih(stevilo_obvestil)
                f.seek(0)
                f.truncate()
                f.write(str(stevilo_obvestil))

    except requests.exceptions.RequestException as e:
        print(f"Napaka pri dostopu do spletne strani: {e}")
    except Exception as e:
        print(f"Napaka pri preverjanju obvestil: {e}")

# Funkcija za pošiljanje e-pošte preko Formspree
def poslji_mail_o_novih_obvestilih(stevilo_obvestil):
    try:
        url = 'https://formspree.io/f/manwrpzz'  # Tvoj Formspree URL
        mail_body = f"Na spletni strani je bilo objavljenih novih obvestil: {stevilo_obvestil}"

        # Pošlji podatke kot JSON
        data = {
            'email': 'prejemnik@example.com',
            'message': mail_body
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            print("E-pošta uspešno poslana!")
        else:
            print(f"Napaka pri pošiljanju e-pošte: {response.status_code}")

    except Exception as e:
        print(f"Napaka pri pošiljanju e-pošte: {e}")

if __name__ == "__main__":
    preveri_nova_obvestila()
