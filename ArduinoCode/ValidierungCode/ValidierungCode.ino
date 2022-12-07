/*
 * This code measures an analog signal with a given sampling frequency
 * To increase resolution, it uses the SparkFun Qwiic 12 Bit ADC and its library. 
 * This helps to change the range to 0-2.048V 
 * and increase the resolution from 10 bit to 11 bit.
 */


 
#include <SparkFun_ADS1015_Arduino_Library.h> //Bibliothek unter folgendem Link verfügbar:  http://librarymanager/All#SparkFun_ADS1015
#include <Wire.h>

ADS1015 adcSensor;

#define sf 1000 // Abtastfrequenz sf ändern
#define tc (1000/(sf))     // Zeitkonstante
unsigned int ADC_Value = 0;    // aktueller ADC Wert
unsigned long last_time = 0;

void setup() {
  Wire.begin();
  Serial.begin(500000);
  if (adcSensor.begin() == true)
  {
    Serial.println("I2C Verbindung gefunden!.");
  }
  else
  {
    Serial.println("Gerät nicht gefunden");
    while (1);
  }
}


// Diese Schleife läuft solange durch bis Sie den Arduino vom Strom trennen
void loop() {
  ADC_Value = adcSensor.getSingleEnded(0);
  if (millis() - last_time >= tc) {
    last_time = millis();
    
    
    Serial.print(ADC_Value);
    Serial.print(";");
    Serial.print(millis());
    Serial.println();
    }
}
