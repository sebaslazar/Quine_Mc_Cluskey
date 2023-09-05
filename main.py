def obtener_minterms():
    while True:
        terminos = input("Ingrese los minterms separados por comas: ").split(",")

        try:
            minterms = [int(termino.strip()) for termino in terminos]
        except ValueError:
            print("Error: Ingrese solo números enteros.")
            continue

        if any(minterm < 0 for minterm in minterms):
            print("Error: Los minterms deben ser números enteros no negativos.")
            continue

        max_minterm = max(minterms)
        num_variables = len(bin(max_minterm)) - 2  # Restamos 2 para excluir el '0b' de la representación binaria
        mostrar_tabla(minterms, num_variables)
        break


def mostrar_tabla(minterms, num_variables):
    tabla = {}
    print("\n-> Minterms ingresados:")

    for minterm in minterms:
        binario = obtener_binario(minterm, num_variables)
        print("{:<10} - {}".format(minterm, binario))
        tabla[minterm] = list(binario)

    ordenar_minterm(tabla, minterms)  # Pasa num_variables a la función


def obtener_binario(numero, num_variables):
    return format(numero, '0{}b'.format(num_variables))


def ordenar_minterm(tabla, minterms):
    tabla_ordenada = {}
    contador = 0
    cantidad_maxima_unos = calcular_cantidad_maxima_unos(tabla)

    while contador <= cantidad_maxima_unos:
        verificador = False
        for minterm, binario in tabla.items():
            if binario.count('1') == contador:
                tabla_ordenada[str(minterm)] = binario
                verificador = True
        if verificador:
            tabla_ordenada["-" + str(contador + 1)] = "-" + str(contador + 1)  # marcador divisor de cantidad de unos
        contador = contador + 1

    tabla_ordenada = corregidor_de_tabla(tabla_ordenada)

    mostrar_tabla_visual(tabla_ordenada)
    aparear(tabla_ordenada, cantidad_maxima_unos, {}, {}, minterms, {}, [])


def mostrar_tabla_visual(tabla_ordenada):
    grupos = {}  # Diccionario para agrupar minterms por cantidad de unos

    for minterm, binario in tabla_ordenada.items():
        if not minterm.startswith('-'):
            cantidad_unos = binario.count('1')
            if cantidad_unos not in grupos:
                grupos[cantidad_unos] = []
            grupos[cantidad_unos].append((minterm, binario))

    max_minterms = max(len(minterms) for minterms in grupos.values())

    print("\n\n-> Minterms ordenados:")
    print("Grupo\t\tMinterms\t\tBinarios")
    print("-----------------------------------------------")

    for grupo, minterms in grupos.items():
        grupo_str = str(grupo)
        print(f"{grupo_str}\t\t")

        for i in range(max_minterms):
            minterms_str = ', '.join(minterm for j, (minterm, _) in enumerate(minterms) if j == i)
            binarios_str = ', '.join(' '.join(binario) for j, (_, binario) in enumerate(minterms) if j == i)
            print(f"\t\t{minterms_str}\t\t{binarios_str}")
        print("-----------------------------------------------")


def calcular_cantidad_maxima_unos(tabla):
    cantidad_maxima_unos = 0
    lista_de_binarios = list(tabla.values())
    for binario in lista_de_binarios:
        cantidad_actual_unos = binario.count('1')
        if cantidad_actual_unos > cantidad_maxima_unos:
            cantidad_maxima_unos = cantidad_actual_unos
    return cantidad_maxima_unos


