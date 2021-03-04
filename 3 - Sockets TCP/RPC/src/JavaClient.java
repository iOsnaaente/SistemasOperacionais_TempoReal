// https://www.tutorialspoint.com/xml-rpc/xml_rpc_examples.htm  // Tutorial util 

import java.util.*;
import org.apache.xmlrpc.*;

public class JavaClient {

 public static void main (String [] args) {
  
  try {
    
     XmlRpcClient server = new XmlRpcClient("http://25.94.218.230:555");   // Comando p/ indicar a porta da conexão  exemplo p/ testes: localhost:555 propria maquina porta 555, no caso deveremos usar o hamachi p/ efetuar a conexão
     Vector params = new Vector();                                         // Vetor contendo os parametros p/ enviar ao servidor
     params.addElement( new java.lang.Double(5) );                         // Comando para adicionar elementos no vetor 
     params.addElement( new java.lang.Double(20) );

     Object result = server.execute("sample.sum", params);                 // Comando p/ enviar os parametros p/servidor
     
     double sum = ( (java.lang.Double) result).doubleValue();              // Comando p/ receber respostao do servidor
     System.out.println("Soma dos Parametros: "+ sum);

   } catch ( Exception exception) {                                        // Comando em caso de erro de execução 
     System.err.println("JavaClient: " + exception);
   }
  }
}