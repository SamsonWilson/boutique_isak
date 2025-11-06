# Étape 1 : choisir une image de base
FROM python:3.12-slim

# Étape 2 : définir le répertoire de travail
WORKDIR /app

# Étape 3 : copier le fichier de requirements et l’installer
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Étape 4 : copier le reste du code
COPY . .

# Étape 5 : définir les variables d’environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Étape 6 : exposer le port 8000
EXPOSE 8000

# Étape 7 : commande par défaut pour lancer Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]