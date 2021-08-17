#Modulo de funciones matemáticas 
#Ejercicio 4
#José Javier Hurtarte 19707

PI = 3.141592654
#recibe un iterable de tamaño n y devuelve una lista
def normVec(vec0):
    magnitude = 0
    for n in vec0:
        magnitude += n*n
    magnitude = magnitude**0.5
    return [i/magnitude for i in vec0]

#recibe un iterable y un numero escalar a multiplicar por cada uno de los componentes
def scalarMul(vec, scalar):
    return[n*scalar for n in vec]
    
#recibe 2 iterables de tamaño n y devuelve una lista de sus elementos restados
def subtract(vec0, vec1):
    resultado = [vec0[n] - vec1[n] for n in range(min(len(vec0), len(vec1)))] #Para asegurarnos que no haya un error de longitudes
    return resultado

#Solo funciona con 2 iterables de tamaño 3 cada uno para sacar el producto cruz, 
def cross(vec0, vec1):
    return [vec0[1]*vec1[2] - vec0[2]*vec1[1],
        vec0[2]*vec1[0] - vec0[0]*vec1[2],
        vec0[0]*vec1[1] - vec0[1]*vec1[0]]

#Producto escalar entre 2 iterables, devuelve un numero escalar
def dot(vec0, vec1):
    result = 0
    #Para asegurarnos que no se pase de largo
    for n in range(min(len(vec0), len(vec1))): #por si se meten 2 listas de tamaños distintos
        result += vec0[n]*vec1[n]
    return result


def matMul(A, B):
    if len(A[0]) != len(B):
        return None #Es imposible hacer la multiplicacion
    mResult = [[0]*len(B[0]) for _ in range(len(A))] #Creacion de una matriz vacia
    
    #Multiplicacion es la sumatoria de la multiplicacion de los elementos de la fila de A por la columna de B
    for m in range(len(A)):
        for n in range(len(B[0])):
            for x in range(len(B)):
                mResult[m][n] += A[m][x] * B[x][n] 
            
    return mResult


def deg2rad(degrees):
    return degrees*(PI/180)

def det3x3(matA):
    total=(matA[0][0]*matA[1][1]*matA[2][2])+(matA[0][1]*matA[1][2]*matA[2][0])+(matA[0][2]*matA[1][0]*matA[2][1]) - (matA[0][1]*matA[1][0]*matA[2][2]) - (matA[0][0]*matA[1][2]*matA[2][1])- (matA[0][2]*matA[1][1]*matA[2][0])
    return total

def det4x4(matA):
    result =[]
    for n in matA:
        result.append(n + n[:3])
    
    determinant = 0
    countSum = 0
    for x in range(len(matA[0])):
        determinant += result[0][0+countSum]*result[1][1+countSum]*result[2][2+countSum]*result[3][3+countSum]
        countSum +=1
    countSum -= 1
    
    for x in range(len(matA[0])):
        determinant += -1*(result[0][0+countSum]*result[1][countSum-1]*result[2][countSum-2]*result[3][countSum-3])
        countSum +=1
    return determinant
    
         
    


def T(A):
    result=[[0]*len(A[0]) for _ in range(len(A))]
    for i in range(len(A)):# iterate through columns
        for j in range(len(A[0])):
            result[j][i] = A[i][j]
    return result
    
    
def inv(A):
    det = det4x4(A)
    A = T(A)
    result=[[0]*len(A[0]) for _ in range(len(A))]
    mult = 1
    for m in range(len(A)):
        for n in range(len(A[0])):
            tempMat = [[A[y][x] for x in range(len(A[0])) if x != n] for y in range(len(A)) if y != m]
            print(tempMat)
            result[m][n] = mult*det3x3(tempMat)/det
            mult *= -1
        mult *= -1
        
    return result
            
print(inv([[6,-7,-8,1],[2,3,5,4],[1,6,9,0],[4,-5,2,1]]))