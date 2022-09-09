# Web scraping of Azuriom by MrCyci6#0001

from bs4 import BeautifulSoup
import requests

log_u = "https://cubexland.fr/user/login" # url de login du site

# token d'autehntification 
def auth_token(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        token = soup.find('input', attrs={'name': '_token'}) # le nom est trouvable dans F12 sur la page avec le type "hidden"
        return token.get('value').strip()
    except:
        print(f"Aucun token d'authentification n'a été trouvé avec le nom '_token', (ligne 12 - 31)")


payload = {
    'email': input("Identifiant >> "), # Pareil que pour le token changer les valeurs par celles dans le code du site
    'password': input("Mot de passe >> "),
}


session = requests.Session()
session.headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')}
response = session.get(log_u)

token = auth_token(response.text)
payload.update({
    '_token': token
})

p = session.post(log_u, data=payload)

nbr = int(input("Nombre d'utilisateur à scrap >> "))
print("\n")
i = 0
while i <= (nbr + 1):

    response = session.get(f"https://cubexland.fr/admin/users/{i}/edit") # url des utilisateurs du site

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        pseudo = soup.find(id='nameInput') # Changer les id si erreur ou trouve rien
        email = soup.find(id='emailInput')
        ip = soup.find(id='addressInput')

        print(f"{i} - {pseudo['value']} - {email['value']} - {ip['value']}")

        f = open("data.txt", 'a')
        f.write(pseudo['value'] + " - " + email['value'] + " - " + ip['value'] + "\n")

        i += 1
    except:
        print(f"pas d'utilisateur avec cet id : {i}")
        i += 1

print("\nTous les utilisateurs on été importés dans : data.txt")