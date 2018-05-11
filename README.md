# Reflected_SQLi_Solver
Fonctionnement du script:
  - Inscription au site avec comme username : "owned'; UPDATE users SET admin=1 -- -"
  - Exploitation de la faille XSS grâce au payload : "<button autofocus onfocus=document.location='http://localhost/challenge/members.php?username=owned'>"
  - Sleep de 60 secondes afin de laisser le BOT lire ses mails
  - Parsing du flag
  
  # Payloads
  Décomposition de la payload utilisée afin d'exploiter la faille SQL ("owned'; UPDATE users SET admin=1 -- -"):
  - owned'; sert à terminée notre requête SQL
  - UPDATE users sert à effectuer des modifications sur des lignes existantes de la table "users" (en mode barbare sans WHERE \o/)
  - SET admin=1 attribue une nouvelle valeur à la colonne "admin" (1)
  - "-- -" sert à passer le reste de notre requête en commentaire (') de manière à ne pas causer d'erreur
  
Décomposition de la payload utilisée afin d'exploiter la faille XSS (<button autofocus onfocus=document.location='http://localhost/challenge/members.php?username=yournick'>):
  - autofocus sert à ordonner au navigateur de focus l'élement "button"
  - onfocus sert à donner une instruction lors du focus (instruction qui sera forcémment exécutée puisqu'on utilise "autofocus")
  - document.location redirige le bot vers notre profil
  
La subtilité du challenge est que lors de l'inscription, la payload est passée sous PDO avec des bindvalue, ce qui fait qu'aucune injection n'est possible. Lors de la visite sur le profil d'un utilisateur, "views" n'est pas incrémenté de 1 si le visiteur est le propriétaire du compte, ce qui force l'attaquant à exploiter la faille XSS. La fonction utilisée pour la requête incrémentant la colonne "views" est la fonction "mysql_query" et le nom d'utilisateur de l'attaquant est passée sous simple quote : "SELECT * FROM users WHERE username='$username'", étant donné que notre pseudonyme est : "owned'; UPDATE users SET admin=1 -- -", la requête deviendra : "SELECT * FROM users WHERE username='owned'; UPDATE users SET admin=1 -- -'.
