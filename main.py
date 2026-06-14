# ==========================================================
# TPI - Programación I
# Gestión de Datos de Países en Python
# Alumno: Rodolfo Gutierrez
# ==========================================================

import csv

ARCHIVO_CSV = "paises.csv"


def normalizar_texto(texto):
    """
    Elimina espacios y convierte el texto a minúsculas.
    """
    return texto.strip().lower()


def validar_continente(continente):
    """
    Valida que el continente ingresado sea correcto.
    """
    continentes_validos = ["america", "américa", "europa", "asia", "africa", "áfrica", "oceania", "oceanía"]

    if normalizar_texto(continente) not in continentes_validos:
        raise ValueError("Continente inválido. Debe ser: América, Europa, Asia, África u Oceanía.")

    continente_normalizado = normalizar_texto(continente)

    if continente_normalizado in ["america", "américa"]:
        return "América"
    elif continente_normalizado == "europa":
        return "Europa"
    elif continente_normalizado == "asia":
        return "Asia"
    elif continente_normalizado in ["africa", "áfrica"]:
        return "África"
    else:
        return "Oceanía"


def pedir_entero(mensaje):
    """
    Solicita un número entero al usuario.
    """
    try:
        return int(input(mensaje))
    except ValueError:
        raise ValueError("Debe ingresar un número entero válido.")


def pedir_texto_no_vacio(mensaje):
    """
    Solicita texto y valida que no esté vacío.
    """
    texto = input(mensaje).strip()

    if texto == "":
        raise ValueError("El campo no puede estar vacío.")

    return texto


def validar_numero_positivo(numero, campo):
    """
    Valida que un número no sea negativo.
    """
    if numero < 0:
        raise ValueError(f"{campo} no puede ser negativo.")

    return numero


def buscar_pais_en_lista(paises, nombre):
    """
    Busca un país por nombre exacto.
    """
    nombre_normalizado = normalizar_texto(nombre)

    for pais in paises:
        if normalizar_texto(pais["nombre"]) == nombre_normalizado:
            return pais

    return None


def cargar_paises_desde_csv(nombre_archivo):
    """
    Carga países desde un archivo CSV.
    """
    paises = []

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                try:
                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": validar_continente(fila["continente"])
                    }

                    if pais["nombre"] != "":
                        paises.append(pais)

                except (ValueError, KeyError):
                    print("Advertencia: una fila del CSV tiene formato inválido y fue omitida.")

    except FileNotFoundError:
        print("Error: no se encontró el archivo paises.csv.")
        print("El programa iniciará sin datos.")

    return paises


def guardar_paises_en_csv(nombre_archivo, paises):
    """
    Guarda los países en el archivo CSV.
    """
    try:
        with open(nombre_archivo, "w", encoding="utf-8", newline="") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            escritor.writeheader()

            for pais in paises:
                escritor.writerow(pais)

        print("Datos guardados correctamente en el archivo CSV.")

    except Exception as error:
        print("Error al guardar el archivo:", error)


def mostrar_paises(paises):
    """
    Muestra el listado de países.
    """
    print("\n--- LISTADO DE PAÍSES ---")

    if len(paises) == 0:
        print("No hay países para mostrar.")
        return

    for pais in paises:
        print(
            f"Nombre: {pais['nombre']} | "
            f"Población: {pais['poblacion']} | "
            f"Superficie: {pais['superficie']} km² | "
            f"Continente: {pais['continente']}"
        )


def agregar_pais(paises):
    """
    Agrega un país nuevo.
    """
    print("\n--- AGREGAR PAÍS ---")

    try:
        nombre = pedir_texto_no_vacio("Ingrese nombre del país: ")

        if buscar_pais_en_lista(paises, nombre) is not None:
            raise ValueError("El país ya existe en el sistema.")

        poblacion = pedir_entero("Ingrese población: ")
        poblacion = validar_numero_positivo(poblacion, "La población")

        superficie = pedir_entero("Ingrese superficie en km²: ")
        superficie = validar_numero_positivo(superficie, "La superficie")

        continente = pedir_texto_no_vacio("Ingrese continente: ")
        continente = validar_continente(continente)

        nuevo_pais = {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente
        }

        paises.append(nuevo_pais)
        print("País agregado correctamente.")

    except ValueError as error:
        print("Error:", error)


