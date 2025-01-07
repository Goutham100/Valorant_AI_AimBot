#include <Mouse.h>
using namespace std;

void setup() {
  Serial.begin(115200);  // Match baud rate with Python
  Mouse.begin();
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); // Read until newline
    int commaIndex = data.indexOf(',');        // Find the comma
    if (commaIndex != -1) {
      int dx = data.substring(0, commaIndex).toInt();       // Extract dx
      int dy = data.substring(commaIndex + 1).toInt();      // Extract dy

      Mouse.move(dx, dy);
    }
  }
}
