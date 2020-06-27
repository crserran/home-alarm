#include "esphome.h"
#include <SPI.h>
#include <MFRC522.h>
#define RST_PIN         22        // Configurable, see typical pin layout above
#define SS_1_PIN        21        // Configurable, take a unused pin, only HIGH/LOW required
#define LED_PIN         12        // Configurable
MFRC522 mfrc522;   // Create MFRC522 instance.
unsigned long tempo2 = 0;


class RFIDRC522Sensor : public Component, public CustomMQTTDevice {
  public:
    TextSensor *rfid = new TextSensor();
    TextSensor *rfidlast = new TextSensor();
    std:: string idnumberstd = "";
    std:: string last_cardstd= "";

    void setup() override {
      SPI.begin();        // Init SPI bus
      mfrc522.PCD_Init(SS_1_PIN, RST_PIN); // Init each MFRC522 card
      pinMode(LED_PIN, OUTPUT);
      subscribe("esphome/safe_mode", &RFIDRC522Sensor::on_message);
    }   

    void loop() override {
      // Look for new cards
      if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
        MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
        dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size, mfrc522.PICC_GetTypeName(piccType)); //llama a la funcion que trabaja con nuestra tarjeta
        // Halt PICC
        mfrc522.PICC_HaltA();
        // Stop encryption on PCD
        mfrc522.PCD_StopCrypto1();
      }

      if (millis() > tempo2 && tempo2 != 0){  
        //Borramos tarjeta y publicamos (vacio)
        idnumberstd.clear();
        rfid->publish_state(idnumberstd);
        tempo2 = 0;
      } 
    }

    void on_message(const std::string &payload) {
      if (payload == "ON") {
        digitalWrite(LED_PIN, HIGH);
      } else {
        digitalWrite(LED_PIN, LOW);
      }
    }

    void dump_byte_array(byte *ID, byte IDSize, String picc) {
      //le damos formato al numero de de la tarjeta leido
      String idnumber = "";
      for(byte i=0; i < IDSize; i++) {
        if(ID[i] < 0x10) {             //Añadimos el 0 de la izquierda en cada byte (si lo tuviera).
          idnumber += "0";
        }
        idnumber += String (ID[i], HEX);
      }
      idnumberstd = idnumber.c_str(); //pasamos a variable standard para que funcione en ESPHome y podamos mandarla
      
      //creamos los datos de la ultima tarjeta leida
      String last_card = (" ID card: "  + idnumber +  " PICC type: " + picc);
      last_cardstd = last_card.c_str(); //pasamos a variable standard para que funcione en ESPHome y podamos mandarla
      
      //Publicamos la tarjeta leida
      rfid->publish_state(idnumberstd);
      rfidlast->publish_state(last_cardstd);
    
      //Activamos temporizador de borrado
      tempo2 = millis() + 1000;
    }
};