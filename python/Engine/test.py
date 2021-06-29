from ax45sEngine.algorithms import axen,axde

key=237415
text='test >< +-*/ crypto'

encrypted=axen(text,key)
print('This encrypt state : "'+axen(text,key)+'"')
print('This decrypt state : "'+axde(encrypted,key)+'"')
