
import time

import serial


device = '/dev/ttyACM0'
baudrate = 115200

import re




def send_cmd(cmd,**kwargs):
  timeout = float(kwargs.get("timeout",0.2))

  with serial.Serial(device, baudrate, timeout=timeout) as ser:
    ser.write(str.encode(cmd)+b"\r\n")
    line = ser.readline().decode()
    ser.close()
    line = line.replace("\r","")
    line = line.replace("\n","")
    return line

def set_threshold_mV(channel,mV):
  threshold = int((2**16-1)*mV/3300.0)
  print("setting threshold {:d}".format(threshold))
  return set_threshold(channel,threshold)

def set_threshold(channel,threshold):
  answer = send_cmd("thr{:02d}={:d}".format(channel,threshold))

  pattern =  re.compile("set channel ([0-9E+\-.]+) threshold ([0-9E+\-.]+)")
  match = re.search(pattern, answer)
  if match:
    rec_channel = int(match.groups()[0])
    rec_threshold = int(match.groups()[1])
    #print(rec_channel)
    #print(rec_threshold)
    if ( ( rec_channel == channel) and (rec_threshold == threshold) ):
      print("success")
    else:
      raise NameError("error, serial communication went wrong")

                  
                  
#  # here is the Arduino sketch, running on a pro micro 3.3v (lily pad)
# 
# #include <SPI.h>
# #include <SoftSPI.h>
# //https://github.com/MajenkoLibraries/SoftSPI - downoad zip and include
#  
#  
# 
# String getValue(String data, char separator, int index)
# {
#     int found = 0;
#     int strIndex[] = { 0, -1 };
#     int maxIndex = data.length() - 1;
# 
#     for (int i = 0; i <= maxIndex && found <= index; i++) {
#         if (data.charAt(i) == separator || i == maxIndex) {
#             found++;
#             strIndex[0] = strIndex[1] + 1;
#             strIndex[1] = (i == maxIndex) ? i+1 : i;
#         }
#     }
#     return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
# }
# 
# 
#  
# // Create a new SPI port with:
# // Pin 2 = MOSI,
# // Pin 3 = MISO,
# // Pin 4 = SCK
# 
# 
# // Pin 5 = CS
# SoftSPI mySPI(2, 3, 4);
# 
# void CS_low(){
#   digitalWrite(5,LOW);
# }
# 
# void CS_high(){
#   digitalWrite(5,HIGH);
# }
#  
# void setup() {
#   pinMode(5, OUTPUT); // CS pin
#   pinMode(2, OUTPUT);
#   mySPI.begin();
#   Serial.begin(115200);
#   Serial.setTimeout(5);
#   }
# 
# void thresh(uint8_t chan, int16_t thr){
#   CS_low();
#   // 8 bit register 0 -> PWM
#   mySPI.transfer(0x00);
#   // 4 bit command, 4 bit subregister (pwm channel)
#   mySPI.transfer(0x80 | (0x0F & chan));
#   // data upper byte
#   mySPI.transfer(thr>>8);
#   // data lower byte
#   mySPI.transfer(thr&0xFF);
#   CS_high();
# 
# }
#  
# void loop() {
#   static uint8_t v = 0;
#  
#   // expect command of following type:
#   // thr04=32000
#   
#   if(Serial.available()) {
# 
#     String a= Serial.readString();// read the incoming data as string
#     //Serial.println(a);
# 
#     String variable = getValue(a,'=',0);
#     String value    = getValue(a,'=',1);
#     //Serial.println("variable");
#     //Serial.println(variable);
#     //Serial.println("value");
#     //Serial.println(value);
#     
#     if( (variable.substring(0,3) == "thr") || (variable.substring(0,3) == "THR")){
#       //Serial.println("setting threshold");
#       if ( value != " ") {
#         int channel = variable.substring(3,5).toInt();
#         int threshold = value.toInt();
#         Serial.print("set channel ");
#         Serial.print(channel);
#         Serial.print(" threshold ");
#         Serial.println(value);
#         thresh(channel,threshold);
#       }
#     }
# 
# 
#   }
# }