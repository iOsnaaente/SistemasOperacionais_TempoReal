import org.apache.xmlrpc.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class JavaServer { 
    public double sum(double a, double b) {     // exemplo de função p/ comunicação Servidor-Cliente soma dos parametros
        double c = 0;
        
        c = a+b;
        return c;
    }

 public static void main (String [] args) {
  try {
     System.out.println("Attempting to start XML-RPC Server...");
     WebServer server = new WebServer(555);                             // Conecta-se na porta 555
     server.addHandler("sample", new JavaServer());                     // Adiciona um manipulador no servidor 
     server.start();                                                    // Inicia o servidor
     System.out.println("Started successfully.");
     System.out.println("Accepting requests. (Halt program to stop.)");
   } catch (Exception exception) {                                      // Comando em caso de erro de execução 
     System.err.println("JavaServer: " + exception);
   }
  }
 }