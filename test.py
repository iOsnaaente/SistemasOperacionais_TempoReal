

df_sensor = [0,1,2,3,4,5,6]
df_atuador = [0,1,2,3,4,5,6,7]




for t_sensor, t_atuador in zip( df_sensor['Time'], df_atuador['Time']):
    print( t_atuador - t_sensor ) 

    print( 'valor 1 %2.2f  valor 2 %2.2f ' %( valor1, valor2)  )