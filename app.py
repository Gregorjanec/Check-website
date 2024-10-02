import requests
from bs4 import BeautifulSoup
import os

# URL spletne strani, ki jo bomo preverjali
url = 'https://www.fe.um.si/aktualna-obvestila.html?option=com_customproperties&view=search&Itemid=427&lang=sl&cp%5Bprogram%5D%5B%5D=mag&cp%5Bprogram%5D%5B%5D=&cp%5Bletnik%5D%5B%5D=1_letnik&cp%5Bletnik%5D%5B%5D=&cp%5Bnacin%5D%5B%5D=redni&cp%5Bnacin%5D%5B%5D=&cp%5Blokacija%5D%5B%5D=krsko&cp%5Blokacija%5D%5B%5D=&submit_search='

try:
    def preveri_nova_obvestila():
        # Pošlji zahtevo na spletno stran
        response = requests.get(url)
        response.raise_for_status()  # Preveri, če je bila zahteva uspešna

        soup = BeautifulSoup(response.content, 'html.parser')

        # Poišči obvestila
        obvestila = soup.find_all('div', class_='category')

        nova_obvestila = [obvestilo.text.strip() for obvestilo in obvestila]

        # Preveri prejšnja obvestila, če so shranjena
        if not os.path.exists('stara_obvestila.txt'):
            with open('stara_obvestila.txt', 'w') as f:
                f.write('\n'.join(nova_obvestila))
            return

        with open('stara_obvestila.txt', 'r+') as f:
            stara_obvestila = f.read().splitlines()

            # Če so nova obvestila, pošlji e-pošto
            if set(nova_obvestila) - set(stara_obvestila):
                poslji_mail_o_novih_obvestilih(nova_obvestila)
                f.seek(0)
                f.truncate()
                f.write('\n'.join(nova_obvestila))

    # Funkcija za pošiljanje e-pošte preko Formspree
    def poslji_mail_o_novih_obvestilih(nova_obvestila):
        url = 'https://formspree.io/f/manwrpzz'  # Tvoj Formspree URL
        mail_body = '\n'.join(nova_obvestila)

        # Pošlji podatke kot JSON
        data = {
            'email': 'grega.grajzl@student.um.si',
            'message': mail_body
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            print("E-pošta uspešno poslana!")
        else:
            print("Napaka pri pošiljanju e-pošte:", response.status_code)

    if __name__ == "__main__":
        preveri_nova_obvestila()

except Exception as e:
    print(f"Prišlo je do napake: {e}")
