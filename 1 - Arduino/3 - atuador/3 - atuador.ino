#include <Servo.h>

#define BUFFER_LEN 32
#define pinServo 8

Servo servo1;

String inputString = "";
boolean stringComplete = false;
void atuador(float ang);

void setup() {

  servo1.attach( pinServo );
  Serial.begin( 9600 );
  inputString.reserve( BUFFER_LEN );

}

void loop() {

  if ( stringComplete ){
    union{
      byte bytes[4] = { inputString[0], inputString[1], inputString[2], inputString[3] };
      float VALUE;
    } f;

    inputString = "";
    stringComplete = false;

    atuador( f.VALUE );
  }

}

void atuador(float ang){
  byte angle = map(ang, 0, 100, 0, 179);
  servo1.write( angle );
}


void serialEvent(){
  while(Serial.available()){
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n'){
      stringComplete = true;    
    }
  } 
}
