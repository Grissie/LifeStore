#from audioop import mul
import math
from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

"""
@proyect: Análisis de Datos de LifeStore
@curse: Fundamentos de Programación con Python - EmTech
@author: Griselda Gutiérrez S.   
"""

#********************************* Top 5 : Productos más vendidos *********************************
#Obtener los ids de los productos vendidos y agregarlos a la nueva lista
vendidos = []
for venta in lifestore_sales:
    #Se añade el id_product de la venta
    vendidos.append(venta[1])

#Crear diccionario para guardar los datos de los productos vendidos
productos_vendidos = {}

for producto in lifestore_products:
    #Mientras el id_product este en vendidos y no este como key en el diccionario
    if producto[0] in vendidos and producto[0] not in productos_vendidos.keys():
        #Crear una lista y agregar los campos
        productos_vendidos[producto[0]] = [] 
        #Obtener el índice de la primera ',' para subtraer el nombre del producto
        indice = producto[1].find(',')
        productos_vendidos[producto[0]].append(producto[1][:indice]) #Agrega nombre
        productos_vendidos[producto[0]].append(producto[3]) #Agrega categoría
        productos_vendidos[producto[0]].append(vendidos.count(producto[0])) #Agrega frecuencia de venta

#Ordenar diccionario por frecuencia de venta
productos_vendidos = sorted(productos_vendidos.items(), key=lambda x:x[1][2], reverse=True)



#********************************* Top 10 : Productos más buscados *********************************

#Obtener los ids de los productos vendidos y agregarlos a la nueva lista
buscados = []
for busqueda in lifestore_searches:
    #Se añade el id_product de la venta
    buscados.append(busqueda[1])

#Crear diccionario para guardar los datos de los productos buscados
productos_buscados = {}

for producto in lifestore_products:
    #Mientras el id_product este en vendidos y no este como key en el diccionario
    if producto[0] in buscados and producto[0] not in productos_buscados.keys():
        #Crear una lista y agregar los campos
        productos_buscados[producto[0]] = [] 
        #Obtener el índice de la primera ',' para subtraer el nombre del producto
        indice = producto[1].find(',')
        productos_buscados[producto[0]].append(producto[1][:indice]) #Agrega nombre
        productos_buscados[producto[0]].append(producto[3]) #Agrega categoría
        productos_buscados[producto[0]].append(buscados.count(producto[0])) #Agrega frecuencia de busqueda

#Ordenar diccionario por frecuencia de venta
productos_buscados = sorted(productos_buscados.items(), key=lambda x:x[1][2], reverse=True)



#********************************* Top 5 : Productos menos vendidos por categoría *********************************

#Hacer una copia de productos_vendidos y ordenar ascedentemente por frecuencia de venta
productos_vendidos_cp = sorted(productos_vendidos, key=lambda x:x[1][2], reverse=False)

#Crear un diccionario con las categorías
productos_por_categoria = {}
for producto in lifestore_products:
    if producto[3] not in productos_por_categoria.keys():
        productos_por_categoria[producto[3]] = []

#Agregar los productos por categoría
for key in productos_por_categoria.keys():
    for i in productos_vendidos_cp:
        #Mientras la categoría del producto sea igual a la llave, se agrega el producto
        if i[1][1] == key:
            productos_por_categoria[key].append(i)



#********************************* Top 5 : Productos menos buscados por categoría *********************************

#Hacer una copia de productos_buscadoss y ordenar ascedentemente por frecuencia de busqueda
productos_buscados_cp = sorted(productos_buscados, key=lambda x:x[1][2], reverse=False)

#Crear un diccionario con las categorías
productos_por_categoria_buscados = {}
for producto in lifestore_products:
    if producto[3] not in productos_por_categoria_buscados.keys():
        productos_por_categoria_buscados[producto[3]] = []

#Agregar los productos por categoría
for key in productos_por_categoria_buscados.keys():
    for i in productos_buscados_cp:
        #Mientras la categoría del producto sea igual a la llave, se agrega el producto
        if i[1][1] == key:
            productos_por_categoria_buscados[key].append(i)



#********************************* Top 5 : Productos con mejor reseña *********************************
#Obtener id_product y score de cada venta
resena_producto_venta = [[venta[1], venta[2]] for venta in lifestore_sales]

#Crear diccionario de la forma id_product:[score1, score2, ...]
resenas_producto = {}
for i in resena_producto_venta:
    #Mientras id_product no este como llave del diccionario, entonces se agrega
    if i[0] not in resenas_producto.keys():
        resenas_producto[i[0]] = []

#Agregar los score por cada id_product
for key in resenas_producto.keys():
    for i in resena_producto_venta:
        #Si el id_product es igual a la llave, entonces se agrega
        if i[0] == key:
            resenas_producto[key].append(i[1])

