from markupsafe import escape

class Sanitizador:

    @staticmethod
    def limpiar_email(email):
        if not email:
            return ""
        # Quita los espacios al inicio al final y convierte todo en minusculas
        return email.strip().lower()
    
    @staticmethod
    def limpiar_texto(texto):
        if not texto:
            return ""
        #Quita espacios extra
        texto_limpio = texto.strip()

        # Escapa caracteres HTML para evitar inyeccion de codigo XSS
        texto_limpio = escape(texto_limpio)
        return str(texto_limpio) 