def actualizar_pais(paises):
    """
    Actualiza población y superficie de un país existente.
    """
    print("\n--- ACTUALIZAR PAÍS ---")

    if len(paises) == 0:
        print("No hay países cargados.")
        return

    nombre = input("Ingrese el nombre del país a actualizar: ").strip()
    pais = buscar_pais_en_lista(paises, nombre)

    if pais is None:
        print("No se encontró el país solicitado.")
        return

    print(f"País encontrado: {pais['nombre']}")
    print(f"Población actual: {pais['poblacion']}")
    print(f"Superficie actual: {pais['superficie']} km²")
    print(f"Continente actual: {pais['continente']}")

    try:
        nueva_poblacion = pedir_entero("Ingrese nueva población: ")
        nueva_poblacion = validar_numero_positivo(nueva_poblacion, "La población")

        nueva_superficie = pedir_entero("Ingrese nueva superficie en km²: ")
        nueva_superficie = validar_numero_positivo(nueva_superficie, "La superficie")

        nuevo_continente = pedir_texto_no_vacio("Ingrese nuevo continente: ")
        nuevo_continente = validar_continente(nuevo_continente)

        pais["poblacion"] = nueva_poblacion
        pais["superficie"] = nueva_superficie
        pais["continente"] = nuevo_continente

        print("Datos actualizados correctamente.")

    except ValueError as error:
        print("Error:", error)


def eliminar_pais(paises):
    """
    Elimina un país del sistema, previa confirmación del usuario.
    """
    print("\n--- ELIMINAR PAÍS ---")

    if len(paises) == 0:
        print("No hay países cargados.")
        return

    nombre = input("Ingrese el nombre del país a eliminar: ").strip()
    pais = buscar_pais_en_lista(paises, nombre)

    if pais is None:
        print("No se encontró el país solicitado.")
        return

    print(
        f"País encontrado: {pais['nombre']} | "
        f"Población: {pais['poblacion']} | "
        f"Superficie: {pais['superficie']} km² | "
        f"Continente: {pais['continente']}"
    )

    confirmacion = input("¿Confirma que desea eliminar este país? (S/N): ").strip().upper()

    if confirmacion == "S":
        paises.remove(pais)
        print("País eliminado correctamente.")
    else:
        print("Operación cancelada.")


def buscar_pais(paises):
    """
    Busca países por nombre o parte del nombre.
    """
    print("\n--- BUSCAR PAÍS ---")

    if len(paises) == 0:
        print("No hay países cargados.")
        return

    texto = input("Ingrese nombre o parte del nombre del país: ").strip().lower()

    if texto == "":
        print("Error: debe ingresar un texto de búsqueda.")
        return

    resultados = []

    for pais in paises:
        if texto in pais["nombre"].lower():
            resultados.append(pais)

    if len(resultados) == 0:
        print("No se encontraron países con ese criterio.")
    else:
        mostrar_paises(resultados)


def filtrar_paises(paises):
    """
    Menú de filtros.
    """
    print("\n--- FILTRAR PAÍSES ---")

    if len(paises) == 0:
        print("No hay países cargados.")
        return

    print("1. Filtrar por continente")
    print("2. Filtrar por rango de población")
    print("3. Filtrar por rango de superficie")

    try:
        opcion = pedir_entero("Seleccione una opción: ")

        if opcion == 1:
            filtrar_por_continente(paises)
        elif opcion == 2:
            filtrar_por_poblacion(paises)
        elif opcion == 3:
            filtrar_por_superficie(paises)
        else:
            print("Error: opción de filtro inválida.")

    except ValueError as error:
        print("Error:", error)


def filtrar_por_continente(paises):
    """
    Filtra países por continente.
    """
    try:
        continente = pedir_texto_no_vacio("Ingrese continente: ")
        continente = validar_continente(continente)

        resultados = []

        for pais in paises:
            if normalizar_texto(pais["continente"]) == normalizar_texto(continente):
                resultados.append(pais)

        if len(resultados) == 0:
            print("No se encontraron países para ese continente.")
        else:
            mostrar_paises(resultados)

    except ValueError as error:
        print("Error:", error)


def filtrar_por_poblacion(paises):
    """
    Filtra países por rango de población.
    """
    try:
        minimo = pedir_entero("Ingrese población mínima: ")
        maximo = pedir_entero("Ingrese población máxima: ")

        validar_numero_positivo(minimo, "La población mínima")
        validar_numero_positivo(maximo, "La población máxima")

        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo.")

        resultados = []

        for pais in paises:
            if minimo <= pais["poblacion"] <= maximo:
                resultados.append(pais)

        if len(resultados) == 0:
            print("No se encontraron países en ese rango de población.")
        else:
            mostrar_paises(resultados)

    except ValueError as error:
        print("Error:", error)


def filtrar_por_superficie(paises):
    """
    Filtra países por rango de superficie.
    """
    try:
        minimo = pedir_entero("Ingrese superficie mínima: ")
        maximo = pedir_entero("Ingrese superficie máxima: ")

        validar_numero_positivo(minimo, "La superficie mínima")
        validar_numero_positivo(maximo, "La superficie máxima")

        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo.")

        resultados = []

        for pais in paises:
            if minimo <= pais["superficie"] <= maximo:
                resultados.append(pais)

        if len(resultados) == 0:
            print("No se encontraron países en ese rango de superficie.")
        else:
            mostrar_paises(resultados)

    except ValueError as error:
        print("Error:", error)


