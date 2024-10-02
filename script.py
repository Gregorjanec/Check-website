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

        # Poišči element, kjer je število obvestil
        badge_element = soup.find('span', id='cp_total_results')

        if badge_element and badge_element.text.strip():
            try:
                stevilo_obvestil = int(badge_element.text.strip())
                print(f"Število obvestil: {stevilo_obvestil}")
            except ValueError:
                print(f"Napaka: Element ni vseboval veljavnega števila. Vsebina elementa: {badge_element.text.strip()}")
                return
        else:
            print("Element s številom obvestil ni bil najden ali je prazen.")
            return

        # Preveri, ali so nova obvestila
        if not os.path.exists('stevilo_obvestil.txt'):
            # Če datoteka ne obstaja, jo ustvari in shrani trenutno število obvestil
            with open('stevilo_obvestil.txt', 'w') as f:
                f.write(str(stevilo_obvestil))
            print(f"Ustvarjena nova datoteka z vrednostjo: {stevilo_obvestil}")
            return

        with open('stevilo_obvestil.txt', 'r+') as f:
            vsebina = f.read().strip()

            # Preveri, če je vsebina datoteke prazna ali neveljavna
            if not vsebina or not vsebina.isdigit():
                print(f"Napaka: Vsebina datoteke ni veljavna številka. Vsebina datoteke: '{vsebina}'")
                f.seek(0)
                f.truncate()  # Počisti datoteko
                f.write(str(stevilo_obvestil))  # Posodobi datoteko s trenutno številko obvestil
                print(f"Posodobljena datoteka z vrednostjo: {stevilo_obvestil}")
                return

            prejsnje_stevilo_obvestil = int(vsebina)

            # Če je trenutno število obvestil večje, pošlji e-pošto
            if stevilo_obvestil > prejsnje_stevilo_obvestil:
                poslji_mail_o_novih_obvestilih(stevilo_obvestil)
                f.seek(0)
                f.truncate()  # Počisti datoteko
                f.write(str(stevilo_obvestil))  # Posodobi datoteko s trenutno številko obvestil
                print(f"Število obvestil posodobljeno na {stevilo_obvestil}")

    except requests.exceptions.RequestException as e:
        print(f"Napaka pri dostopu do spletne strani: {e}")
    except Exception as e:
        print(f"Napaka pri preverjanju obvestil: {e}")

# Funkcija za pošiljanje e-pošte preko Formspree
def poslji_mail_o_novih_obvestilih(stevilo_obvestil):
    try:
        url = 'https://www.fe.um.si/aktualna-obvestila.html?option=com_customproperties&view=search&Itemid=427&lang=sl&cp%5Bprogram%5D%5B%5D=mag&cp%5Bprogram%5D%5B%5D=&cp%5Bletnik%5D%5B%5D=1_letnik&cp%5Bletnik%5D%5B%5D=&cp%5Bnacin%5D%5B%5D=redni&cp%5Bnacin%5D%5B%5D=&cp%5Blokacija%5D%5B%5D=krsko&cp%5Blokacija%5D%5B%5D=&submit_search='  # Tvoj Formspree URL
        mail_body = f"Novo obvestilo!\nNa spletni strani je bilo objavljeno novo obvestilo.\n\n"
        mail_body += f"Ogled obvestil: {url}"  # Dodaj povezavo do strani

        # Pošlji podatke kot JSON
        data = {
            'email': 'grega.grajzl@student.um.si',  # Spremeni na svoj e-poštni naslov
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
