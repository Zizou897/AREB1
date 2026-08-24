#!/usr/bin/env bash
set -e

PROJECT_DIR="/var/www/AREB1"
SERVICE_NAME="areb_portfolio_gunicorn"

echo "🚀 Déploiement en cours pour Azeez Ridwan Portfolio..."

cd $PROJECT_DIR

echo "📥 Récupération des dernières modifications..."
git pull origin main

echo "📦 Mise à jour de l'environnement virtuel..."
source venv/bin/activate
pip install -r requirements.txt

echo "🗄️ Application des migrations Django..."
python manage.py migrate --no-input

echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "🔄 Redémarrage du service Gunicorn ($SERVICE_NAME)..."
sudo systemctl restart $SERVICE_NAME

echo "✅ Déploiement terminé avec succès !"
