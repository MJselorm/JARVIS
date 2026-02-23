#include <WiFi.h>

// Replace with your Wi-Fi credentials
const char* ssid = "MJ";
const char* password = "PASSWORD";

// LED pin
const int ledPin = 2;
const int rpin=32;
const int gpin=33;
const int bpin=25;
// Create Wi-Fi server on port 80
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(rpin, OUTPUT);
  pinMode(gpin, OUTPUT);
  pinMode(bpin, OUTPUT);

  //setting all leds off
  digitalWrite(ledPin, LOW);
  digitalWrite(rpin, LOW);
  digitalWrite(gpin, LOW);
  digitalWrite(bpin, LOW);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available(); // Check if a client connected
  if (client) {
    Serial.println("New Client.");
    String currentLine = "";
    String request = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        request += c;
        if (c == '\n') { // End of HTTP request line
          if (request.indexOf("GET /ON") >= 0) {
            digitalWrite(ledPin, HIGH);
          }
          if (request.indexOf("GET /RED") >= 0) {
            digitalWrite(rpin, HIGH);
            digitalWrite(gpin, LOW);
            digitalWrite(bpin, LOW);
            
          }
          if (request.indexOf("GET /GREEN") >= 0) {
            digitalWrite(gpin, HIGH);
            digitalWrite(rpin, LOW);
            digitalWrite(bpin, LOW);
          }
          if (request.indexOf("GET /BLUE") >= 0) {
            digitalWrite(bpin, HIGH);
            digitalWrite(rpin, LOW);
            digitalWrite(gpin, LOW);
          }
          if (request.indexOf("GET /WHITE") >= 0) {
            analogWrite(rpin,255); 
            analogWrite(gpin,255); 
            analogWrite(bpin,255); 
          }
           if (request.indexOf("GET /YELLOW") >= 0) {
            analogWrite(rpin,255); 
            analogWrite(gpin,255); 
            analogWrite(bpin,0); 
          }
          if (request.indexOf("GET /OFF") >= 0) {
            digitalWrite(ledPin, LOW);
            digitalWrite(rPin, LOW);
            digitalWrite(bPin, LOW);
            digitalWrite(gpinin, LOW);
            
          }

          // Send HTML response
          client.println("HTTP/1.1 200 OK");
          client.println("Content-type:text/html");
          client.println();
          client.println("<!DOCTYPE html>");
          client.println("<html>");
          client.println("<h1>ESP32 LED Control</h1>");
          client.println("<button onclick=\"window.location.href='/ON'\">LED ON</button>");
          client.println("<button onclick=\"window.location.href='/OFF'\">LED OFF</button>");
          client.println("</html>");
          client.println();
          break;
        }
      }
    }
    delay(1);
    client.stop();
    Serial.println("Client Disconnected.");
  }
}
