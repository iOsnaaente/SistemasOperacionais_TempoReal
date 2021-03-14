#define INT32LEN sizeof(int32_t)

int32_t read_sensor();

long int time_ms = 500; // milisegundos 
long int time_c;  

void setup() {
  Serial.begin(9600);
}

void loop() {

  time_c = millis();

  union {
    int32_t val_sensor = read_sensor();
    byte bytes_val[INT32LEN]; 
  } var;

  for ( int i = 0; i < INT32LEN; i++ ){
    Serial.print(var.bytes_val[i], HEX);
    Serial.print(' ');
  }
  Serial.println();

  // Garante periodicidade 
  delay( time_ms - ( millis() - time_c ) );

}

int32_t read_sensor(){
  return (int32_t)random(0, 0xfffffff );
}
