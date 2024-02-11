# Nombre de travailleurs (workers) Gunicorn à utiliser
workers = 3

# Adresse et port sur lesquels Gunicorn doit écouter
bind = '0.0.0.0:8000'

# Chemin vers le fichier de logs de Gunicorn
errorlog = 'gunicorn/error.log'