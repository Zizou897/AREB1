#!/usr/bin/env bash
# ==============================================================================
# Script d'activation des services Gunicorn & Nginx (Azeez Ridwan Portfolio)
# Usage : sudo bash deploy/setup_services.sh
# ==============================================================================

set -e

# Couleurs pour le terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="/var/www/AREB1"
GUNICORN_SERVICE_NAME="areb_portfolio_gunicorn"
NGINX_CONF_NAME="areb_portfolio.conf"

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}  🚀 Activation des Services Gunicorn & Nginx (AREB1) ${NC}"
echo -e "${BLUE}======================================================${NC}"

# 1. Vérification des droits root / sudo
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}❌ Ce script doit être exécuté avec les privilèges root (sudo).${NC}"
  echo "Exemple : sudo bash deploy/setup_services.sh"
  exit 1
fi

# 2. Création du dossier des logs et assignation des permissions
echo -e "\n${YELLOW}📁 [1/5] Configuration des dossiers et permissions...${NC}"
mkdir -p /var/log/gunicorn
chown -R www-data:www-data /var/log/gunicorn
chmod -R 755 /var/log/gunicorn

if [ -d "$PROJECT_DIR" ]; then
  chown -R www-data:www-data "$PROJECT_DIR"
  echo -e "${GREEN}✓ Droits assignés à www-data pour $PROJECT_DIR${NC}"
else
  echo -e "${YELLOW}⚠️ Attention : Le dossier $PROJECT_DIR n'a pas été trouvé. Vérifiez le chemin.${NC}"
fi

# 3. Installation et activation du service Systemd Gunicorn
echo -e "\n${YELLOW}⚙️  [2/5] Configuration du service Gunicorn...${NC}"
cp "$PROJECT_DIR/deploy/$GUNICORN_SERVICE_NAME.service" "/etc/systemd/system/$GUNICORN_SERVICE_NAME.service"

systemctl daemon-reload
systemctl enable "$GUNICORN_SERVICE_NAME"
systemctl restart "$GUNICORN_SERVICE_NAME"
echo -e "${GREEN}✓ Service Gunicorn ($GUNICORN_SERVICE_NAME) activé et démarré.${NC}"

# 4. Configuration et activation du site Nginx
echo -e "\n${YELLOW}🌐 [3/5] Configuration du serveur web Nginx...${NC}"
cp "$PROJECT_DIR/deploy/$NGINX_CONF_NAME" "/etc/nginx/sites-available/$NGINX_CONF_NAME"

# Création du lien symbolique s'il n'existe pas déjà
ln -sf "/etc/nginx/sites-available/$NGINX_CONF_NAME" "/etc/nginx/sites-enabled/$NGINX_CONF_NAME"

# 5. Test de la configuration Nginx et rechargement
echo -e "\n${YELLOW}🔍 [4/5] Test de la syntaxe Nginx...${NC}"
nginx -t

echo -e "\n${YELLOW}🔄 [5/5] Rechargement de Nginx...${NC}"
systemctl enable nginx
systemctl restart nginx
echo -e "${GREEN}✓ Nginx configuré et rechargé avec succès.${NC}"

# Résumé des statuts
echo -e "\n${BLUE}======================================================${NC}"
echo -e "${GREEN}  🎉 Les 2 services sont maintenant actifs et prêts ! ${NC}"
echo -e "${BLUE}======================================================${NC}"
echo -e "• Gunicorn : $(systemctl is-active $GUNICORN_SERVICE_NAME)"
echo -e "• Nginx    : $(systemctl is-active nginx)"
echo -e "\n${BLUE}👉 Prochaine étape : Vous pouvez maintenant exécuter le script de déploiement :${NC}"
echo -e "   bash deploy/deploy.sh\n"
