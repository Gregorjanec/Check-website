import requests
from bs4 import BeautifulSoup
import os

# URL spletne strani, ki jo bomo preverjali
url = 'https://www.fe.um.si/aktualna-obvestila.html?option=com_customproperties&view=search&Itemid=427&lang=sl&cp%5Bprogram%5D%5B%5D=mag&cp%5Bprogram%5D%5B%5D=&cp%5Bletnik%5D%5B%5D=1_letnik&cp%5Bletnik%5D%5B%5D=&cp%5Bnacin%5D%5B%5D=redni&cp%5Blokacija%5D%5B%5D=krsko&cp%5Blokacija%5D%5B%5D=&submit_search='

def preveri_nova_obvestila():
    try:
        # Pošlji zahtevo na spletno stran
        response = requests.get(url)
        response.raise_for_status()  # Preveri, če je bila zahteva uspešna
        soup = BeautifulSoup(response.content, 'html.parser')

        # Poišči element, kjer je število obvestil
        badge_element = soup.find('span', id='cp_total_results')

        if badge_element and badge_element.text.strip():
            try:
                stevilo_obvestil = int(badge_element.text.strip())
                print(f"Število obvestil na strani: {stevilo_obvestil}")
            except ValueError:
                print(f"Napaka: Element ni vseboval veljavnega števila. Vsebina elementa: {badge_element.text.strip()}")
                return
        else:
            print("Element s številom obvestil ni bil najden ali je prazen.")
            return

        # Preveri, ali datoteka stevilo_obvestil.txt obstaja
        if os.path.exists('stevilo_obvestil.txt'):
            with open('stevilo_obvestil.txt', 'r') as f:
                prejsnje_stevilo_obvestil = f.read().strip()
                print(f"Prejšnje število obvestil: {prejsnje_stevilo_obvestil}")
        else:
            print("Datoteka stevilo_obvestil.txt ne obstaja. Ustvarjam novo.")
            prejsnje_stevilo_obvestil = '0'
            with open('stevilo_obvestil.txt', 'w') as f:
                f.write(prejsnje_stevilo_obvestil)

        # Če je novo število obvestil večje, posodobi in pošlji e-pošto
        if int(stevilo_obvestil) > int(prejsnje_stevilo_obvestil):
            print(f"Nova obvestila so zaznana! Pošiljam e-pošto...")
            poslji_mail_o_novih_obvestilih(stevilo_obvestil)

            # Posodobi datoteko z novim številom obvestil
            with open('stevilo_obvestil.txt', 'w') as f:
                f.write(str(stevilo_obvestil))
            print(f"Število obvestil posodobljeno na {stevilo_obvestil} v datoteko.")
        else:
            print(f"Ni novih obvestil. Trenutno število obvestil: {stevilo_obvestil}")

    except requests.exceptions.RequestException as e:
        print(f"Napaka pri dostopu do spletne strani: {e}")
    except Exception as e:
        print(f"Napaka pri preverjanju obvestil: {e}")

# Funkcija za pošiljanje e-pošte več prejemnikom
def poslji_mail_o_novih_obvestilih(stevilo_obvestil):
    try:
        # Seznam prejemnikov
        prejemniki = ['grega.grajzl@student.um.si']  # Dodaj več prejemnikov

        url = 'https://formspree.io/f/manwrpzz'  # Pravi Formspree URL
        mail_body = f"Novo obvestilo!\nNa spletni strani je bilo objavljeno novo obvestilo.\n\n"
        mail_body += f"Ogled obvestil: https://www.fe.um.si/aktualna-obvestila.html?option=com_customproperties&view=search&Itemid=427&lang=sl&cp%5Bprogram%5D%5B%5D=mag&cp%5Bprogram%5D%5B%5D=&cp%5Bletnik%5D%5B%5D=1_letnik&cp%5Bletnik%5D%5B%5D=&cp%5Bnacin%5D%5B%5D=redni&cp%5Blokacija%5D%5B%5D=krsko&cp%5Blokacija%5D%5B%5D=&submit_search="  # Povezava do obvestil

        # Pošlji e-pošto vsakemu prejemniku posebej
        for prejemnik in prejemniki:
            data = {
                'email': prejemnik,  # Posodobi prejemnika za vsako pošiljanje
                'message': mail_body
            }

            response = requests.post(url, data=data)

            if response.status_code == 200:
                print(f"E-pošta uspešno poslana prejemniku {prejemnik}!")
            else:
                print(f"Napaka pri pošiljanju e-pošte prejemniku {prejemnik}: {response.status_code}")

    except Exception as e:
        print(f"Napaka pri pošiljanju e-pošte: {e}")

if __name__ == "__main__":
    preveri_nova_obvestila()
