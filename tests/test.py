######################################################
# RoboCop Interface
# Nota: per funzioni pyton non in locale importarle
# in un file locale  
# oppure usare:
#   $ robot --pythonpath . example.robot  


ar = [1, 2, 3, 4, 5, 6, 7]

print (len(ar))

ar.reverse()
print(ar)

if len(ar)>3:
    ar = ar[0:2]

ar.append(66)

print(ar)
