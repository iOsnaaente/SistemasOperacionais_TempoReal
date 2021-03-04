#define BUFFER_LEN 32

String inputString = "";
boolean stringComplete = false;

float manipulate( float receivedData );

void setup() {
  Serial.begin(9600);
  inputString.reserve(BUFFER_LEN);
}

float data;

void loop() {
  
  if (stringComplete){

    union{
      byte bytes[4] = {inputString[0], inputString[1], inputString[2], inputString[3]};  
      float VALUE;
    } f;

    inputString = "";
    stringComplete = false;

    data = manipulate(f.VALUE);

    union{
      float sendData = data;
      byte sDATA[4];
    }s;

    for (int i=0; i<4; i++){
      Serial.print(s.sDATA[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
  }
}

float manipulate(float receivedData){
  return sqrt(receivedData);
};

void serialEvent(){
  while(Serial.available()){
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n'){
      stringComplete = true;    
    }
  } 
}
