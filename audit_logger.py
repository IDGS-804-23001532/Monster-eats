# audit_logger.py
from pymongo import MongoClient
from datetime import datetime
from flask import request
from flask_security import current_user
import threading

class AuditLogger:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="monster_eats_audit"):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            self.db = self.client[db_name]
        except Exception as e:
            print(f"Error conectando a MongoDB: {e}")
            self.db = None

    def log_action(self, module_name, action, details=None, level="INFO"):
        """
        Guarda un registro de auditoría en la colección específica del módulo (module_name).
        """
        if self.db is None:
            return

        # 1. Recolectmos contexto del usuario y SUS ROLES
        if current_user and current_user.is_authenticated:
            user_id = current_user.id_usuario
            user_email = current_user.email
            # Extraemos los nombres de los roles que tiene el usuario actualmente
            user_roles = [role.name for role in current_user.roles] 
        else:
            user_id = "Anónimo"
            user_email = "N/A"
            user_roles = ["Sin Rol"]

        # 2. Recolectamos datos de red y petición
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr) if request else "Local"
        endpoint = request.endpoint if request else "N/A"
        method = request.method if request else "N/A"

        # 3. Armar el documento a guardar (para mongodb)
        log_entry = {
            "timestamp": datetime.utcnow(),
            "level": level,
            "user_id": user_id,
            "user_email": user_email,
            "user_roles": user_roles,
            "ip_address": ip_address,
            "endpoint": endpoint,
            "method": method,
            "action": action,
            "details": details or {}
        }

        # 4. Guardar en hilo separado apuntando a la colección dinámica (colección por módulo)
        def save_to_mongo(entry, collection):
            try:
                # self.db[collection] selecciona o crea la colección con el nombre del módulo
                self.db[collection].insert_one(entry)
            except Exception as e:
                print(f"Fallo al escribir log en MongoDB: {e}")

        # Pasamos el nombre del módulo al hilo para que sepa en qué colección guardarlo
        threading.Thread(target=save_to_mongo, args=(log_entry, module_name)).start()

# Instancia global
audit = AuditLogger()


#Respaldo de la base de datos de mysql a mongodb, para auditoría de seguridad y análisis forense en caso de incidentes.
