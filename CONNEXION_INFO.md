# 🔐 Informations de Connexion - Gold 7 Car Rent

## 🚀 Accès à l'Application

L'application Gold 7 Car Rent est maintenant sécurisée avec un système de connexion.

### 📍 URL de Connexion
```
http://127.0.0.1:5001/login
```

### 🔑 Identifiants de Connexion

**Code d'accès :** `gold72025car`  
**Mot de passe :** `gold72025car`

## 🛡️ Sécurité

- ✅ **Toutes les pages sont protégées** - Accès impossible sans connexion
- ✅ **Session sécurisée** - Reste connecté pendant la session
- ✅ **Déconnexion automatique** - Bouton de déconnexion disponible
- ✅ **Redirection intelligente** - Redirige vers login si non connecté

## 🎯 Comment se Connecter

1. **Ouvrez votre navigateur** et allez sur `http://127.0.0.1:5001`
2. **Vous serez redirigé** vers la page de connexion automatiquement
3. **Entrez les identifiants :**
   - Code d'accès : `gold72025car`
   - Mot de passe : `gold72025car`
4. **Cliquez sur "Se connecter"**
5. **Vous accédez** au tableau de bord principal

## 🔄 Déconnexion

- **Cliquez sur votre nom d'utilisateur** en haut à droite de la barre de navigation
- **Sélectionnez "Déconnexion"** dans le menu déroulant
- **Vous serez redirigé** vers la page de connexion

## 🎨 Interface de Connexion

La page de connexion présente :
- **Logo Gold 7 Car Rent** en en-tête
- **Design moderne** avec dégradé doré
- **Animations fluides** à l'ouverture
- **Responsive** - S'adapte aux mobiles et tablettes
- **Messages d'erreur** en cas d'identifiants incorrects

## ⚙️ Configuration Technique

### Identifiants dans le Code
Les identifiants sont définis dans `app.py` :
```python
LOGIN_USERNAME = 'gold72025car'
LOGIN_PASSWORD = 'gold72025car'
```

### Modification des Identifiants
Pour changer les identifiants :
1. **Ouvrez** le fichier `app.py`
2. **Modifiez** les lignes 20-21 :
   ```python
   LOGIN_USERNAME = 'nouveau_nom_utilisateur'
   LOGIN_PASSWORD = 'nouveau_mot_de_passe'
   ```
3. **Redémarrez** l'application

## 🔒 Pages Protégées

Toutes ces pages nécessitent une connexion :
- ✅ **Tableau de bord** (`/`)
- ✅ **Gestion des voitures** (`/voitures`)
- ✅ **Gestion des réservations** (`/reservations`)
- ✅ **Gestion des vidanges** (`/vidanges`)
- ✅ **Toutes les sous-pages** (ajouter, modifier, supprimer)
- ✅ **Génération de reçus** (web et PDF)

## 📱 Compatibilité

Le système de connexion fonctionne sur :
- ✅ **Ordinateurs** (Windows, Mac, Linux)
- ✅ **Tablettes** (iPad, Android)
- ✅ **Smartphones** (iPhone, Android)
- ✅ **Tous navigateurs** (Chrome, Firefox, Safari, Edge)

## 🚨 Dépannage

### Problème : "Identifiants incorrects"
- ✅ Vérifiez que vous tapez exactement : `gold72025car`
- ✅ Attention aux majuscules/minuscules
- ✅ Pas d'espaces avant ou après

### Problème : Page ne se charge pas
- ✅ Vérifiez que l'application Flask est démarrée
- ✅ Allez sur `http://127.0.0.1:5001/login`
- ✅ Redémarrez l'application si nécessaire

### Problème : Déconnecté automatiquement
- ✅ Normal après fermeture du navigateur
- ✅ Reconnectez-vous avec les mêmes identifiants

## 💡 Conseils d'Utilisation

- **Gardez l'onglet ouvert** pour rester connecté
- **Utilisez le bouton déconnexion** avant de fermer
- **Bookmarkez** la page de login pour un accès rapide
- **Partagez les identifiants** uniquement avec les utilisateurs autorisés

---

**🎉 Votre système Gold 7 Car Rent est maintenant sécurisé et prêt à l'emploi !**
