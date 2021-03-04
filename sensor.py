from Serial_SR import Serial_SR

comport = Serial_SR('COM5')

for i in range(10):
    
    lines = comport.serial_receive() 
    
    for line in  lines:
        print(line.decode())