#Diccionario final que contiene el promedio de las reseñas
resenas_producto_final = {}

#Obtener el promedio de reseñas de cada producto
for key in resenas_producto.keys():
    #Obtener el promedio de reseñas de cada producto
    promedio_total = sum(resenas_producto[key])/(len(resenas_producto[key]))
    decimales = 2
    multiplicador = 10**decimales
    promedio_total = math.ceil(promedio_total*multiplicador)/multiplicador

    #Validar que la key actual no este el diccionario nuevo y agregar el valor de la reseña promedio
    if key not in resenas_producto_final.keys():
        resenas_producto_final[key] = []
        resenas_producto_final[key].append(promedio_total)

#Agregar datos del producto
for producto in lifestore_products:
    for key in resenas_producto_final.keys():
        #Mientras el id_product sea igual, se añaden los datos
        if key == producto[0]:
            indice = producto[1].find(',')
            resenas_producto_final[key].append(producto[1][:indice]) #Agrega nombre
            resenas_producto_final[key].append(producto[3]) #Agrega categoría

#Ordenar diccionario por el promedio de la reseña
resenas_producto_final = sorted(resenas_producto_final.items(), key=lambda x:x[1][0], reverse=True)



#********************************* Top 5 : Productos con peor reseña *********************************
resenas_producto_final_cp = sorted(resenas_producto_final, key=lambda x:x[1][0], reverse=False)



#********************************* Análisis de ventas e ingresos por mes *********************************

#Obtener el id_product y el mes de cada venta
producto_mes = [[venta[1], venta[3][3:5]] for venta in lifestore_sales if venta[4] == 0]

#Crear diccionario con los meses y con los ids_productos vendidos
ventas_por_mes = {}
for i in producto_mes:
    #Mientras el mes no este como llave, entonces se agrega
    if i[1] not in ventas_por_mes.keys():
        ventas_por_mes[i[1]] = []
    ventas_por_mes[i[1]].append(i[0])

#Crear diccionario con el total de ventas y total de ingresos
ventas_por_mes_final = {}

for key in ventas_por_mes.keys():
    #Obtener la lista de ids de los productos del mes actual
    lista = ventas_por_mes[key]
    suma = 0
    for i in lifestore_products:
        for j in lista:
            #Mientras el id_product sea el mismo
            if j == i[0]:
                #Se obtiene el precio del producto
                suma = suma + i[2]
    ventas_por_mes_final[key] = []
    ventas_por_mes_final[key].append(suma)
    ventas_por_mes_final[key].append(len(lista))
    
#Mapeo de digito a mes en letras
meses = [['01','Enero'],['02','Febrero'],['03','Marzo'],['04','Abril'],['05','Mayo'],['06','Junio'],
        ['07','Julio'],['08','Agosto'],['09','Septiembre'],['10','Octubre'],['11','Noviembre'],['12','Diciembre']]

#Diccionario final ya con los ingresos y ventas por mes
ventas_ingresos_por_mes = {}
for i in meses:
    for key in ventas_por_mes_final.keys():
        #Mientras la llaves sea igual al id de lista
        if key == i[0]:
            ventas_ingresos_por_mes[i[1]] = []
            ventas_ingresos_por_mes[i[1]] = ventas_por_mes_final[key]