def aparear(tabla_ordenada, cantidad_maxima_unos, no_apareos_backup, backup_tabla, minterms, no_apareados_global, apareados):
    nueva_tabla = {}
    no_apareados = {}
    apareado = {}
    contador_divisores = 0
    contador = -1
    total_de_divisores = 0
    verificador_de_apareo = False
    # Recorremos los minterms ordenados en busca de apareamientos
    for minterm in tabla_ordenada.keys():
        if "-" in minterm:
            total_de_divisores = total_de_divisores + 1
    for minterm, minterm_binario in tabla_ordenada.items():
        identificador = False
        verificador_de_no_apareo = True

        # Solo consideramos los minterms que no contienen "-"
        if "-" not in minterm:
            for minterm_comparado, minterm_binario_comparado in tabla_ordenada.items():
                if identificador and "-" not in minterm_comparado:
                    # Verificamos si hay un apareamiento
                    if sum(i != j for i, j in zip(minterm_binario, minterm_binario_comparado)) == 1:
                        # Realizamos el apareamiento
                        lista_resultante = [t if t == tc else "-" for t, tc in
                                            zip(minterm_binario, minterm_binario_comparado)]
                        nueva_tabla[f"{minterm}, {minterm_comparado}"] = lista_resultante
                        verificador_de_apareo = True
                        verificador_de_no_apareo = False
                        apareado[minterm_comparado] = minterm_binario_comparado
                        apareados.append(minterm_comparado)

                if minterm_comparado == str(contador):
                    identificador = True
                if minterm_comparado == str(contador - 1) and identificador:
                    identificador = False
                    break

            if verificador_de_no_apareo:
                no_apareados[str(minterm)] = minterm_binario
                no_apareados_global[str(minterm)] = minterm_binario

        else:
            if int(minterm) > int(cantidad_maxima_unos) * -1:
                if verificador_de_apareo:
                    nueva_tabla[str(contador)] = str(contador)
                contador_divisores += 1
                contador -= 1
    if verificador_de_apareo:
        nueva_tabla = corregidor_de_tabla(nueva_tabla)  # Corregir tabla de negativos
        for minterm_apareado, binario_apareado in apareado.items():
            if binario_apareado in list(no_apareados.values()):
                del no_apareados[minterm_apareado]
        print("\n\n-> Apareo:")
        print("+--------------+---------------------+")
        print("| Implicante   | Binario             |")
        print("+--------------+---------------------+")
        combinaciones_impresas = set()  # Conjunto para rastrear combinaciones ya impresas
        for implicante, binario in nueva_tabla.items():
            if "-" not in implicante:
                combinaciones = tuple(sorted(implicante.split(", ")))  # Convertir a tupla ordenada
                if combinaciones not in combinaciones_impresas:
                    no_apareados[implicante] = binario
                    binario_str = ' '.join(binario)  # Convert binario list to string
                    implicante_str = ', '.join(implicante.split(", "))  # Separar por coma y espacio
                    print("{:<14}   {:<19}".format(implicante_str, binario_str))
                    combinaciones_impresas.add(combinaciones)  # Agregar combinación al conjunto
        print("+--------------+---------------------+")
        aparear(nueva_tabla, contador_divisores, no_apareados, nueva_tabla, minterms, no_apareados_global, apareados)
    else:
        temporal = {}
        temporal_2 = {}
        temp_data = []
        for termino, binario in no_apareos_backup.items():
            if len(temporal) > 0:
                if binario not in temporal.values():
                    temporal[termino] = binario
            else:
                temporal[termino] = binario
        no_apareos_backup = temporal.copy()
        no_apareados_global.update(no_apareos_backup)
        for termino, binario in no_apareados_global.items():
            if len(temporal_2) > 0:
                if binario not in temporal_2.values():
                    temporal_2[termino] = binario
            else:
                temporal_2[termino] = binario
        no_apareados_global = temporal_2.copy()
        for termino, binario in no_apareados_global.items():
            for elemento in apareados:
                if elemento not in temp_data:
                    if elemento == termino:
                        temp_data.append(elemento)
        for elemento in temp_data:
            del no_apareados_global[elemento]
        print("NO APAREADOS_GLOBAL: " + str(no_apareados_global))
        ordenar_implicantes(backup_tabla, no_apareados_global, minterms)


def corregidor_de_tabla(nueva_tabla):
    contador = -1
    errores = {}
    for minterm, binario in nueva_tabla.items():
        if "-" in minterm:
            if int(minterm) != contador:
                errores[minterm] = str(contador)
            contador = contador - 1
    if len(errores) > 0:
        for error, correccion in errores.items():
            nueva_tabla = {correccion if k == error else k: v for k, v in nueva_tabla.items()}
            nueva_tabla[correccion] = correccion
    return nueva_tabla


def ordenar_implicantes(tabla_final, no_apareados, minterms):
    print("\n\n-> Tabla final:")
    print("+--------------+---------------------+")
    print("| Implicante   | Binario             |")
    print("+--------------+---------------------+")
    combinaciones_impresas = set()  # Conjunto para rastrear combinaciones ya impresas
    for implicante, binario in tabla_final.items():
        if "-" not in implicante:
            combinaciones = tuple(sorted(implicante.split(", ")))  # Convertir a tupla ordenada
            if combinaciones not in combinaciones_impresas:
                no_apareados[implicante] = binario
                binario_str = ' '.join(binario)  # Convert binario list to string
                implicante_str = ', '.join(implicante.split(", "))  # Separar por coma y espacio
                print("{:<14}   {:<19}".format(implicante_str, binario_str))
                combinaciones_impresas.add(combinaciones)  # Agregar combinación al conjunto
    print("+--------------+---------------------+")
    imprimir_tabla_implicantes_primarios(no_apareados, minterms)


def imprimir_tabla_implicantes_primarios(tabla_ordenada, minterms):
    print("\n-> Impresión de los implicantes primos esenciales:")

    header = "  Mintérminos  | " + " ".join(str(m).center(6) for m in minterms)
    separator = "=" * (len(header))
    print(header)
    print(separator)

    combinaciones_impresas = set()  # Conjunto para rastrear combinaciones ya impresas

    for implicant in tabla_ordenada:
        if not any(term.startswith('-') for term in implicant.split(", ")):
            implicant_terms = implicant.split(", ")
            implicant_terms_str = " ".join(str(term) for term in implicant_terms)
            row = "{:<14} |".format(implicant_terms_str)

            combinaciones = tuple(sorted(implicant_terms))  # Convertir a tupla ordenada

            if combinaciones not in combinaciones_impresas:
                row_data = []  # Lista para almacenar datos de la fila

                for minterm in minterms:
                    if any(str(minterm) == term for term in implicant_terms):
                        row_data.append("X".center(6))  # Alinear la X con la columna
                    else:
                        row_data.append(" ".center(6))

                row += " ".join(data for data in row_data)  # Alinear las X
                print(row)
                print(separator)

                combinaciones_impresas.add(combinaciones)  # Agregar combinación al conjunto
    if not tabla_ordenada:
        print("No se encontraron implicantes primos esenciales.")
    tabla_de_mc_cluskey(tabla_ordenada, minterms, 1)


