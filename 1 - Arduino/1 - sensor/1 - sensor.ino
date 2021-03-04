#define BUFFER_LEN 32

float read_sensor();

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.write( read_sensor() );
  delay(500);
}

float read_sensor(){
  return random(0,100);
}
