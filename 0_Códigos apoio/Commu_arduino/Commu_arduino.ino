/*  TRABALHO DE REDES INDUSTRIAIS 
 *
 *   Autor: Bruno Gabriel Flores Sampaio
 *   Data : 26/06/2020
 *
 *   Descriço: 
       Usando um Arduino NANO, farei o  sensoriamento
       de objetos dentro de uma area limitada em 180º
       fazendo o uso de um  HC-SR04, um sensor ultra-
       Sonico. 
       O Arduino  estara conectado ao Serial  e um script
       em python fara a leitura dos dados da porta e uti-
       lizando  transmissoes via sockets UDP, fara o con-
       trole remoto ou local do sistema.
 *
 *   Primeira atualizaçao.  
 *
 */


// TAMANHO DO BUFFER EM BYTES 
#define BUFFER_LEN 32

#define ANGULO    '11'
#define DISTANCIA '22'


String inputString = "";
boolean stringComplete = false;

// INICIO DO CODIGO
void setup() {

  // PARA INICIAR O SERIAL 
  Serial.begin(9600);
  
  // SERPARA n BYTES PARA O INPUT
  inputString.reserve(BUFFER_LEN);

}

int FUNC;
float VALOR;

void loop(){


    if (stringComplete) {
      
      union{
        byte  bytes[2] = {inputString[0], inputString[1]};
        int   FUNC;
      } n;      
      
      union{
        byte  bytes[4] = {inputString[2], inputString[3],inputString[4],inputString[5]};
        float VALUE;
      } f;


      inputString = "";
      stringComplete = false;  
    
      if (n.FUNC == ANGULO )        VALOR = f.VALUE;    
      else if(n.FUNC == DISTANCIA)  VALOR = (float)random(100, 150);
      else                          VALOR = 0.0;
      
      union{
        float fVALUE = VALOR;
        byte pVALUE[4];
      } p;
      
      for (int i = 0; i<4; i++){
        Serial.print(p.pVALUE[i], HEX);
        Serial.print(" ");
      }
      Serial.println();
    }
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

