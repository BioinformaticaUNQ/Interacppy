def mutar_secuencia(secuencia, posicion, nuevo_residuo):
    """
    Esta función realiza una mutación en la secuencia en la posición indicada.
    
    Args:
    secuencia (str): La secuencia original de la proteína o ácido nucleico.
    posicion (int): La posición de la mutación (índice de la secuencia).
    nuevo_residuo (str): El nuevo residuo (base o aminoácido) que reemplazará al actual.
    
    Returns:
    str: La secuencia mutada.
    """
    # Asegurarse de que la posición está dentro de la secuencia
    if posicion < 0 or posicion >= len(secuencia):
        raise ValueError("La posición está fuera de los límites de la secuencia.")
    
    # Realizar la mutación
    secuencia_mutada = secuencia[:posicion] + nuevo_residuo + secuencia[posicion+1:]
    
    return secuencia_mutada


# Secuencia de ejemplo
secuencia_original = "ACGTAGCTAGC"

# Mutar la secuencia en la posición 3 (por ejemplo, cambiar 'T' por 'C')
secuencia_mutada = mutar_secuencia(secuencia_original, 3, "C")
print(f"Secuencia original: {secuencia_original}")
print(f"Secuencia mutada: {secuencia_mutada}")
