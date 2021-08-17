#Ejercicio 5, graphics library
#Jose Hurtarte 19707
#Graficos por computadora basado en lo escrito por Ing. Carlos Alonso


#Librería de gráficos desarrollada en clase


#struct si se puede usar, es para establecer el tamaño de memoria de los tipos de variables
#los regresa como tipos de variables de C o Java
#from _typeshed import Self
import struct
from numpy import sin, cos, tan
import GenericMath as gm
from obj import Obj
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

def _color(r, g, b):
    # Acepta valores de 0 a 1
    # Se asegura que la información de color se guarda solamente en 3 bytes
    #En un bitmap rgb se guarda al reves
    return bytes([ int(b * 255), int(g* 255), int(r* 255)]) #esto solo tiene 3 bytes y cada uno de los componentes tiene 1 byte

#Constantes de colores
BLACK = _color(0,0,0)
WHITE = _color(1,1,1)

def baryCoords(A, B, C, P):
    # u es para A, v es para B, w es para C
    try:
        #PCB/ABC
        u = (((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        #PCA/ABC
        v = (((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w


class Renderer(object):
    #el primer parametro de cada uno dentro de la clase debe ser si mismo
    def __init__(self, width, height):
        #Constructor
        #Las variables siempre se crean dentro de este
        #Despues solo se llaman con self. el nombre de la variable
        
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glViewMatrix()
        self.glCreateWindow(width, height)
        self.glViewPort(0,0,width,height)
        




    def glLine_NDC(self, v0, v1, color = None):

        x0 = int( (v0.x + 1) * (self.portwidth / 2) + self.vpX)
        x1 = int( (v1.x + 1) * (self.portwidth / 2) + self.vpX)
        y0 = int( (v0.y + 1) * (self.portheight / 2) + self.vpY)
        y1 = int( (v1.y + 1) * (self.portheight / 2) + self.vpY)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glVertex(y, x, color)
            else:
                self.glVertex(x, y, color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1




    
    #El area donde vamos a estar dibujando
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear() #Para que luego de crear la pantalla, ponga negro todos los pixeles

    #Este coloca el color de fondo
    def glClearColor(self, r, g, b):
        self.clear_color = _color(r, g, b)

    # Limpia los pixeles de la pantalla poniendolos en blanco o negro
    def glClear(self):
        #Crea una una estructura par aguardar los pixeles (lista 2D de pixeles) y a cada valor le asigna 3 bytes de color
        #Con una lista por comprension a cada coordenada X y Y se le coloca el clear color
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]
        self.zbuffer = [[ float('inf')for y in range(self.height)]
                          for x in range(self.width)]


    #Se establece el color de dibujo, si no tiene nada se dibuja blanco
    def glColor(self, r, g, b):
        self.curr_color = _color(r,g,b)

    

    # es equivalente al Vertex, ya que dibuja un punto
    def glVertex(self, x, y, color = None):
        #Verifica que este dibujando adentro de la altura y ancho de la imagen (o arreglo de pixeles) y que este dentro del viewport, de lo contrario no se dibujara
        if (0 <= (x + self.xport) < self.width) and (0 <= (y+ self.yport) < self.height) and (0 <= x < self.portwidth) and (0 <= y < self.portheight):
            self.pixels[int(x + self.xport)][int( y + self.yport)] = color or self.curr_color
            

    #utiliza las coordenadas como la esquina inferior izquierda
    def glViewPort(self, x, y, width, height):
        self.xport = x
        self.yport = y
        self.portwidth = width
        self.portheight = height
        self.viewportMatrix = [[width/2, 0, 0, x + width/2],
                                         [0, height/2, 0, y + height/2],
                                         [0, 0, 0.5, 0.5],
                                         [0, 0, 0, 1]]

        self.glProjectionMatrix()

    #Utilización del algoritmo de Bresenham, para creación de lineas
    #recibe vertice final y vertice inicial
    def glLine(self, v0, v1, color = None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        if y0 == y1 and x0 == x1: #Este fue el error que le comenté a carlos en clase y lo resolvió como yo lo había pensado
            self.glVertex(x0,y1,color)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep: #Si esta muy inclinado cambiamos de eje
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1: #Se asegura que dibujemos siempre de izquierda a derecha
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep: 
                self.glVertex(y, x, color)
            else:
                self.glVertex(x, y, color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    #Busca lineas pares o impares
    #Si hay lineas pares devuelve falso e impares verdadero 
    def allowedToPaint(self, horizontal, lineColor):
        count = 0
        lineas = 0
        while count < len(horizontal):
            if horizontal[count] == lineColor:
                lineas += 1
                offset = 0
                for n in horizontal[count:]:
                    if n == lineColor:
                        offset += 1
                    else:
                        break
                count += offset
                    
                
            else:
                count += 1
        return lineas%2

    #ScanLine Algorithm
    #Utiliza una variación que escribí para que pudiera pintar casi cualquier poligono
    def glFillPolygonScanLine(self, x0, xf, y0, yf,lineColor,bottomGrossor = 1, fillColor=_color(1,0,0)):
        
        for y in range((y0+bottomGrossor),yf):
            paintFlag = False
            for x in range((x0),(xf+1)):
                

                if(paintFlag) and (self.pixels[x][y] == lineColor):
                    paintFlag = False

                
                if (self.pixels[x][y] == lineColor) and (self.pixels[x+1][y] != lineColor):

                    
                    #aqui decide si en realidad debe pintar o no
                    
                    paintFlag = self.allowedToPaint([i[y] for i in self.pixels[(x+1):]], lineColor)
                    continue

                #Si se va a pintar
                if(paintFlag):
                    self.pixels[x][y] = fillColor

    
    def glTriangle_standard(self, A, B, C, color = None):

        #Para asegurarnos que estamos trabajando con el orden correcto de los vertices
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        def flatBottomTriangle(v1, v2, v3):

            try:#por la división por 0
                d_21 = (v2.x - v1.x) / (v2.y - v1.y)
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
            except:
                pass
            else:
                x1 = v2.x
                x2 = v3.x
                for y in range(v2.y, v1.y + 1):
                    self.glLine(V2(int(x1),y), V2(int(x2),y), color)
                    x1 += d_21
                    x2 += d_31

        def flatTopTriangle(v1, v2, v3):
            try:
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
                d_32 = (v3.x - v2.x) / (v3.y - v2.y)
            except:
                pass
            else:
                x1 = v3.x
                x2 = v3.x

                for y in range(v3.y, v1.y + 1):
                    self.glLine(V2(int(x1),y), V2(int(x2),y), color)
                    x1 += d_31
                    x2 += d_32

        if B.y == C.y:
            # triangulo con base inferior plana
            flatBottomTriangle(A, B, C)
        elif A.y == B.y:
            # triangulo con base superior plana
            flatTopTriangle(A, B, C)
        else:
            # es irregular y se debe dividir el triangulo en dos
            # dibujar ambos casos
            # Teorema de intercepto
            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x)   , B.y)
            flatBottomTriangle(A, B, D)
            flatTopTriangle(B, D, C)

    def glPoint_NDC(self, x, y, color = None):
        x = int( (x + 1) * (self.portwidth / 2) + self.vpX )
        y = int( (y + 1) * (self.portheight / 2) + self.vpY)


        if x < self.vpX or x >= self.vpX + self.portwidth or y < self.vpY or y >= self.vpY + self.portheight:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color



    def glFinish(self, filename):
        #Crea un archivo BMP y lo llena con la información dentro de self.pixels
        #Escribe el archivo en forma de escritura en bytes
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii'))) #signature
            file.write(bytes('M'.encode('ascii'))) 
            file.write(dword(14 + 40 + (self.width * self.height * 3)))#FileSize, por cada pixel 3 bytes
            file.write(dword(0)) #reservados 4 bytes
            file.write(dword(14 + 40)) #Data offset, es el header + infoheader

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width)) #Width
            file.write(dword(self.height)) #Height
            file.write(word(1)) #Planes
            file.write(word(24)) #Bits per pixel, 3bytes por pixel
            file.write(dword(0))# Compresion, 0 por no compresion
            file.write(dword(self.width * self.height * 3))# Image size, alto por altura por la cantidad de bytes de cada uno
            file.write(dword(0)) #reservados, XpixelsPerM
            file.write(dword(0)) #YpixelsPerM
            file.write(dword(0)) #Colors Used
            file.write(dword(0)) #Important Colors, 0 all

            # Color Table, escribe todos los pixeles dibujados
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

    def glTriangle_bc(self, A, B, C, texCoords = (), texture = None, color = _color(1,1,1), intensity = 1):
        #Bounding Box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A.z * u + B.z * v + C.z * w

                    if texture:
                        tA, tB, tC = texCoords
                        tx = tA[0] * u + tB[0] * v + tC[0] * w
                        ty = tA[1] * u + tB[1] * v + tC[1] * w
                        color = texture.getColor(tx, ty)



                    if 0<=x<self.width and 0<=y<self.height:
                        if z < self.zbuffer[x][y] and z<=1 and z >= -1:

                            self.glVertex(x,y, _color( color[2] * intensity / 255,
                                                      color[1] * intensity / 255,
                                                      color[0] * intensity / 255) )
                            self.zbuffer[x][y] = z



    def glTransform(self, vertex, vMatrix):
        augVertex = V4(vertex[0], vertex[1], vertex[2], 1)
        #transVertex = vMatrix @ augVertex
        transVertex = gm.matMul(vMatrix , [[n] for n in augVertex])
        

        #transVertex = transVertex.tolist()[0]

        transVertex = V3(transVertex[0][0] / transVertex[3][0],
                         transVertex[1][0] / transVertex[3][0],
                         transVertex[2][0] / transVertex[3][0])

        return transVertex

    def glCamTransform( self, vertex ):
        augVertex = [[vertex[0]], [vertex[1]], [vertex[2]], [1]]
        transVertex = gm.matMul(gm.matMul(gm.matMul(self.viewportMatrix, self.projectionMatrix), self.viewMatrix), augVertex)
        #transVertex = transVertex.tolist()[0]

        transVertex = V3(transVertex[0][0] / transVertex[3][0],
                         transVertex[1][0] / transVertex[3][0],
                         transVertex[2][0] / transVertex[3][0])

        return transVertex


    def glCreateRotationMatrix(self, rotate=V3(0,0,0)):
        pitch = gm.deg2rad(rotate.x)
        yaw = gm.deg2rad(rotate.y)
        roll = gm.deg2rad(rotate.z)

        rotationX = [[1,0,0,0],
                               [0,cos(pitch),-sin(pitch),0],
                               [0,sin(pitch),cos(pitch),0],
                               [0,0,0,1]]

        rotationY = [[cos(yaw),0,sin(yaw),0],
                               [0,1,0,0],
                               [-sin(yaw),0,cos(yaw),0],
                               [0,0,0,1]]

        rotationZ = [[cos(roll),-sin(roll),0,0],
                               [sin(roll),cos(roll),0,0],
                               [0,0,1,0],
                               [0,0,0,1]]

        return gm.matMul(gm.matMul(rotationX, rotationY), rotationZ)

        
    def glCreateObjectMatrix(self, translate = V3(0,0,0), scale = V3(1,1,1), rotate = V3(0,0,0)):

        translateMatrix = [[1,0,0,translate.x],
                                     [0,1,0,translate.y],
                                     [0,0,1,translate.z],
                                     [0,0,0,1]]

        scaleMatrix = [[scale.x,0,0,0],
                                 [0,scale.y,0,0],
                                 [0,0,scale.z,0],
                                 [0,0,0,1]]

        rotationMatrix = self.glCreateRotationMatrix(rotate)

        return gm.matMul(gm.matMul(translateMatrix, rotationMatrix), scaleMatrix)

    def glViewMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0)):
        camMatrix = self.glCreateObjectMatrix(translate,V3(1,1,1),rotate)
        
        self.viewMatrix = gm.inv(camMatrix)

    def glLookAt(self, eye, camPosition = V3(0,0,0)):
        forward = gm.subtract(camPosition, eye)
        forward = gm.normVec(forward)

        right = gm.cross(V3(0,1,0), forward)
        right = gm.normVec(right)

        up = gm.cross(forward, right)
        up = gm.normVec(up)

        camMatrix = [[right[0],up[0],forward[0],camPosition.x],
                               [right[1],up[1],forward[1],camPosition.y],
                               [right[2],up[2],forward[2],camPosition.z],
                               [0,0,0,1]]

        self.viewMatrix = gm.inv(camMatrix)



    def glProjectionMatrix(self, n = 0.1, f = 1000, fov = 60 ):
        t = tan(gm.deg2rad(fov) / 2) * n
        r = t * self.portwidth / self.portheight

        self.projectionMatrix = [[n/r, 0, 0, 0],
                                           [0, n/t, 0, 0],
                                           [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
                                           [0, 0, -1, 0]]

    def glLoadModel(self, filename, texture = None, translate = V3(0,0,0), scale = V3(1,1,1),rotate = V3(0,0,0), light = V3(0,0,-1)):

        model = Obj(filename)
        modelMatrix = self.glCreateObjectMatrix(translate,scale,rotate)
        
        #light = light / np.linalg.norm(light)
        light = gm.normVec(light)

        for face in model.faces:
            vertCount = len(face)

            vert0 = model.vertices[face[0][0] - 1]
            vert1 = model.vertices[face[1][0] - 1]
            vert2 = model.vertices[face[2][0] - 1]

            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]


            a = self.glTransform(vert0, modelMatrix)
            b = self.glTransform(vert1, modelMatrix)
            c = self.glTransform(vert2, modelMatrix)

            if vertCount == 4:
                vert3 = model.vertices[face[3][0] - 1]
                vt2 = model.texcoords[face[3][1] - 1]
                d = self.glTransform(vert3, modelMatrix)


            normal = gm.cross(gm.subtract(b,a), gm.subtract(c,a))
            normal = gm.normVec(normal)
            #normal = normal / np.linalg.norm(normal) # la normalizamos
            
            intensity = gm.dot(normal, gm.scalarMul(light,-1))
            #print(normal, light, intensity)

            if intensity > 1:
                intensity = 1
            elif intensity < 0:
                intensity = 0

            a = self.glCamTransform(a)
            b = self.glCamTransform(b)
            c = self.glCamTransform(c)
            if vertCount == 4:
                d = self.glCamTransform(d)



            self.glTriangle_bc(a, b, c, texCoords = (vt0,vt1,vt2), texture = texture, intensity = intensity)
            if vertCount == 4:
                vt3 = model.texcoords[face[3][1] - 1]
                self.glTriangle_bc(a, c, d, texCoords = (vt0,vt2,vt3), texture = texture, intensity = intensity)


