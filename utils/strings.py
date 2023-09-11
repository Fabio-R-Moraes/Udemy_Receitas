def e_um_numero_positivo(value):
    try:
        number_string = float(value)
    except ValueError:
        return False

    return number_string > 0

#print(e_um_numero_positivo('10'))
