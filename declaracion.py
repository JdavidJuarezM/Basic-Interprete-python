import re

# Abrir archivo de texto
file = open('Example.atom', 'r')

# Crear el diccionario de palabras reservadas
palRes = {'ent': 'entero', 'cad': 'cadena', 'vf': 'booleano'}
palRes_key = palRes.keys()
palResil = {'impri' : 'imprimir', 'lee' : 'leer'}
palResil_key = palResil.keys()

# Crear listas
ident = []
lista = []

count = 0
s = 0
d = 0

#separar programa en líneas 
program = file.readlines()
for line in program:
    count += 1
    tokens = line.split()
    
    if len(tokens) == 0:
        continue  # Ignorar líneas vacías
    
    # Verificar si el primer token es una palabra reservada o un identificador
    if tokens[0] in palRes_key or tokens[0] in [item[0] for item in ident] or tokens[0] in palResil_key:
        #Parte donde se revisan las declaraciones 
        if tokens[0] in palRes_key:
            if len(tokens) < 2: 
                print(f"\nError en línea {count}: Dato no válido\n")
            else:
                identificador = tokens[1]      
                if tokens[1] in palRes_key:
                    print(f"\nError en línea {count}: '{tokens[1]}' es una palabra reservada\n")
                elif re.match('^[a-z]', tokens[1]):
                    if any(identificador == item[0] for item in ident):
                        print(f"\nError en línea {count}: El identificador '{tokens[1]}' ya está definido\n")
                    else:
                        tipo = palRes[tokens[0]]
                        if tokens[0] == "ent":
                            if len(tokens) > 2:
                                print(f"\nError en línea {count}: Solo se puede declarar un identificador por línea\n")
                            else:
                                tipo = palRes[tokens[0]]
                                ident.append([identificador, "ent"])
                                lista.extend([identificador, tipo, 0, "id"+str(d)])
                                d = int(d)
                                d = d+1
                        if tokens[0] == "cad":
                            if len(tokens) > 2:
                                print(f"\nError en línea {count}: Solo se puede declarar un identificador por línea\n")
                            else:
                                ident.append([identificador, "cad"])
                                lista.extend([identificador, tipo, "", "id"+str(d)])
                                d = int(d)
                                d = d+1
                        if tokens[0] == "vf":
                            if len(tokens) > 2:
                                print(f"\nError en línea {count}: Solo se puede declarar un identificador por línea\n")
                            else:
                                ident.append([identificador, "vf"])
                                lista.extend([identificador, tipo, False, "id"+str(d)])
                                d = int(d)
                                d = d+1
                else:
                    print(f"\nError en línea {count}: El identificador debe comenzar con una letra minúscula\n")
        #Parte donde se revisa el leer e imprimir
        # El diccionario variables contiene todas las variables del programa
            variables = {}
        
        elif tokens[0] in palResil_key: 
                v = line.split(maxsplit=1)  
                p1 = v[1].strip() #Para despejar los identificadores de los parentesis
                patron = p1.strip("()")  # Para despejar los identificadores de los parentesis
                if tokens[0] == 'impri':
                    if re.match('^[(]["][a-zA-Z0-9 ]*["][)]$', v[1]):
                        # Impri se usa con string literal
                        print(patron)
                    elif re.match('^[(][a-zA-Z0-9]*[)]$', v[1]):
                        if patron in variables:
                            # Impri se usa con el nombre de una variable
                            print(variables[patron])
                        else :
                            print(f"\nError en línea {count}: {patron} no definido\n")
                    else:
                        print(f"\nError en línea {count}: instrucción inválida\n")
                        
                        
                        
                if tokens[0] == 'lee':
                    if re.match('^[(][a-zA-Z0-9]*[)]$', v[1]):
                        if patron in [item[0] for item in ident]:
                            z=1
                        else:
                            print(f"\nError en línea {count}: {patron} no definido\n")
                    else:
                        print(f"\nError en línea {count}: instrucción inválida\n")
                        

















                        
        #Parte de asignacion a los identificadores 
        else:
            if len(tokens) < 3:
                print(f"\nError en línea {count}: Asignación no válida\n")
            elif tokens[1] != "=":
                print(f"\nError en línea {count}: Carácter '{tokens[1]}' no válido\n")
            else:
                identificador = tokens[0]
                if any(identificador == item[0] for item in ident):
                    tipo = next(item[1] for item in ident if item[0] == identificador)
                    valor = tokens[2]
                    
                    if tipo == "ent":
                        if re.match('^[0-9]*$', valor): #Valora que solo se introduzcan números
                            if int(valor) < 2147483647 and int(valor) > -2147483648: #Rango de int 
                                num = lista.index(identificador)
                                lista[num + 2] = int(valor)
                            else:
                                print(f"\nError en línea {count}: valor fuera de rango\n")
                        else:
                            print(f"\nError en línea {count}: Valor no válido para ent\n")
                    elif tipo == "cad":
                        if re.match('^["][a-zA-Z]*["]$', valor): #Valora cadenas con comillas
                            num = lista.index(identificador)
                            lista[num + 2] = tokens[2]
                        else:
                            print(f"\nError en línea {count}: Valor no válido para cad\n")
                    elif tipo == "vf": #Valora verdadero o falso
                        if valor == "Verdadero":
                            num = lista.index(identificador)
                            lista[num + 2] = True
                        elif valor == "Falso":
                            num = lista.index(identificador)
                            lista[num + 2] = False
                        else:
                            print(f"\nError en línea {count}: Valor no válido para vf\n")
                else:
                    print(f"\nError en línea {count}: Identificador '{tokens[0]}' no definido\n")
                    
    else:
        print(f"\nError en línea {count}: '{tokens[0]}' no definido\n")

if len(lista) > 0:
    l = len(lista)
    l = l // 4
    o = int(l)
    for i in range(o):
        print(lista[s:s+4])
        s = s + 4

file.close()  # Cerrar archivo