#********************************* Menú principal *********************************
#Login principal
#Variable para limitar los intentos de acceso al sistema
intentos=0
opcion=0
while True:
    print("---------------------------------------------")
    print("| B I E N V E N I D O   A L   S I S T E M A |")
    print("---------------------------------------------")
    usuario=input("Ingrese su usuario: ")
    contrasena=input("Ingrese su contraseña: ")
    intentos+=1

    #Credenciales validas, entonces se muestra un menu del reporte
    if usuario=="SYS_admin" and contrasena=="SYS_admin123":
        #Menú interno
        while(True):
            print("\n")
            print("--------------------------------------------------")
            print("|        R E P O R T E   D E   V E N T A S       |")
            print("--------------------------------------------------")

            print("1. Top 5 de productos vendidos \n2. Top 10 de productos buscados \n3. Top 5 productos menos vendidos por categoría" +
                "\n4. Top 5 productos menos buscados por categoría \n5. Top 10 productos con mejor reseña \n6. Top 10 productos con peor reseña \n7. Ventas e ingresos por mes \n8. Salir")
            
            opcion = int(input("Elige una opción: "))
            
            if opcion == 1:
                print("\n")
                print("****** T O P  5 :   P R O D U C T O S   M Á S   V E N D I D O S ******")
                print("\n")
                #Imprimir los primeros 5 productos
                for i in productos_vendidos[:5]:
                    print("ID producto: " + str(i[0]) + " |", "Nombre: " + str(i[1][0]) + " |", "Categoría: " + str(i[1][1]) + " |", "Número de ventas: " + str(i[1][2]))
                print("\n")

            if opcion == 2:
                print("\n")
                print("****** T O P  10 :   P R O D U C T O S   M Á S   B U S C A D O S ******")
                print("\n")
                #Imprimir los primeros 10 productos
                for i in productos_buscados[:10]:
                    print("ID producto: " + str(i[0]) + " |", "Nombre: " + str(i[1][0]) + " |", "Categoría: " + str(i[1][1]) + " |", "Número de busquedas: " + str(i[1][2]))
                print("\n")

            if opcion == 3:
                print("\n")
                print("****** T O P  5 :   P R O D U C T O S   M E N O S   V E N D I D O S   P O R   C A T E G O R Í A ******")
                print("\n")
                #Imprimir diccionario
                for key in productos_por_categoria.keys():
                    print(">> Categoría: ", key)
                    tamano = len(productos_por_categoria[key])
                    #Si el tamaño de la lista de la llave es mayor a 5, solo se imprimen los primeros 5 productos
                    if tamano > 5:
                        for i in productos_por_categoria[key][:5]:
                            print("ID producto: " + str(i[0]) + " |", "Nombre: " + str(i[1][0]) + " |", "Número de ventas: " + str(i[1][2]))
                    else:
                    #Si el tamaño es menor o igual a cinco, se imprimen todos los productos
                        for i in productos_por_categoria[key]:
                            print("ID producto: " + str(i[0]) + " |", "Nombre: " + str(i[1][0]) + " |", "Número de ventas: " + str(i[1][2]))
                    print("\n")
                print("\n")

            if opcion == 4:
                print("\n")
                print("****** T O P  5 :   P R O D U C T O S   M E N O S   B U S C A D O S   P O R   C A T E G O R Í A ******")
                print("\n")
                #Imprimir diccionario
                for key in productos_por_categoria_buscados.keys():
                    print(">> Categoría: ", key)
                    tamano = len(productos_por_categoria_buscados[key])
                    #Si el tamaño de la lista de la llave es mayor a 5, solo se imprimen los primeros 5 productos
                    if tamano > 5:
                        for i in productos_por_categoria_buscados[key][:5]:
                            print("ID producto: " + str(i[0]) + " |", "Nombre: " + str(i[1][0]) + " |", "Número de búsquedas: " + str(i[1][2]))
                    
                    elif tamano == 0:
                        print("Sin búsquedas")
                    
                    else:
                    #Si el tamaño es menor o igual a cinco, se imprimen todos los productos
                        for i in productos_por_categoria_buscados[key]:
                            print("ID producto: " + str(i[0]) + " |", "Nombre: " + str(i[1][0]) + " |", "Número de búsquedas: " + str(i[1][2]))
                    print("\n")
                print("\n")

            if opcion == 5:
                print("\n")
                print("****** T O P  10 :   P R O D U C T O S   C O N   M E J O R   R E S E Ñ A ******")
                print("\n")
                #Imprimir los primeros diez productos
                for i in resenas_producto_final[:10]:
                    print("ID producto: " + str(i[0]) + " |", "Reseña promedio: " + str(i[1][0]) + " |", "Nombre: " + str(i[1][1]) + " |", "Categoría: " + str(i[1][2]))
                print("\n")

            if opcion == 6:
                print("\n")
                print("****** T O P  10 :   P R O D U C T O S   C O N   P E O R   R E S E Ñ A ******")
                print("\n")
            
                #Imprimir los primeros diez productos
                for i in resenas_producto_final_cp[:10]:
                    print("ID producto: " + str(i[0]) + " |", "Reseña promedio: " + str(i[1][0]) + " |", "Nombre: " + str(i[1][1]) + " |", "Categoría: " + str(i[1][2]))
                print("\n")

            if opcion == 7:
                print("\n")
                print("******  V E N T A S   E   I N G R E S O S   P O R   M E S ******")
                print("\n")
                for key in ventas_ingresos_por_mes.keys():
                    print("Mes: ", key)
                    print("Total de ingresos: $ " +str(ventas_ingresos_por_mes[key][0])+".00" + " | " +"Total de ventas: " +str(ventas_ingresos_por_mes[key][1]))
                print("\n")
                
            if opcion == 8:
                print("Saliendo del sistema")
                exit()
    elif usuario=="SYS_admin" and contrasena!="SYS_admin123":
        print("----> Error en contraseña")
        print("\n")

    elif usuario!="SYS_admin" and contrasena=="SYS_admin123":
        print("----> Error en usuario")
        print("\n")

    else:
        print("----> Error en usuario y contraseña")
        print("\n")

    if intentos==3:
        print("Ya intentaste acceder 3 veces, saliendo del sistema")
        print("\n")
        exit()
