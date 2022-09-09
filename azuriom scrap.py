# Azuriom scraping V1.0.0
# by MrCyci6#0001

from bs4 import BeautifulSoup
import requests

domain = input("Nom de domain >> ")
log_u = f"https://{domain}/user/login"

# token d'autehntification
def auth_token(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        token = soup.find('input', attrs={'name': '_token'})
        return token.get('value').strip()  
    except:
        print(f"Aucun token d'authentification n'a été trouvé avec le nom '_token', (ligne 14 - 32)")


payload = {
    'email': input("Identifiant >> "),
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

    response = session.get(f"https://{domain}/admin/users/{i}/edit")

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        pseudo = soup.find(id='nameInput')
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