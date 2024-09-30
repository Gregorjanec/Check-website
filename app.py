import requests
from bs4 import BeautifulSoup

# URL do strani z obvestili
URL = 'https://www.fe.um.si/aktualna-obvestila.html?option=com_customproperties&view=search&Itemid=427&lang=sl&cp%5Bprogram%5D%5B%5D=mag&cp%5Bprogram%5D%5B%5D=&cp%5Bletnik%5D%5B%5D=1_letnik&cp%5Bletnik%5D%5B%5D=&cp%5Bnacin%5D%5B%5D=redni&cp%5Bnacin%5D%5B%5D=&cp%5Blokacija%5D%5B%5D=krsko&cp%5Blokacija%5D%5B%5D=&submit_search='

# Funkcija za pridobivanje obvestil s strani
def get_obvestila():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Najdemo vsa obvestila (vsak element 'div' z določeno klaso)
    obvestila = soup.find_all('div', class_='category-list')
    
    # Shranimo besedilo obvestil
    return [obvestilo.text.strip() for obvestilo in obvestila]

# Funkcija za pošiljanje e-pošte preko Formspree
def send_email(message):
    url = 'https://formspree.io/f/manwrpzz'  # Zamenjaj {tvoj_form_id} z ID-jem, ki si ga dobil od Formspree
    data = {
        'email': 'prejemnik@primer.com',  # Tvoj e-poštni naslov
        'message': message  # Sporočilo z novim obvestilom
    }

    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print('Email poslan uspešno.')
    else:
        print(f'Napaka pri pošiljanju e-pošte: {response.status_code}')

# Glavni del programa
def main():
    try:
        # Preberemo prejšnja obvestila iz datoteke
        with open('prejsnja_obvestila.txt', 'r', encoding='utf-8') as f:
            prejsnja_obvestila = f.read().splitlines()
    except FileNotFoundError:
        prejsnja_obvestila = []

    # Pridobimo trenutno obvestila
    trenutna_obvestila = get_obvestila()

    # Preverimo, če so nova obvestila
    nova_obvestila = [obv for obv in trenutna_obvestila if obv not in prejsnja_obvestila]

    # Če so nova obvestila, pošljemo e-pošto
    if nova_obvestila:
        send_email(f'Nova obvestila: {", ".join(nova_obvestila)}')
        
        # Shranimo trenutno stanje obvestil
        with open('prejsnja_obvestila.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(trenutna_obvestila))
    else:
        print("Ni novih obvestil.")

# Klic glavne funkcije
if __name__ == "__main__":
    main()
