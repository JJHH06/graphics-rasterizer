#Ejercicio 5, Librería de cargador de obj
#Jose Hurtarte 19707
#Basado en el programa de clase desarrollado por Ing. Carlos Alonso, ya que se hizo al mismo tiempo que el explicaba

import struct

def _color(r, g, b):
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])

def fixNoneCord(vert):
    if '' in vert:
        for n in range(len(vert)):
            if vert[n] == '':
                vert[n] == '0'
                return vert
    else:
        return vert
   

    
# Clase utilizada para cargar modelos .obj
class Obj(object):

    #filename: El parametro del nombre del archivo a cargar
    def __init__(self, filename):
        
        #Abriendo en modo read
        with open(filename) as file:
            self.lines = file.read().splitlines()
        #listado de vertices, o puntos
        self.vertices = []
        #Listado de coordenadas de textura
        self.texcoords = []
        #Listado de normales
        self.normals = []
        #Listado de las caras
        self.faces = []

        #Ejecuta la función para guardar todos los datos
        self.read()


    def read(self):
        for line in self.lines:

            #verifica que la linea en realidad exista
            if line:
                #Para aislar el primer caracter y el valor
                prefix, value = line.split(' ', 1) #Hace el split solo 1 vez

                # Si la línea es un vertice
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' ')))) #Separa los valores y cada uno lo convierte en float
                #Si es una normal
                elif prefix == 'vn':
                    self.normals.append(list(map(float, value.split(' '))))# Separa y parsea a float y se vuelve una lista
                #Si es una coordenada de textura
                elif prefix == 'vt':
                    self.texcoords.append(list(map(float, value.split(' ')))) #Igual, Separa y parsea a float y se vuelve una lista
                #Si es una cara, face
                elif prefix == 'f':
                    # se separa primero por espacio y después lo separa por / y finamente los convierte a enteros, ya que busca en el listado de vertices
                    self.faces.append( [ list(map(int, fixNoneCord(vertex.split('/')))) for vertex in value.split(' ')] )
                    
class Texture(object):
    def __init__(self, filename):
        self.filename = filename
        self.read()

    def read(self):
        with open(self.filename, "rb") as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            image.seek(14 + 4)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            self.pixels = []

            for x in range(self.width):
                self.pixels.append([])
                for y in range(self.height):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255

                    self.pixels[x].append( _color(r,g,b) )

    def getColor(self, tx, ty):
        if 0<=tx<1 and 0<=ty<1:
            x = round(tx * self.width)
            y = round(ty * self.height)
            return self.pixels[y][x]
        else:
            return _color(0,0,0)