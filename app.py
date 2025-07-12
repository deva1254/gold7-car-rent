from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gold7-car-rent-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location_voiture.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Informations de connexion
LOGIN_USERNAME = 'gold72025car'
LOGIN_PASSWORD = 'gold72025car'

# Décorateur pour protéger les routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Modèles de données
class Voiture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    immatriculation = db.Column(db.String(20), unique=True, nullable=False)
    couleur = db.Column(db.String(50), nullable=False)
    km = db.Column(db.Integer, nullable=False)
    carburant = db.Column(db.String(20), nullable=False)  # diesel/essence
    disponible = db.Column(db.Boolean, default=True)
    
    reservations = db.relationship('Reservation', backref='voiture', lazy=True)
    vidanges = db.relationship('Vidange', backref='voiture', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_client = db.Column(db.String(100), nullable=False)
    date_depart = db.Column(db.Date, nullable=False)
    date_retour = db.Column(db.Date, nullable=False)
    jours = db.Column(db.Integer, nullable=False)
    prix_par_jour = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    voiture_id = db.Column(db.Integer, db.ForeignKey('voiture.id'), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

class Vidange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    immatriculation = db.Column(db.String(20), nullable=False)
    derniere_vidange = db.Column(db.Integer, nullable=False)  # km
    prochaine_vidange = db.Column(db.Integer, nullable=False)  # km
    voiture_id = db.Column(db.Integer, db.ForeignKey('voiture.id'), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

class Retour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_retour = db.Column(db.Date, nullable=False)
    heure_retour = db.Column(db.Time, nullable=False)
    nom_client = db.Column(db.String(100), nullable=False)
    voiture_id = db.Column(db.Integer, db.ForeignKey('voiture.id'), nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=True)
    km_retour = db.Column(db.Integer, nullable=True)  # Kilométrage au retour
    etat_vehicule = db.Column(db.String(200), nullable=True)  # État du véhicule
    commentaires = db.Column(db.Text, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    voiture = db.relationship('Voiture', backref='retours')
    reservation = db.relationship('Reservation', backref='retour', uselist=False)

# Routes de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            flash('Connexion réussie ! Bienvenue dans Gold 7 Car Rent.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté avec succès.', 'info')
    return redirect(url_for('login'))

# Routes principales
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Routes pour les voitures
@app.route('/voitures')
@login_required
def voitures():
    voitures = Voiture.query.all()
    return render_template('voitures.html', voitures=voitures)

@app.route('/voiture/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_voiture():
    if request.method == 'POST':
        nom = request.form['nom']
        immatriculation = request.form['immatriculation']
        couleur = request.form['couleur']
        km = int(request.form['km'])
        carburant = request.form['carburant']

        nouvelle_voiture = Voiture(
            nom=nom,
            immatriculation=immatriculation,
            couleur=couleur,
            km=km,
            carburant=carburant
        )

        try:
            db.session.add(nouvelle_voiture)
            db.session.commit()
            flash('Voiture ajoutée avec succès!', 'success')
            return redirect(url_for('voitures'))
        except:
            flash('Erreur: Cette immatriculation existe déjà!', 'error')

    return render_template('ajouter_voiture.html')

@app.route('/voiture/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_voiture(id):
    voiture = Voiture.query.get_or_404(id)

    if request.method == 'POST':
        voiture.nom = request.form['nom']
        voiture.immatriculation = request.form['immatriculation']
        voiture.couleur = request.form['couleur']
        voiture.km = int(request.form['km'])
        voiture.carburant = request.form['carburant']
        voiture.disponible = 'disponible' in request.form

        try:
            db.session.commit()
            flash('Voiture modifiée avec succès!', 'success')
            return redirect(url_for('voitures'))
        except:
            flash('Erreur lors de la modification!', 'error')

    return render_template('modifier_voiture.html', voiture=voiture)

@app.route('/voiture/supprimer/<int:id>')
@login_required
def supprimer_voiture(id):
    voiture = Voiture.query.get_or_404(id)

    try:
        db.session.delete(voiture)
        db.session.commit()
        flash('Voiture supprimée avec succès!', 'success')
    except:
        flash('Erreur lors de la suppression!', 'error')

    return redirect(url_for('voitures'))

# Routes pour les réservations
@app.route('/reservations')
@login_required
def reservations():
    reservations = Reservation.query.all()
    return render_template('reservations.html', reservations=reservations)

@app.route('/reservation/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_reservation():
    if request.method == 'POST':
        nom_client = request.form['nom_client']
        date_depart = datetime.strptime(request.form['date_depart'], '%Y-%m-%d').date()
        date_retour = datetime.strptime(request.form['date_retour'], '%Y-%m-%d').date()
        prix_par_jour = float(request.form['prix_par_jour'])
        voiture_id = int(request.form['voiture_id'])

        # Calculer le nombre de jours
        jours = (date_retour - date_depart).days
        if jours <= 0:
            flash('La date de retour doit être après la date de départ!', 'error')
            voitures = Voiture.query.filter_by(disponible=True).all()
            return render_template('ajouter_reservation.html', voitures=voitures)

        # Calculer le total
        total = jours * prix_par_jour

        nouvelle_reservation = Reservation(
            nom_client=nom_client,
            date_depart=date_depart,
            date_retour=date_retour,
            jours=jours,
            prix_par_jour=prix_par_jour,
            total=total,
            voiture_id=voiture_id
        )

        # Marquer la voiture comme indisponible
        voiture = Voiture.query.get(voiture_id)
        voiture.disponible = False

        try:
            db.session.add(nouvelle_reservation)
            db.session.commit()
            flash('Réservation ajoutée avec succès!', 'success')
            return redirect(url_for('reservations'))
        except:
            flash('Erreur lors de l\'ajout de la réservation!', 'error')

    voitures = Voiture.query.filter_by(disponible=True).all()
    return render_template('ajouter_reservation.html', voitures=voitures)

@app.route('/reservation/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_reservation(id):
    reservation = Reservation.query.get_or_404(id)

    if request.method == 'POST':
        # Rendre l'ancienne voiture disponible
        ancienne_voiture = Voiture.query.get(reservation.voiture_id)
        ancienne_voiture.disponible = True

        reservation.nom_client = request.form['nom_client']
        reservation.date_depart = datetime.strptime(request.form['date_depart'], '%Y-%m-%d').date()
        reservation.date_retour = datetime.strptime(request.form['date_retour'], '%Y-%m-%d').date()
        reservation.prix_par_jour = float(request.form['prix_par_jour'])
        reservation.voiture_id = int(request.form['voiture_id'])

        # Recalculer
        reservation.jours = (reservation.date_retour - reservation.date_depart).days
        reservation.total = reservation.jours * reservation.prix_par_jour

        # Marquer la nouvelle voiture comme indisponible
        nouvelle_voiture = Voiture.query.get(reservation.voiture_id)
        nouvelle_voiture.disponible = False

        try:
            db.session.commit()
            flash('Réservation modifiée avec succès!', 'success')
            return redirect(url_for('reservations'))
        except:
            flash('Erreur lors de la modification!', 'error')

    voitures = Voiture.query.filter_by(disponible=True).all()
    voitures.append(reservation.voiture)  # Ajouter la voiture actuelle
    return render_template('modifier_reservation.html', reservation=reservation, voitures=voitures)

@app.route('/reservation/supprimer/<int:id>')
@login_required
def supprimer_reservation(id):
    reservation = Reservation.query.get_or_404(id)

    # Rendre la voiture disponible
    voiture = Voiture.query.get(reservation.voiture_id)
    voiture.disponible = True

    try:
        db.session.delete(reservation)
        db.session.commit()
        flash('Réservation supprimée avec succès!', 'success')
    except:
        flash('Erreur lors de la suppression!', 'error')

    return redirect(url_for('reservations'))

@app.route('/reservation/recu/<int:id>')
@login_required
def generer_recu(id):
    reservation = Reservation.query.get_or_404(id)
    return render_template('recu.html', reservation=reservation)

@app.route('/reservation/recu_pdf/<int:id>')
@login_required
def generer_recu_pdf(id):
    reservation = Reservation.query.get_or_404(id)

    # Créer un buffer pour le PDF
    buffer = io.BytesIO()

    # Créer le PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Essayer d'ajouter le logo
    logo_path = os.path.join('static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        try:
            p.drawImage(logo_path, 50, height - 80, width=100, height=40, preserveAspectRatio=True)
        except:
            pass  # Si erreur avec l'image, continuer sans logo

    # Titre
    p.setFont("Helvetica-Bold", 18)
    p.drawString(200, height - 50, "GOLD 7 CAR RENT")
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, height - 70, "REÇU DE LOCATION DE VOITURE")

    # Informations de la réservation
    p.setFont("Helvetica", 12)
    y = height - 120

    p.drawString(50, y, f"Client: {reservation.nom_client}")
    y -= 20
    p.drawString(50, y, f"Voiture: {reservation.voiture.nom}")
    y -= 20
    p.drawString(50, y, f"Immatriculation: {reservation.voiture.immatriculation}")
    y -= 20
    p.drawString(50, y, f"Date de départ: {reservation.date_depart}")
    y -= 20
    p.drawString(50, y, f"Date de retour: {reservation.date_retour}")
    y -= 20
    p.drawString(50, y, f"Nombre de jours: {reservation.jours}")
    y -= 20
    p.drawString(50, y, f"Prix par jour: {reservation.prix_par_jour} DH")
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"TOTAL: {reservation.total} DH")

    p.showPage()
    p.save()

    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=recu_{reservation.id}.pdf'

    return response

# Routes pour les vidanges
@app.route('/vidanges')
@login_required
def vidanges():
    vidanges = Vidange.query.all()
    return render_template('vidanges.html', vidanges=vidanges)

@app.route('/vidange/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_vidange():
    if request.method == 'POST':
        immatriculation = request.form['immatriculation']
        derniere_vidange = int(request.form['derniere_vidange'])
        voiture_id = int(request.form['voiture_id'])

        # Calculer la prochaine vidange
        prochaine_vidange = derniere_vidange + 10000

        nouvelle_vidange = Vidange(
            immatriculation=immatriculation,
            derniere_vidange=derniere_vidange,
            prochaine_vidange=prochaine_vidange,
            voiture_id=voiture_id
        )

        try:
            db.session.add(nouvelle_vidange)
            db.session.commit()
            flash('Vidange ajoutée avec succès!', 'success')
            return redirect(url_for('vidanges'))
        except:
            flash('Erreur lors de l\'ajout de la vidange!', 'error')

    voitures = Voiture.query.all()
    return render_template('ajouter_vidange.html', voitures=voitures)

@app.route('/vidange/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_vidange(id):
    vidange = Vidange.query.get_or_404(id)

    if request.method == 'POST':
        vidange.immatriculation = request.form['immatriculation']
        vidange.derniere_vidange = int(request.form['derniere_vidange'])
        vidange.voiture_id = int(request.form['voiture_id'])

        # Recalculer la prochaine vidange
        vidange.prochaine_vidange = vidange.derniere_vidange + 10000

        try:
            db.session.commit()
            flash('Vidange modifiée avec succès!', 'success')
            return redirect(url_for('vidanges'))
        except:
            flash('Erreur lors de la modification!', 'error')

    voitures = Voiture.query.all()
    return render_template('modifier_vidange.html', vidange=vidange, voitures=voitures)

@app.route('/vidange/supprimer/<int:id>')
@login_required
def supprimer_vidange(id):
    vidange = Vidange.query.get_or_404(id)

    try:
        db.session.delete(vidange)
        db.session.commit()
        flash('Vidange supprimée avec succès!', 'success')
    except:
        flash('Erreur lors de la suppression!', 'error')

    return redirect(url_for('vidanges'))

# Routes pour les retours
@app.route('/retours')
@login_required
def retours():
    retours = Retour.query.order_by(Retour.date_retour.desc(), Retour.heure_retour.desc()).all()
    today = date.today()
    return render_template('retours.html', retours=retours, today=today)

@app.route('/retour/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_retour():
    if request.method == 'POST':
        date_retour = datetime.strptime(request.form['date_retour'], '%Y-%m-%d').date()
        heure_retour = datetime.strptime(request.form['heure_retour'], '%H:%M').time()
        nom_client = request.form['nom_client']
        voiture_id = int(request.form['voiture_id'])
        reservation_id = request.form.get('reservation_id')
        km_retour = request.form.get('km_retour')
        etat_vehicule = request.form.get('etat_vehicule', '')
        commentaires = request.form.get('commentaires', '')

        # Convertir reservation_id et km_retour en entiers si fournis
        reservation_id = int(reservation_id) if reservation_id else None
        km_retour = int(km_retour) if km_retour else None

        nouveau_retour = Retour(
            date_retour=date_retour,
            heure_retour=heure_retour,
            nom_client=nom_client,
            voiture_id=voiture_id,
            reservation_id=reservation_id,
            km_retour=km_retour,
            etat_vehicule=etat_vehicule,
            commentaires=commentaires
        )

        # Marquer la voiture comme disponible
        voiture = Voiture.query.get(voiture_id)
        voiture.disponible = True

        # Mettre à jour le kilométrage de la voiture si fourni
        if km_retour:
            voiture.km = km_retour

        try:
            db.session.add(nouveau_retour)
            db.session.commit()
            flash('Retour enregistré avec succès!', 'success')
            return redirect(url_for('retours'))
        except:
            flash('Erreur lors de l\'enregistrement du retour!', 'error')

    # Récupérer les voitures indisponibles (en location) et les réservations actives
    voitures_en_location = Voiture.query.filter_by(disponible=False).all()
    reservations_actives = Reservation.query.join(Voiture).filter(Voiture.disponible == False).all()
    today = date.today()
    now = datetime.now()

    return render_template('ajouter_retour.html',
                         voitures=voitures_en_location,
                         reservations=reservations_actives,
                         today=today,
                         now=now)

@app.route('/retour/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_retour(id):
    retour = Retour.query.get_or_404(id)

    if request.method == 'POST':
        retour.date_retour = datetime.strptime(request.form['date_retour'], '%Y-%m-%d').date()
        retour.heure_retour = datetime.strptime(request.form['heure_retour'], '%H:%M').time()
        retour.nom_client = request.form['nom_client']
        retour.voiture_id = int(request.form['voiture_id'])
        retour.reservation_id = request.form.get('reservation_id')
        retour.km_retour = request.form.get('km_retour')
        retour.etat_vehicule = request.form.get('etat_vehicule', '')
        retour.commentaires = request.form.get('commentaires', '')

        # Convertir en entiers si fournis
        retour.reservation_id = int(retour.reservation_id) if retour.reservation_id else None
        retour.km_retour = int(retour.km_retour) if retour.km_retour else None

        # Mettre à jour le kilométrage de la voiture si fourni
        if retour.km_retour:
            voiture = Voiture.query.get(retour.voiture_id)
            voiture.km = retour.km_retour

        try:
            db.session.commit()
            flash('Retour modifié avec succès!', 'success')
            return redirect(url_for('retours'))
        except:
            flash('Erreur lors de la modification!', 'error')

    voitures = Voiture.query.all()
    reservations = Reservation.query.all()
    return render_template('modifier_retour.html', retour=retour, voitures=voitures, reservations=reservations)

@app.route('/retour/supprimer/<int:id>')
@login_required
def supprimer_retour(id):
    retour = Retour.query.get_or_404(id)

    try:
        db.session.delete(retour)
        db.session.commit()
        flash('Retour supprimé avec succès!', 'success')
    except:
        flash('Erreur lors de la suppression!', 'error')

    return redirect(url_for('retours'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Configuration pour l'hébergement
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'

    app.run(debug=debug, host='0.0.0.0', port=port)
