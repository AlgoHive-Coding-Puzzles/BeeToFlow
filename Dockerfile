FROM python:3.9-slim

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY entrypoint.py /app/entrypoint.py

# Définir le script comme exécutable
RUN chmod +x /app/entrypoint.py

# Définir le point d'entrée
ENTRYPOINT ["python", "/app/entrypoint.py"]
