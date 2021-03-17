#include <Servo.h>

#define BUFFER_LEN 32
#define pinServo 3

Servo servo1;

String inputString = "";
boolean stringComplete = false;

void atuador(float ang);

void setup() {

  servo1.attach( pinServo );
  Serial.begin( 9600 );
  
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH); 
  
  inputString.reserve( BUFFER_LEN );

}

void loop() {

  if ( stringComplete ) {
    union {
      byte bytes[4] = { inputString[0], inputString[1], inputString[2], inputString[3] };
      int32_t VALUE;
    } f;

    inputString = "";
    stringComplete = false;

    atuador( f.VALUE );
  }
}

void atuador(int32_t ang) {
  //byte angle = map( ang, 0, 100, 0, 179 );
  digitalWrite(13, HIGH);
  servo1.write( (int)ang );
  Serial.println(ang);
  digitalWrite(13, LOW); 
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