def ordenar_paises(paises):
    """
    Ordena países por nombre, población o superficie.
    """
    print("\n--- ORDENAR PAÍSES ---")

    if len(paises) == 0:
        print("No hay países cargados.")
        return

    print("1. Ordenar por nombre")
    print("2. Ordenar por población")
    print("3. Ordenar por superficie")

    try:
        criterio = pedir_entero("Seleccione criterio de ordenamiento: ")

        print("1. Ascendente")
        print("2. Descendente")

        orden = pedir_entero("Seleccione tipo de orden: ")

        if orden == 1:
            reverso = False
        elif orden == 2:
            reverso = True
        else:
            raise ValueError("Tipo de orden inválido.")

        if criterio == 1:
            paises_ordenados = sorted(paises, key=lambda pais: pais["nombre"].lower(), reverse=reverso)
        elif criterio == 2:
            paises_ordenados = sorted(paises, key=lambda pais: pais["poblacion"], reverse=reverso)
        elif criterio == 3:
            paises_ordenados = sorted(paises, key=lambda pais: pais["superficie"], reverse=reverso)
        else:
            raise ValueError("Criterio de ordenamiento inválido.")

        mostrar_paises(paises_ordenados)

    except ValueError as error:
        print("Error:", error)


def mostrar_estadisticas(paises):
    """
    Muestra estadísticas generales.
    """
    print("\n--- ESTADÍSTICAS ---")

    if len(paises) == 0:
        print("No hay países cargados.")
        return

    pais_mayor_poblacion = max(paises, key=lambda pais: pais["poblacion"])
    pais_menor_poblacion = min(paises, key=lambda pais: pais["poblacion"])

    total_poblacion = 0
    total_superficie = 0

    for pais in paises:
        total_poblacion += pais["poblacion"]
        total_superficie += pais["superficie"]

    promedio_poblacion = total_poblacion / len(paises)
    promedio_superficie = total_superficie / len(paises)

    print(f"País con mayor población: {pais_mayor_poblacion['nombre']} ({pais_mayor_poblacion['poblacion']})")
    print(f"País con menor población: {pais_menor_poblacion['nombre']} ({pais_menor_poblacion['poblacion']})")
    print(f"Promedio de población: {promedio_poblacion:.2f}")
    print(f"Promedio de superficie: {promedio_superficie:.2f} km²")

    mostrar_cantidad_por_continente(paises)


def mostrar_cantidad_por_continente(paises):
    """
    Cuenta países por continente.
    """
    conteo = {}

    for pais in paises:
        continente = pais["continente"]

        if continente in conteo:
            conteo[continente] += 1
        else:
            conteo[continente] = 1

    print("\nCantidad de países por continente:")

    for continente, cantidad in conteo.items():
        print(f"{continente}: {cantidad}")


def mostrar_menu():
    """
    Muestra el menú principal.
    """
    print("\n====================================")
    print(" SISTEMA DE GESTIÓN DE PAÍSES")
    print("====================================")
    print("1. Mostrar países")
    print("2. Agregar país")
    print("3. Actualizar país")
    print("4. Buscar país por nombre")
    print("5. Filtrar países")
    print("6. Ordenar países")
    print("7. Mostrar estadísticas")
    print("8. Guardar cambios en CSV")
    print("9. Eliminar país")
    print("0. Salir")


def main():
    """
    Función principal del programa.
    """
    paises = cargar_paises_desde_csv(ARCHIVO_CSV)

    while True:
        mostrar_menu()

        try:
            opcion = pedir_entero("Seleccione una opción: ")

            if opcion == 1:
                mostrar_paises(paises)
            elif opcion == 2:
                agregar_pais(paises)
            elif opcion == 3:
                actualizar_pais(paises)
            elif opcion == 4:
                buscar_pais(paises)
            elif opcion == 5:
                filtrar_paises(paises)
            elif opcion == 6:
                ordenar_paises(paises)
            elif opcion == 7:
                mostrar_estadisticas(paises)
            elif opcion == 8:
                guardar_paises_en_csv(ARCHIVO_CSV, paises)
            elif opcion == 9:
                eliminar_pais(paises)
            elif opcion == 0:
                guardar_paises_en_csv(ARCHIVO_CSV, paises)
                print("Fin del programa.")
                break
            else:
                print("Error: opción fuera de rango.")

        except ValueError as error:
            print("Error:", error)


main()