#Validaciones
import re


# -----------------------------------------------------------------------
# TEXTO OBLIGATORIO (referencia, descripción, nombre, apellidos, etc.)
#
# nombre_campo va SIN artículo (ej. "Referencia", no "La referencia"),
# así el mensaje no tiene problemas de concordancia de género.
# -----------------------------------------------------------------------
def validar_texto_obligatorio(texto, nombre_campo):

    texto = texto.strip()

    if texto == "":
        return False, f"Debe completar el campo '{nombre_campo}'."

    return True, texto


# -----------------------------------------------------------------------
# NÚMERO ENTERO (horas de capacitación, cédula, etc.)
# -----------------------------------------------------------------------
def validar_entero(texto, nombre_campo):

    texto = texto.strip()

    if not texto.isdigit():
        return False, f"El campo '{nombre_campo}' debe ser un número entero."

    return True, int(texto)


# -----------------------------------------------------------------------
# NÚMERO DECIMAL (horas de asesoría)
# Acepta tanto punto como coma para los decimales (2.5 o 2,5)
# -----------------------------------------------------------------------
def validar_decimal(texto, nombre_campo):

    texto = texto.strip().replace(",", ".")

    try:
        valor = float(texto)
    except ValueError:
        return False, f"El campo '{nombre_campo}' debe ser un número decimal."

    if valor < 0:
        return False, f"El campo '{nombre_campo}' no puede ser negativo."

    return True, valor


# -----------------------------------------------------------------------
# FECHA FINAL CONTRA FECHA INICIAL
# -----------------------------------------------------------------------
def validar_fechas(fecha_inicio, fecha_final):

    if fecha_final < fecha_inicio:
        return False, "La fecha final no puede ser menor que la fecha inicial."

    return True, None


# -----------------------------------------------------------------------
# CORREO ELECTRÓNICO (para Estudiantes, por si se necesita)
# -----------------------------------------------------------------------
def validar_correo(correo):

    correo = correo.strip()

    patron = r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$"

    if not re.match(patron, correo):
        return False, "El correo electrónico no es válido."

    return True, correo


# -----------------------------------------------------------------------
# PRUEBA RÁPIDA:  python Validaciones.py
# -----------------------------------------------------------------------
if __name__ == "__main__":

    print(validar_texto_obligatorio("", "Referencia"))
    print(validar_texto_obligatorio("  PROG3-01 ", "Referencia"))
    print(validar_entero("12.5", "Horas de capacitación"))
    print(validar_entero("40", "Horas de capacitación"))
    print(validar_decimal("2,5", "Horas de asesoría"))
    print(validar_correo("correo_invalido"))
    print(validar_correo("ana@correo.com"))