def tabla_de_mc_cluskey(tabla_ordenada, minterms, contador):
    minterms_elegidos = []
    posibles_implicantes = []
    ecuacion = []
    ecuacion_final = []
    verificador = True
    while verificador:
        verificador = False
        for minterm in minterms:
            if minterm not in minterms_elegidos:  # Verifica que la columna no esté propagada
                for numerico, binario in tabla_ordenada.items():
                    if binario not in ecuacion or contador == 1:  # verifica que la fila no esté propagada
                        nuevo_numerico = numerico.split(",")
                        nuevo_numerico_final = [eval(i) for i in nuevo_numerico]
                        if minterm in nuevo_numerico_final:  # verica que haya una marca en la fila y columna
                            # correspondiente
                            posibles_implicantes.append(binario)
                if len(posibles_implicantes) == contador:
                    if contador > 1:
                        columnas_con_marca = []
                        longitud = []
                        for p_implicantes in posibles_implicantes:
                            lista_temporal = []
                            for a, b in tabla_ordenada.items():
                                if b == p_implicantes:
                                    llave = a
                            llave = llave.split(",")
                            llave = [eval(i) for i in llave]
                            for objeto in llave:
                                if objeto not in minterms_elegidos:
                                    lista_temporal.append(objeto)
                            columnas_con_marca.append(lista_temporal)
                        if len(columnas_con_marca) > 1:
                            for x in columnas_con_marca:
                                longitud.append(len(x))
                            max_marcas = longitud[0]
                            igualdad = True
                            for y in longitud:
                                if max_marcas != y:
                                    igualdad = False
                                    max_marcas = max(max_marcas, y)
                            if igualdad:
                                ecuacion.append(posibles_implicantes[0])
                            else:
                                contador = 0
                                for z in columnas_con_marca:
                                    if len(z) == max_marcas:
                                        marcador = contador
                                    contador = contador + 1
                                ecuacion.append(posibles_implicantes[marcador])
                            for elemento in ecuacion:  # Propaga las columnas restantes
                                for termino, binario in tabla_ordenada.items():  # Recupera el valor numérico del
                                    # binario en la ecuación final
                                    if binario == elemento:
                                        lista = termino
                                lista_strings = lista.split(",")
                                lista_numeros = [eval(i) for i in lista_strings]
                                for elemento in lista_numeros:
                                    if elemento not in minterms_elegidos:
                                        minterms_elegidos.append(elemento)
                        elif len(columnas_con_marca) == 1:
                            ecuacion.append(posibles_implicantes[0])
                    else:
                        ecuacion.append(posibles_implicantes[0])
                    minterms_elegidos.append(minterm)
                    verificador = True
                posibles_implicantes.clear()
        for elemento in ecuacion:  # Elimina los posibles terminos redundantes
            if elemento not in ecuacion_final:
                ecuacion_final.append(elemento)
        for elemento in ecuacion_final:  # Propaga las columnas restantes
            for termino, binario in tabla_ordenada.items():  # Recupera el valor numérico del binario en la ecuación
                # final
                if binario == elemento:
                    lista = termino
            lista_strings = lista.split(",")
            lista_numeros = [eval(i) for i in lista_strings]
            for elemento in lista_numeros:
                if elemento not in minterms_elegidos:
                    minterms_elegidos.append(elemento)
        contador = contador + 1
        ecuacion.clear()
        print("Minterms elegidos: " + str(minterms_elegidos))
    print(ecuacion_final)
    expresion_final = ecuacion_mccluskey(ecuacion_final)
    print("Expresión Final: " + expresion_final)


def ecuacion_mccluskey(ecuacion_final):
    num_terminos = len(ecuacion_final)  # Número de términos
    num_variables = len(ecuacion_final[0])  # Número de variables basado en la longitud del primer término

    # Generar una lista de letras para las variables (A, B, C, ...)
    letras_variables = [chr(65 + i) for i in range(num_variables)]

    expresion_simplificada = []

    for i in range(num_terminos):
        termino = ecuacion_final[i]
        expresion_termino = []
        for j in range(num_variables):
            valor = termino[j]
            letra_variable = letras_variables[j]
            if valor == '0':
                expresion_termino.append(letra_variable + "'")
            elif valor == '1':
                expresion_termino.append(letra_variable)
        if expresion_termino:
            expresion_simplificada.append(''.join(expresion_termino))

    # Unir todos los términos en la expresión final
    expresion_final = ' + '.join(expresion_simplificada)

    return expresion_final


print("Bienvenido al Simplificador de Expresiones usando Quine-McCluskey")
obtener_minterms()

