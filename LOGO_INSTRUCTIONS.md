# 🎨 Instructions pour Ajouter Votre Logo Gold 7 Car Rent

## 📋 Résumé

Votre système de gestion de location de voiture est maintenant configuré pour afficher votre logo "Gold 7 Car Rent" dans toute l'application. Actuellement, un logo temporaire SVG est utilisé.

## 🚀 Comment Ajouter Votre Logo Personnalisé

### Étape 1 : Préparer votre fichier logo
1. **Sauvegardez** l'image de votre logo sur votre ordinateur
2. **Assurez-vous** que l'image est claire et de bonne qualité
3. **Format recommandé :** PNG avec fond transparent
4. **Taille recommandée :** 200x80 pixels (format paysage)

### Étape 2 : Ajouter le logo à l'application
1. **Naviguez** vers le dossier : `static/images/`
2. **Copiez** votre fichier logo dans ce dossier
3. **Renommez** le fichier en `logo.png` (exactement ce nom)
4. **Redémarrez** l'application Flask

### Étape 3 : Vérifier l'affichage
1. **Actualisez** votre navigateur (F5)
2. **Vérifiez** que votre logo apparaît dans :
   - La barre de navigation (en haut)
   - La page d'accueil (grand logo central)
   - Les reçus (en-tête des reçus)
   - Les PDF générés

## 📍 Emplacements du Logo

Votre logo apparaîtra automatiquement dans :

| Emplacement | Taille | Description |
|-------------|--------|-------------|
| **Barre de navigation** | 40px hauteur | Logo compact en haut de chaque page |
| **Page d'accueil** | 80px hauteur | Logo principal sur la page d'accueil |
| **Reçus web** | 50px hauteur | Logo sur les reçus affichés à l'écran |
| **Reçus PDF** | 100x40px | Logo sur les documents PDF générés |

## 🔄 Système de Fallback

L'application est configurée avec un système intelligent :
- **Si `logo.png` existe** → Votre logo personnalisé s'affiche
- **Si `logo.png` n'existe pas** → Le logo SVG temporaire s'affiche

## 💡 Conseils pour un Meilleur Rendu

### Format et Qualité
- ✅ **PNG avec fond transparent** (recommandé)
- ✅ **JPG** (acceptable)
- ✅ **Résolution élevée** pour un rendu net
- ❌ Évitez les formats GIF ou BMP

### Dimensions
- **Largeur :** 200-300 pixels
- **Hauteur :** 80-120 pixels
- **Ratio :** Format paysage (plus large que haut)

### Design
- **Lisibilité :** Le texte doit être lisible même en petite taille
- **Contraste :** Assurez-vous que le logo est visible sur fond blanc et coloré
- **Simplicité :** Un design simple fonctionne mieux aux petites tailles

## 🛠️ Dépannage

### Le logo ne s'affiche pas ?
1. **Vérifiez le nom du fichier :** Doit être exactement `logo.png`
2. **Vérifiez l'emplacement :** Doit être dans `static/images/`
3. **Actualisez le navigateur :** Appuyez sur F5 ou Ctrl+F5
4. **Redémarrez l'application :** Arrêtez et relancez `python run.py`

### Le logo est déformé ?
1. **Vérifiez les proportions** de votre image originale
2. **Créez une version** avec les bonnes dimensions
3. **Utilisez un fond transparent** pour un meilleur rendu

### Le logo n'apparaît pas dans les PDF ?
1. **Redémarrez l'application** après avoir ajouté le logo
2. **Générez un nouveau reçu** pour tester
3. **Vérifiez que le fichier** `logo.png` est bien présent

## 📞 Support

Si vous rencontrez des difficultés :
1. Vérifiez que le fichier est bien nommé `logo.png`
2. Assurez-vous qu'il est dans le bon dossier `static/images/`
3. Redémarrez complètement l'application
4. Testez avec un fichier PNG simple d'abord

## ✅ Checklist Finale

- [ ] Logo sauvegardé comme `logo.png`
- [ ] Fichier placé dans `static/images/`
- [ ] Application redémarrée
- [ ] Navigateur actualisé
- [ ] Logo visible dans la navigation
- [ ] Logo visible sur la page d'accueil
- [ ] Logo visible sur les reçus
- [ ] Test de génération PDF effectué

---

**🎉 Une fois votre logo ajouté, votre application Gold 7 Car Rent aura une identité visuelle complète et professionnelle !**
