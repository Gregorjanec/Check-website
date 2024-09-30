import requests

# Funkcija za pošiljanje e-pošte preko Formspree
def send_email(message):
    url = 'https://formspree.io/f/manwrpzz'  # Zamenjaj {tvoj_form_id} z URL-jem iz Formspree
    data = {
        'email': 'grega.grajzl@student.um.si',  # Tukaj vpiši svoj e-poštni naslov
        'message': message  # Sporočilo, ki ga želiš poslati
    }

    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print('Email poslan uspešno.')
    else:
        print(f'Napaka pri pošiljanju e-pošte: {response.status_code}')

# Pokliči funkcijo in pošlji sporočilo
send_email('To je testno sporočilo!')
