#define INT32LEN sizeof(int32_t)

int32_t read_sensor();

long int time_ms = 500; // milisegundos 
long int time_c;  

void setup() {
  Serial.begin(9600);
}

int32_t aux;

void loop() {

  time_c = millis();
  
  aux = read_sensor();
  aux = aux*aux; 
  
  union {
    int32_t val_sensor = aux;
    byte bytes_val[INT32LEN]; 
  } var;

  for ( int i = 0; i < INT32LEN; i++ ){
    Serial.print(var.bytes_val[i], DEC);
    Serial.print(' ');
  }
  Serial.println();

  // Garante periodicidade 
  delay( time_ms - ( millis() - time_c ) );

}

int32_t val = 0; 

int32_t read_sensor(){
  //return (int32_t)random(0, 180 );
  return (int32_t) val < 180 ? val=val+5 : val = 0  ;
}
