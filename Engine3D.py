#Ejercicio 5, programa principal
#Transformations
#Jose Hurtarte 19707



from gl import Renderer, V2,V3, _color
from obj import Texture

width = 1080
height = 540

rend = Renderer(width, height) #Equivalente al glinit
# ya se llamo al constructor y se tiene al renderer creado

rend.glClearColor(0, 0, 0) # establece el fondo verde oscuro en vez del default negro
rend.glClear()# Lo escribe
#rend.glColor(1,1,1)

cameraPosition = V3(0, -30, -10)
modelPosition = V3(0, 0, -10)


#Low Angle
rend.glLookAt(modelPosition, V3(0,0,6))
rend.glLoadModel("banana.obj", texture=Texture("banana.bmp") ,translate = modelPosition,scale = V3(0.15,0.15,0.15),rotate =V3(-30,0,0))
rend.glFinish("LowAngle.bmp")


#HighAngle
rend.glClear()
rend.glLookAt(modelPosition, V3(0,30,5))
rend.glLoadModel("banana.obj", texture=Texture("banana.bmp") ,translate = modelPosition,scale = V3(0.15,0.15,0.15),rotate =V3(-10,0,0),light = V3(0,-0.5,-1))
rend.glFinish("HighAngle.bmp")


#Medium angle
rend.glClear()
rend.glLookAt( V3(0, 5.2, 0), V3(0,5,8))
rend.glLoadModel("banana.obj", texture=Texture("banana.bmp") ,translate = modelPosition,scale = V3(0.15,0.15,0.15),rotate =V3(-10,0,0),light = V3(0,-0.5,-1))
rend.glFinish("Medium.bmp")


#DutchAngle
rend.glClear()
rend.glLookAt( modelPosition, V3(0,0,7))
rend.glLoadModel("banana.obj", texture=Texture("banana.bmp") ,translate = modelPosition,scale = V3(0.15,0.15,0.15),rotate =V3(0,0,60),light = V3(0,-0.5,-1))
rend.glFinish("DutchAngle.bmp")




