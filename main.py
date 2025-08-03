import os
import subprocess
from datetime import datetime

# Ruta de tu servidor
MINECRAFT_DIR = '/home/nicolas/Descargas/bedrock-server-1.21.95.1'  # Ajusta según corresponda

# Carpeta donde guardar el backup
BACKUP_DIR = '/home/nicolas/backups'
os.makedirs(BACKUP_DIR, exist_ok=True)

# Nombre del archivo con fecha
fecha = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
zip_filename = f'minecraft_backup_{fecha}.zip'
zip_path = os.path.join(BACKUP_DIR, zip_filename)

print("🛑 Deteniendo el servidor...")
subprocess.run(['sudo', 'systemctl', 'stop', 'minecraft-bedrock.service'])

print("📦 Comprimiendo archivos...")
subprocess.run(['zip', '-r', zip_path, MINECRAFT_DIR])

print(f"✅ Backup creado: {zip_path}")

print("🚀 Reiniciando el servidor...")
subprocess.run(['sudo', 'systemctl', 'start', 'minecraft-bedrock.service'])

print("✅ Proceso completo.")
