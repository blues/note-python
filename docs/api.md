# Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`namespace `[`notecard::binary_helpers`](#namespacenotecard_1_1binary__helpers) | 
`namespace `[`notecard::card`](#namespacenotecard_1_1card) | 
`namespace `[`notecard::cobs`](#namespacenotecard_1_1cobs) | 
`namespace `[`notecard::crc32`](#namespacenotecard_1_1crc32) | 
`namespace `[`notecard::env`](#namespacenotecard_1_1env) | 
`namespace `[`notecard::file`](#namespacenotecard_1_1file) | 
`namespace `[`notecard::gpio`](#namespacenotecard_1_1gpio) | 
`namespace `[`notecard::hub`](#namespacenotecard_1_1hub) | 
`namespace `[`notecard::md5`](#namespacenotecard_1_1md5) | 
`namespace `[`notecard::note`](#namespacenotecard_1_1note) | 
`namespace `[`notecard::notecard`](#namespacenotecard_1_1notecard) | 
`namespace `[`notecard::timeout`](#namespacenotecard_1_1timeout) | 
`namespace `[`notecard::transaction_manager`](#namespacenotecard_1_1transaction__manager) | 
`namespace `[`notecard::validators`](#namespacenotecard_1_1validators) | 

# namespace `notecard::binary_helpers` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`private def `[`_md5_hash`](#namespacenotecard_1_1binary__helpers_1a7cbdb1c94d6448e186df0f37f26b4125)`(data)`            | Create an MD5 digest of the given data.
`public def `[`binary_store_decoded_length`](#namespacenotecard_1_1binary__helpers_1af168917cad28bfabb154817552f95535)`(`[`Notecard`](#classnotecard_1_1notecard_1_1_notecard)` card)`            | Get the length of the decoded binary data store.
`public def `[`binary_store_reset`](#namespacenotecard_1_1binary__helpers_1aa35216fb089167c5b7401330f3d4db38)`(`[`Notecard`](#classnotecard_1_1notecard_1_1_notecard)` card)`            | Reset the binary data store.
`public def `[`binary_store_transmit`](#namespacenotecard_1_1binary__helpers_1a6150afaf45a91b405ae1b9bfb6f12b77)`(`[`Notecard`](#classnotecard_1_1notecard_1_1_notecard)` card,bytearray data,int offset)`            | Write bytes to index `offset` of the binary data store.
`public def `[`binary_store_receive`](#namespacenotecard_1_1binary__helpers_1ab8c54de7f3990a0e60307ba8f9327477)`(card,int offset,int length)`            | Receive length bytes from index `offset` of the binary data store.

## Members

#### `private def `[`_md5_hash`](#namespacenotecard_1_1binary__helpers_1a7cbdb1c94d6448e186df0f37f26b4125)`(data)` 

Create an MD5 digest of the given data.

#### `public def `[`binary_store_decoded_length`](#namespacenotecard_1_1binary__helpers_1af168917cad28bfabb154817552f95535)`(`[`Notecard`](#classnotecard_1_1notecard_1_1_notecard)` card)` 

Get the length of the decoded binary data store.

#### `public def `[`binary_store_reset`](#namespacenotecard_1_1binary__helpers_1aa35216fb089167c5b7401330f3d4db38)`(`[`Notecard`](#classnotecard_1_1notecard_1_1_notecard)` card)` 

Reset the binary data store.

#### `public def `[`binary_store_transmit`](#namespacenotecard_1_1binary__helpers_1a6150afaf45a91b405ae1b9bfb6f12b77)`(`[`Notecard`](#classnotecard_1_1notecard_1_1_notecard)` card,bytearray data,int offset)` 

Write bytes to index `offset` of the binary data store.

#### `public def `[`binary_store_receive`](#namespacenotecard_1_1binary__helpers_1ab8c54de7f3990a0e60307ba8f9327477)`(card,int offset,int length)` 

Receive length bytes from index `offset` of the binary data store.

# namespace `notecard::card` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`attn`](#namespacenotecard_1_1card_1ad11e82dd52c3c9f5ae3f1de5f7f5a9b9)`(card,mode,files,seconds,payload,start)`            | Configure interrupt detection between a host and Notecard.
`public def `[`time`](#namespacenotecard_1_1card_1a0de0f6e72a2387d09aaaa4a719383313)`(card)`            | Retrieve the current time and date from the Notecard.
`public def `[`status`](#namespacenotecard_1_1card_1a13f03abe1576ab81ea8190e3074576ce)`(card)`            | Retrieve the status of the Notecard.
`public def `[`temp`](#namespacenotecard_1_1card_1aa15a26b60d8f8be7f994338f0af563cf)`(card,minutes)`            | Retrieve the current temperature from the Notecard.
`public def `[`version`](#namespacenotecard_1_1card_1ac0a7ef1176b55152d42de04d39dfac54)`(card)`            | Retrieve firmware version information from the Notecard.
`public def `[`voltage`](#namespacenotecard_1_1card_1a1f9f65c34f1bd959d7902285a7537ce6)`(card,hours,offset,vmax,vmin)`            | Retrieve current and historical voltage info from the Notecard.
`public def `[`wireless`](#namespacenotecard_1_1card_1a10f5f4667d80f47674d1876df69b8e22)`(card,mode,apn)`            | Retrieve wireless modem info or customize modem behavior.
`public def `[`transport`](#namespacenotecard_1_1card_1a0d157a8f39c045891fb6f644cfc52118)`(card,method,allow)`            | Configure the Notecard's connectivity method.

## Members

#### `public def `[`attn`](#namespacenotecard_1_1card_1ad11e82dd52c3c9f5ae3f1de5f7f5a9b9)`(card,mode,files,seconds,payload,start)` 

Configure interrupt detection between a host and Notecard.

#### Parameters
* `card` The current Notecard object. 

* `mode` The attn mode to set. 

* `files` A collection of notefiles to watch. 

* `seconds` A timeout to use when arming attn mode. 

* `payload` When using sleep mode, a payload of data from the host that the Notecard should hold in memory until retrieved by the host. 

* `start` When using sleep mode and the host has reawakened, request the Notecard to return the stored payload.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`time`](#namespacenotecard_1_1card_1a0de0f6e72a2387d09aaaa4a719383313)`(card)` 

Retrieve the current time and date from the Notecard.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`status`](#namespacenotecard_1_1card_1a13f03abe1576ab81ea8190e3074576ce)`(card)` 

Retrieve the status of the Notecard.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`temp`](#namespacenotecard_1_1card_1aa15a26b60d8f8be7f994338f0af563cf)`(card,minutes)` 

Retrieve the current temperature from the Notecard.

#### Parameters
* `card` The current Notecard object. 

* `minutes` If specified, creates a templated _temp.qo file that gathers Notecard temperature value at the specified interval.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`version`](#namespacenotecard_1_1card_1ac0a7ef1176b55152d42de04d39dfac54)`(card)` 

Retrieve firmware version information from the Notecard.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`voltage`](#namespacenotecard_1_1card_1a1f9f65c34f1bd959d7902285a7537ce6)`(card,hours,offset,vmax,vmin)` 

Retrieve current and historical voltage info from the Notecard.

#### Parameters
* `card` The current Notecard object. 

* `hours` Number of hours to analyze. 

* `offset` Number of hours to offset. 

* `vmax` max voltage level to report. 

* `vmin` min voltage level to report.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`wireless`](#namespacenotecard_1_1card_1a10f5f4667d80f47674d1876df69b8e22)`(card,mode,apn)` 

Retrieve wireless modem info or customize modem behavior.

#### Parameters
* `card` The current Notecard object. 

* `mode` The wireless module mode to set. Must be one of: "-" to reset to the default mode "auto" to perform automatic band scan mode (default) "m" to restrict the modem to Cat-M1 "nb" to restrict the modem to Cat-NB1 "gprs" to restrict the modem to EGPRS 

* `apn` Access Point Name (APN) when using an external SIM. Use "-" to reset to the Notecard default APN.

#### Returns

#### Returns
dict The result of the Notecard request containing network status and signal information.

#### `public def `[`transport`](#namespacenotecard_1_1card_1a0d157a8f39c045891fb6f644cfc52118)`(card,method,allow)` 

Configure the Notecard's connectivity method.

#### Parameters
* `card` The current Notecard object. 

* `method` The connectivity method to enable. Must be one of: "-" to reset to device default "wifi-cell" to prioritize WiFi with cellular fallback "wifi" to enable WiFi only "cell" to enable cellular only "ntn" to enable Non-Terrestrial Network mode "wifi-ntn" to prioritize WiFi with NTN fallback "cell-ntn" to prioritize cellular with NTN fallback "wifi-cell-ntn" to prioritize WiFi, then cellular, then NTN 

* `allow` When True, allows adding Notes to non-compact Notefiles while connected over a non-terrestrial network.

#### Returns

#### Returns
dict The result of the Notecard request.

# namespace `notecard::cobs` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public bytearray `[`cobs_encode`](#namespacenotecard_1_1cobs_1a21f5995d4351903d8eee0283f5fea1c4)`(bytearray data,int eop)`            | Functions for COBS encoding and decoding of bytearrays.
`public bytearray `[`cobs_decode`](#namespacenotecard_1_1cobs_1a3d69441998d7c88c3412775db981a57b)`(bytes encoded,int eop)`            | COBS decode an array of bytes, using eop as the end of packet marker.

## Members

#### `public bytearray `[`cobs_encode`](#namespacenotecard_1_1cobs_1a21f5995d4351903d8eee0283f5fea1c4)`(bytearray data,int eop)` 

Functions for COBS encoding and decoding of bytearrays.

This module implements Consistent Overhead Byte Stuffing (COBS), an encoding that eliminates zero bytes from arbitrary binary data. The Notecard uses this for binary data transfers to ensure reliable transmission.

COBS encode an array of bytes, using eop as the end of packet marker.

#### `public bytearray `[`cobs_decode`](#namespacenotecard_1_1cobs_1a3d69441998d7c88c3412775db981a57b)`(bytes encoded,int eop)` 

COBS decode an array of bytes, using eop as the end of packet marker.

# namespace `notecard::crc32` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`private def `[`_logical_rshift`](#namespacenotecard_1_1crc32_1a899a3e0bc54c6f8f72f9156c0cf0d520)`(val,shift_amount,num_bits)`            | Logcally right shift `val` by `shift_amount` bits.
`public def `[`crc32`](#namespacenotecard_1_1crc32_1aa0bac9c104b88fbeba89290339ef2c82)`(data)`            | Compute CRC32 of the given data.

## Members

#### `private def `[`_logical_rshift`](#namespacenotecard_1_1crc32_1a899a3e0bc54c6f8f72f9156c0cf0d520)`(val,shift_amount,num_bits)` 

Logcally right shift `val` by `shift_amount` bits.

Logical right shift (i.e. right shift that fills with 0s instead of the sign bit) isn't supported natively in Python. This is a simple implementation. See: [https://realpython.com/python-bitwise-operators/#arithmetic-vs-logical-shift](https://realpython.com/python-bitwise-operators/#arithmetic-vs-logical-shift)

#### `public def `[`crc32`](#namespacenotecard_1_1crc32_1aa0bac9c104b88fbeba89290339ef2c82)`(data)` 

Compute CRC32 of the given data.

Small lookup-table half-byte CRC32 algorithm based on: [https://create.stephan-brumme.com/crc32/#half-byte](https://create.stephan-brumme.com/crc32/#half-byte)

# namespace `notecard::env` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`default`](#namespacenotecard_1_1env_1a6ff91175ae591e8a3a87c2a4ef9c5a13)`(card,name,text)`            | Perform an [env.default](#namespacenotecard_1_1env_1a6ff91175ae591e8a3a87c2a4ef9c5a13) request against a Notecard.
`public def `[`get`](#namespacenotecard_1_1env_1a28ed0423d0aff1d109371427139e0a73)`(card,name)`            | Perform an [env.get](#namespacenotecard_1_1env_1a28ed0423d0aff1d109371427139e0a73) request against a Notecard.
`public def `[`modified`](#namespacenotecard_1_1env_1aa672554b72786c9ec1e5f76b3e11eb34)`(card)`            | Perform an [env.modified](#namespacenotecard_1_1env_1aa672554b72786c9ec1e5f76b3e11eb34) request against a Notecard.
`public def `[`set`](#namespacenotecard_1_1env_1a848e61d00dc69d8d143b4a5a92c41e45)`(card,name,text)`            | Perform an [env.set](#namespacenotecard_1_1env_1a848e61d00dc69d8d143b4a5a92c41e45) request against a Notecard.

## Members

#### `public def `[`default`](#namespacenotecard_1_1env_1a6ff91175ae591e8a3a87c2a4ef9c5a13)`(card,name,text)` 

Perform an [env.default](#namespacenotecard_1_1env_1a6ff91175ae591e8a3a87c2a4ef9c5a13) request against a Notecard.

#### Parameters
* `card` The current Notecard object. 

* `name` The name of an environment var to set a default for. 

* `text` The default value. Omit to delete the default.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`get`](#namespacenotecard_1_1env_1a28ed0423d0aff1d109371427139e0a73)`(card,name)` 

Perform an [env.get](#namespacenotecard_1_1env_1a28ed0423d0aff1d109371427139e0a73) request against a Notecard.

#### Parameters
* `card` The current Notecard object. 

* `name` The name of an environment variable to get.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`modified`](#namespacenotecard_1_1env_1aa672554b72786c9ec1e5f76b3e11eb34)`(card)` 

Perform an [env.modified](#namespacenotecard_1_1env_1aa672554b72786c9ec1e5f76b3e11eb34) request against a Notecard.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`set`](#namespacenotecard_1_1env_1a848e61d00dc69d8d143b4a5a92c41e45)`(card,name,text)` 

Perform an [env.set](#namespacenotecard_1_1env_1a848e61d00dc69d8d143b4a5a92c41e45) request against a Notecard.

#### Parameters
* `card` The current Notecard object. 

* `name` The name of an environment variable to set. 

* `text` The variable value. Omit to delete.

#### Returns

#### Returns
string The result of the Notecard request.

# namespace `notecard::file` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`changes`](#namespacenotecard_1_1file_1a16a6d9bd035cf4f3d0273948701e299c)`(card,tracker,files)`            | Perform individual or batch queries on Notefiles.
`public def `[`delete`](#namespacenotecard_1_1file_1a06c97850aed80627ce2202dd7878c313)`(card,files)`            | Delete individual notefiles and their contents.
`public def `[`stats`](#namespacenotecard_1_1file_1afd6ecece175a8ba9052b07889cf757f4)`(card)`            | Obtain statistics about local notefiles.
`public def `[`pendingChanges`](#namespacenotecard_1_1file_1aac52d0739fcba481f9a0bd4cfd35362e)`(card)`            | Retrieve information about pending Notehub changes.

## Members

#### `public def `[`changes`](#namespacenotecard_1_1file_1a16a6d9bd035cf4f3d0273948701e299c)`(card,tracker,files)` 

Perform individual or batch queries on Notefiles.

#### Parameters
* `card` The current Notecard object. 

* `tracker` A developer-defined tracker ID. 

* `files` A list of Notefiles to retrieve changes for.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`delete`](#namespacenotecard_1_1file_1a06c97850aed80627ce2202dd7878c313)`(card,files)` 

Delete individual notefiles and their contents.

#### Parameters
* `card` The current Notecard object. 

* `files` A list of Notefiles to delete.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`stats`](#namespacenotecard_1_1file_1afd6ecece175a8ba9052b07889cf757f4)`(card)` 

Obtain statistics about local notefiles.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`pendingChanges`](#namespacenotecard_1_1file_1aac52d0739fcba481f9a0bd4cfd35362e)`(card)` 

Retrieve information about pending Notehub changes.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

# namespace `notecard::gpio` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`notecard::gpio::GPIO`](#classnotecard_1_1gpio_1_1_g_p_i_o) | [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) abstraction.
`class `[`notecard::gpio::CircuitPythonGPIO`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o) | [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) for CircuitPython.
`class `[`notecard::gpio::MicroPythonGPIO`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o) | [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) for MicroPython.
`class `[`notecard::gpio::RpiGPIO`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o) | [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) for Raspbian (Raspberry Pi).

# class `notecard::gpio::GPIO` 

[GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) abstraction.

Supports [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) on CircuitPython, MicroPython, and Raspbian (Raspberry Pi).

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`direction`](#classnotecard_1_1gpio_1_1_g_p_i_o_1a196b0aadec928a05fa0696094bf1f228)`(self,direction)` | Set the direction of the pin.
`public def `[`pull`](#classnotecard_1_1gpio_1_1_g_p_i_o_1aa1ed7db0c71818cc363998971b76abff)`(self,pull)` | Set the pull of the pin.
`public def `[`value`](#classnotecard_1_1gpio_1_1_g_p_i_o_1a7045bfe38df0ed3f44cc9aab4b2be87e)`(self,value)` | Set the output or get the current level of the pin.
`public def `[`__init__`](#classnotecard_1_1gpio_1_1_g_p_i_o_1aa706502ba47ce3ef0b3fda83efaed56c)`(self,pin,`[`direction`](#classnotecard_1_1gpio_1_1_g_p_i_o_1a196b0aadec928a05fa0696094bf1f228)`,`[`pull`](#classnotecard_1_1gpio_1_1_g_p_i_o_1aa1ed7db0c71818cc363998971b76abff)`,`[`value`](#classnotecard_1_1gpio_1_1_g_p_i_o_1a7045bfe38df0ed3f44cc9aab4b2be87e)`)` | Initialize the [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o).

## Members

#### `public def `[`direction`](#classnotecard_1_1gpio_1_1_g_p_i_o_1a196b0aadec928a05fa0696094bf1f228)`(self,direction)` 

Set the direction of the pin.

Does nothing in this base class. Should be implemented by subclasses.

#### `public def `[`pull`](#classnotecard_1_1gpio_1_1_g_p_i_o_1aa1ed7db0c71818cc363998971b76abff)`(self,pull)` 

Set the pull of the pin.

Does nothing in this base class. Should be implemented by subclasses.

#### `public def `[`value`](#classnotecard_1_1gpio_1_1_g_p_i_o_1a7045bfe38df0ed3f44cc9aab4b2be87e)`(self,value)` 

Set the output or get the current level of the pin.

Does nothing in this base class. Should be implemented by subclasses.

#### `public def `[`__init__`](#classnotecard_1_1gpio_1_1_g_p_i_o_1aa706502ba47ce3ef0b3fda83efaed56c)`(self,pin,`[`direction`](#classnotecard_1_1gpio_1_1_g_p_i_o_1a196b0aadec928a05fa0696094bf1f228)`,`[`pull`](#classnotecard_1_1gpio_1_1_g_p_i_o_1aa1ed7db0c71818cc363998971b76abff)`,`[`value`](#classnotecard_1_1gpio_1_1_g_p_i_o_1a7045bfe38df0ed3f44cc9aab4b2be87e)`)` 

Initialize the [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o).

Pin and direction are required arguments. Pull and value will be set
   only if given.

# class `notecard::gpio::CircuitPythonGPIO` 

```
class notecard::gpio::CircuitPythonGPIO
  : public notecard.gpio.GPIO
```  

[GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) for CircuitPython.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`pin`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1aee8b724c5d7c9f62cee37dcd78a2dc30) | 
`public def `[`direction`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1ad69863c129beedf8cd4282bc0d386d1a)`(self,direction)` | Set the direction of the pin.
`public def `[`pull`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1a15d2ccb9629fe780aeb7d192bf0bd6e0)`(self,pull)` | Set the pull of the pin.
`public def `[`value`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1a83159467a8e8a7c1bba551a7b02d2723)`(self,value)` | Set the output or get the current level of the pin.
`public def `[`__init__`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1aeeab02f708086e616d49a8f092d4ec2c)`(self,`[`pin`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1aee8b724c5d7c9f62cee37dcd78a2dc30)`,`[`direction`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1ad69863c129beedf8cd4282bc0d386d1a)`,`[`pull`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1a15d2ccb9629fe780aeb7d192bf0bd6e0)`,`[`value`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1a83159467a8e8a7c1bba551a7b02d2723)`)` | Initialize the [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o).

## Members

#### `public  `[`pin`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1aee8b724c5d7c9f62cee37dcd78a2dc30) 

#### `public def `[`direction`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1ad69863c129beedf8cd4282bc0d386d1a)`(self,direction)` 

Set the direction of the pin.

Allowed direction values are GPIO.IN and GPIO.OUT. Other values cause a
   ValueError.

#### `public def `[`pull`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1a15d2ccb9629fe780aeb7d192bf0bd6e0)`(self,pull)` 

Set the pull of the pin.

Allowed pull values are GPIO.PULL_UP, GPIO.PULL_DOWN, and
   GPIO.PULL_NONE. Other values cause a ValueError.

#### `public def `[`value`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1a83159467a8e8a7c1bba551a7b02d2723)`(self,value)` 

Set the output or get the current level of the pin.

If value is not given, returns the level of the pin (i.e. the pin is an
   input). If value is given, sets the level of the pin (i.e. the pin is an
   output).

#### `public def `[`__init__`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1aeeab02f708086e616d49a8f092d4ec2c)`(self,`[`pin`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1aee8b724c5d7c9f62cee37dcd78a2dc30)`,`[`direction`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1ad69863c129beedf8cd4282bc0d386d1a)`,`[`pull`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1a15d2ccb9629fe780aeb7d192bf0bd6e0)`,`[`value`](#classnotecard_1_1gpio_1_1_circuit_python_g_p_i_o_1a83159467a8e8a7c1bba551a7b02d2723)`)` 

Initialize the [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o).

Pin and direction are required arguments. Pull and value will be set
   only if given.

# class `notecard::gpio::MicroPythonGPIO` 

```
class notecard::gpio::MicroPythonGPIO
  : public notecard.gpio.GPIO
```  

[GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) for MicroPython.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`pin`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a572ca355f15813af55515ccfdf0f0710) | 
`public def `[`direction`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a7ae27116656ff6263e41cddc9056c7a5)`(self,direction)` | Set the direction of the pin.
`public def `[`pull`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1ade062dcf3e7b236305485563f56bfb2e)`(self,pull)` | Set the pull of the pin.
`public def `[`value`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a0f67725b3adbc6ea3ca651ee294b8e69)`(self,value)` | Set the output or get the current level of the pin.
`public def `[`__init__`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a9e9b28185d99a1c6e80786ac4770b1a6)`(self,`[`pin`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a572ca355f15813af55515ccfdf0f0710)`,`[`direction`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a7ae27116656ff6263e41cddc9056c7a5)`,`[`pull`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1ade062dcf3e7b236305485563f56bfb2e)`,`[`value`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a0f67725b3adbc6ea3ca651ee294b8e69)`)` | Initialize the [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o).

## Members

#### `public  `[`pin`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a572ca355f15813af55515ccfdf0f0710) 

#### `public def `[`direction`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a7ae27116656ff6263e41cddc9056c7a5)`(self,direction)` 

Set the direction of the pin.

Allowed direction values are GPIO.IN and GPIO.OUT. Other values cause a
   ValueError.

#### `public def `[`pull`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1ade062dcf3e7b236305485563f56bfb2e)`(self,pull)` 

Set the pull of the pin.

Allowed pull values are GPIO.PULL_UP, GPIO.PULL_DOWN, and
   GPIO.PULL_NONE. Other values cause a ValueError.

#### `public def `[`value`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a0f67725b3adbc6ea3ca651ee294b8e69)`(self,value)` 

Set the output or get the current level of the pin.

If value is not given, returns the level of the pin (i.e. the pin is an
   input). If value is given, sets the level of the pin (i.e. the pin is an
   output).

#### `public def `[`__init__`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a9e9b28185d99a1c6e80786ac4770b1a6)`(self,`[`pin`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a572ca355f15813af55515ccfdf0f0710)`,`[`direction`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a7ae27116656ff6263e41cddc9056c7a5)`,`[`pull`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1ade062dcf3e7b236305485563f56bfb2e)`,`[`value`](#classnotecard_1_1gpio_1_1_micro_python_g_p_i_o_1a0f67725b3adbc6ea3ca651ee294b8e69)`)` 

Initialize the [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o).

Pin and direction are required arguments. Pull and value will be set
   only if given.

# class `notecard::gpio::RpiGPIO` 

```
class notecard::gpio::RpiGPIO
  : public notecard.gpio.GPIO
```  

[GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o) for Raspbian (Raspberry Pi).

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`rpi_direction`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1aaeab2d015fcb0e8a70eba5f1cc63d81b) | 
`public  `[`pin`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1abe65b0ddc7db50805a26b2114a36a9d5) | 
`public def `[`direction`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1afa4f710df0c3fc5f16f8e62885247718)`(self,direction)` | Set the direction of the pin.
`public def `[`pull`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1a4add5ea414b45c6f0e46122ebd5e5b3a)`(self,pull)` | Set the pull of the pin.
`public def `[`value`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1aa32e799d69be26456250691de9bea60c)`(self,value)` | Set the output or get the current level of the pin.
`public def `[`__init__`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1a3dc01f9d7af7461fbc2e18d2931bfdb2)`(self,`[`pin`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1abe65b0ddc7db50805a26b2114a36a9d5)`,`[`direction`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1afa4f710df0c3fc5f16f8e62885247718)`,`[`pull`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1a4add5ea414b45c6f0e46122ebd5e5b3a)`,`[`value`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1aa32e799d69be26456250691de9bea60c)`)` | Initialize the [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o).

## Members

#### `public  `[`rpi_direction`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1aaeab2d015fcb0e8a70eba5f1cc63d81b) 

#### `public  `[`pin`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1abe65b0ddc7db50805a26b2114a36a9d5) 

#### `public def `[`direction`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1afa4f710df0c3fc5f16f8e62885247718)`(self,direction)` 

Set the direction of the pin.

Allowed direction values are GPIO.IN and GPIO.OUT. Other values cause a
   ValueError.

#### `public def `[`pull`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1a4add5ea414b45c6f0e46122ebd5e5b3a)`(self,pull)` 

Set the pull of the pin.

Allowed pull values are GPIO.PULL_UP, GPIO.PULL_DOWN, and
   GPIO.PULL_NONE. Other values cause a ValueError.

#### `public def `[`value`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1aa32e799d69be26456250691de9bea60c)`(self,value)` 

Set the output or get the current level of the pin.

If value is not given, returns the level of the pin (i.e. the pin is an
   input). If value is given, sets the level of the pin (i.e. the pin is an
   output).

#### `public def `[`__init__`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1a3dc01f9d7af7461fbc2e18d2931bfdb2)`(self,`[`pin`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1abe65b0ddc7db50805a26b2114a36a9d5)`,`[`direction`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1afa4f710df0c3fc5f16f8e62885247718)`,`[`pull`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1a4add5ea414b45c6f0e46122ebd5e5b3a)`,`[`value`](#classnotecard_1_1gpio_1_1_rpi_g_p_i_o_1aa32e799d69be26456250691de9bea60c)`)` 

Initialize the [GPIO](#classnotecard_1_1gpio_1_1_g_p_i_o).

Pin and direction are required arguments. Pull and value will be set
   only if given.

# namespace `notecard::hub` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`set`](#namespacenotecard_1_1hub_1af7eeda1f4ad38f303a24844ad651f6ab)`(card,product,sn,mode,outbound,inbound,duration,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`,align,voutbound,vinbound,host)`            | Configure Notehub behavior on the Notecard.
`public def `[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`(card)`            | Initiate a sync of the Notecard to Notehub.
`public def `[`syncStatus`](#namespacenotecard_1_1hub_1adeec5dd54d3ce966f7e08bee81105d2b)`(card,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`)`            | Retrieve the status of a sync request.
`public def `[`status`](#namespacenotecard_1_1hub_1a5c44efc254a08e2f8eb6d6b2d3d9ab82)`(card)`            | Retrieve the status of the Notecard's connection.
`public def `[`log`](#namespacenotecard_1_1hub_1aa78d6e2e3028e6022b3b9405527937b2)`(card,text,alert,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`)`            | Send a log request to the Notecard.
`public def `[`get`](#namespacenotecard_1_1hub_1a5c2687d0e446715d54c1dd7b4ac4c682)`(card)`            | Retrieve the current Notehub configuration parameters.

## Members

#### `public def `[`set`](#namespacenotecard_1_1hub_1af7eeda1f4ad38f303a24844ad651f6ab)`(card,product,sn,mode,outbound,inbound,duration,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`,align,voutbound,vinbound,host)` 

Configure Notehub behavior on the Notecard.

#### Parameters
* `card` The current Notecard object. 

* `product` The ProductUID of the project. 

* `sn` The Serial Number of the device. 

* `mode` The sync mode to use. 

* `outbound` Max time to wait to sync outgoing data. 

* `inbound` Max time to wait to sync incoming data. 

* `duration` If in continuous mode, the amount of time, in minutes, of each session. 

* `sync` If in continuous mode, whether to automatically sync each time a change is detected on the device or Notehub. 

* `align` To align syncs to a regular time-interval, as opposed to using max time values. 

* `voutbound` Overrides "outbound" with a voltage-variable value. 

* `vinbound` Overrides "inbound" with a voltage-variable value. 

* `host` URL of an alternative or private Notehub instance.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`(card)` 

Initiate a sync of the Notecard to Notehub.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`syncStatus`](#namespacenotecard_1_1hub_1adeec5dd54d3ce966f7e08bee81105d2b)`(card,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`)` 

Retrieve the status of a sync request.

#### Parameters
* `card` The current Notecard object. 

* `sync` True if sync should be auto-initiated pending outbound data.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`status`](#namespacenotecard_1_1hub_1a5c44efc254a08e2f8eb6d6b2d3d9ab82)`(card)` 

Retrieve the status of the Notecard's connection.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`log`](#namespacenotecard_1_1hub_1aa78d6e2e3028e6022b3b9405527937b2)`(card,text,alert,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`)` 

Send a log request to the Notecard.

#### Parameters
* `card` The current Notecard object. 

* `text` The ProductUID of the project. 

* `alert` True if the message is urgent. 

* `sync` Whether to sync right away.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`get`](#namespacenotecard_1_1hub_1a5c2687d0e446715d54c1dd7b4ac4c682)`(card)` 

Retrieve the current Notehub configuration parameters.

#### Parameters
* `card` The current Notecard object.

#### Returns

#### Returns
string The result of the Notecard request.

# namespace `notecard::md5` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`left_rotate`](#namespacenotecard_1_1md5_1ad47995927682f5ef4b0faf7c7fe0afa1)`(x,amount)`            | 
`public def `[`md5`](#namespacenotecard_1_1md5_1a2068feeb80dcc31372ed28124a4fb9e0)`(message)`            | 
`public def `[`digest`](#namespacenotecard_1_1md5_1ab5fc780c84e630ba029b74babecf2472)`(message)`            | 

## Members

#### `public def `[`left_rotate`](#namespacenotecard_1_1md5_1ad47995927682f5ef4b0faf7c7fe0afa1)`(x,amount)` 

#### `public def `[`md5`](#namespacenotecard_1_1md5_1a2068feeb80dcc31372ed28124a4fb9e0)`(message)` 

#### `public def `[`digest`](#namespacenotecard_1_1md5_1ab5fc780c84e630ba029b74babecf2472)`(message)` 

# namespace `notecard::note` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`add`](#namespacenotecard_1_1note_1a163ab38179a215238b0877f203236d5d)`(card,file,body,payload,sync,port)`            | Add a Note to a Notefile.
`public def `[`changes`](#namespacenotecard_1_1note_1a660dda3f8fa6f9afff52e0a3be6bef84)`(card,file,tracker,maximum,start,stop,deleted,`[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`)`            | Incrementally retrieve changes within a Notefile.
`public def `[`get`](#namespacenotecard_1_1note_1ad7a4c296382c14a8efb54278c127d73b)`(card,file,note_id,`[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`,deleted)`            | Retrieve a note from an inbound or DB Notefile.
`public def `[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`(card,file,note_id)`            | Delete a DB note in a Notefile by its ID.
`public def `[`update`](#namespacenotecard_1_1note_1a149f30ef24735181e7d55477a50bd9d5)`(card,file,note_id,body,payload)`            | Update a note in a DB Notefile by ID.
`public def `[`template`](#namespacenotecard_1_1note_1a5133667dc0a68e837437dd19c242f8ee)`(card,file,body,length,port,compact)`            | Create a template for new Notes in a Notefile.

## Members

#### `public def `[`add`](#namespacenotecard_1_1note_1a163ab38179a215238b0877f203236d5d)`(card,file,body,payload,sync,port)` 

Add a Note to a Notefile.

#### Parameters
* `card` The current Notecard object. 

* `file` The name of the file. body (JSON object): A developer-defined tracker ID. 

* `payload` An optional base64-encoded string. 

* `sync` Perform an immediate sync after adding. 

* `port` If provided, a unique number to represent a notefile. Required for Notecard LoRa.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`changes`](#namespacenotecard_1_1note_1a660dda3f8fa6f9afff52e0a3be6bef84)`(card,file,tracker,maximum,start,stop,deleted,`[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`)` 

Incrementally retrieve changes within a Notefile.

#### Parameters
* `card` The current Notecard object. 

* `file` The name of the file. 

* `tracker` A developer-defined tracker ID. 

* `maximum` Maximum number of notes to return. 

* `start` Should tracker be reset to the beginning before a get. 

* `stop` Should tracker be deleted after get. 

* `deleted` Should deleted notes be returned. 

* `delete` Should notes in a response be auto-deleted.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`get`](#namespacenotecard_1_1note_1ad7a4c296382c14a8efb54278c127d73b)`(card,file,note_id,`[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`,deleted)` 

Retrieve a note from an inbound or DB Notefile.

#### Parameters
* `card` The current Notecard object. 

* `file` The inbound or DB notefile to retrieve a Notefile from. 

* `note_id` (DB files only) The ID of the note to retrieve. 

* `delete` Whether to delete the note after retrieval. 

* `deleted` Whether to allow retrieval of a deleted note.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`(card,file,note_id)` 

Delete a DB note in a Notefile by its ID.

#### Parameters
* `card` The current Notecard object. 

* `file` The file name of the DB notefile. 

* `note_id` The id of the note to delete.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`update`](#namespacenotecard_1_1note_1a149f30ef24735181e7d55477a50bd9d5)`(card,file,note_id,body,payload)` 

Update a note in a DB Notefile by ID.

#### Parameters
* `card` The current Notecard object. 

* `file` The file name of the DB notefile. 

* `note_id` The id of the note to update. 

* `body` The JSON object to add to the note. 

* `payload` The base64-encoded JSON payload to add to the note.

#### Returns

#### Returns
string The result of the Notecard request.

#### `public def `[`template`](#namespacenotecard_1_1note_1a5133667dc0a68e837437dd19c242f8ee)`(card,file,body,length,port,compact)` 

Create a template for new Notes in a Notefile.

#### Parameters
* `card` The current Notecard object. 

* `file` The file name of the notefile. 

* `body` A sample JSON body that specifies field names and values as "hints" for the data type. 

* `length` If provided, the maximum length of a payload that can be sent in Notes for the template Notefile. 

* `port` If provided, a unique number to represent a notefile. Required for Notecard LoRa. 

* `compact` If true, sets the format to compact to tell the Notecard to omit this additional metadata to save on storage and bandwidth. Required for Notecard LoRa.

#### Returns

#### Returns
string The result of the Notecard request.

# namespace `notecard::notecard` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`notecard::notecard::SerialLockTimeout`](#classnotecard_1_1notecard_1_1_serial_lock_timeout) | A null [SerialLockTimeout](#classnotecard_1_1notecard_1_1_serial_lock_timeout) for when use_serial_lock is False.
`class `[`notecard::notecard::NoOpContextManager`](#classnotecard_1_1notecard_1_1_no_op_context_manager) | A no-op context manager for use with [NoOpSerialLock](#classnotecard_1_1notecard_1_1_no_op_serial_lock).
`class `[`notecard::notecard::NoOpSerialLock`](#classnotecard_1_1notecard_1_1_no_op_serial_lock) | A no-op serial lock class for when use_serial_lock is False.
`class `[`notecard::notecard::Notecard`](#classnotecard_1_1notecard_1_1_notecard) | Base [Notecard](#classnotecard_1_1notecard_1_1_notecard) class.
`class `[`notecard::notecard::OpenSerial`](#classnotecard_1_1notecard_1_1_open_serial) | [Notecard](#classnotecard_1_1notecard_1_1_notecard) class for Serial communication.
`class `[`notecard::notecard::OpenI2C`](#classnotecard_1_1notecard_1_1_open_i2_c) | [Notecard](#classnotecard_1_1notecard_1_1_notecard) class for I2C communication.

# class `notecard::notecard::SerialLockTimeout` 

```
class notecard::notecard::SerialLockTimeout
  : public Exception
```  

A null [SerialLockTimeout](#classnotecard_1_1notecard_1_1_serial_lock_timeout) for when use_serial_lock is False.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------

## Members

# class `notecard::notecard::NoOpContextManager` 

A no-op context manager for use with [NoOpSerialLock](#classnotecard_1_1notecard_1_1_no_op_serial_lock).

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__enter__`](#classnotecard_1_1notecard_1_1_no_op_context_manager_1a45e5f5d525d68876cc5a5a669874992c)`(self)` | No-op enter function.
`public def `[`__exit__`](#classnotecard_1_1notecard_1_1_no_op_context_manager_1aa4fc0701f38d457e4b0f96077fc4b46e)`(self,exc_type,exc_value,traceback)` | No-op exit function.

## Members

#### `public def `[`__enter__`](#classnotecard_1_1notecard_1_1_no_op_context_manager_1a45e5f5d525d68876cc5a5a669874992c)`(self)` 

No-op enter function.

Required for context managers.

#### `public def `[`__exit__`](#classnotecard_1_1notecard_1_1_no_op_context_manager_1aa4fc0701f38d457e4b0f96077fc4b46e)`(self,exc_type,exc_value,traceback)` 

No-op exit function.

Required for context managers.

# class `notecard::notecard::NoOpSerialLock` 

A no-op serial lock class for when use_serial_lock is False.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`acquire`](#classnotecard_1_1notecard_1_1_no_op_serial_lock_1ad6a7e9bf7f23ef117c9f87e4a306c3fe)`(* args,** kwargs)` | Acquire the no-op lock.
`public def `[`release`](#classnotecard_1_1notecard_1_1_no_op_serial_lock_1adc256ea3ce065b51c99aae23de4b7774)`(* args,** kwargs)` | Release the no-op lock.

## Members

#### `public def `[`acquire`](#classnotecard_1_1notecard_1_1_no_op_serial_lock_1ad6a7e9bf7f23ef117c9f87e4a306c3fe)`(* args,** kwargs)` 

Acquire the no-op lock.

#### `public def `[`release`](#classnotecard_1_1notecard_1_1_no_op_serial_lock_1adc256ea3ce065b51c99aae23de4b7774)`(* args,** kwargs)` 

Release the no-op lock.

# class `notecard::notecard::Notecard` 

Base [Notecard](#classnotecard_1_1notecard_1_1_notecard) class.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classnotecard_1_1notecard_1_1_notecard_1a442972f12bcd38ad54b77238db2b514b)`(self,debug)` | Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) object.
`public def `[`Transaction`](#classnotecard_1_1notecard_1_1_notecard_1ad1f10d0d420850ecc665f134d16dea46)`(self,req,lock)` | Send a request to the [Notecard](#classnotecard_1_1notecard_1_1_notecard) and read back a response.
`public def `[`Command`](#classnotecard_1_1notecard_1_1_notecard_1aed43fa69581140729fbe56f26884cfd8)`(self,req)` | Send a command to the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`GetUserAgent`](#classnotecard_1_1notecard_1_1_notecard_1a3873873f525447a9414f8d45faa7556b)`(self)` | Return the User Agent String for the host for debug purposes.
`public def `[`SetAppUserAgent`](#classnotecard_1_1notecard_1_1_notecard_1a7e5a045afc15d8112afce726d15ea218)`(self,app_user_agent)` | Set the User Agent info for the app.
`public def `[`UserAgentSent`](#classnotecard_1_1notecard_1_1_notecard_1aa4248c7b4293e9e38f8e67aa955183ae)`(self)` | Return true if the User Agent has been sent to the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`SetTransactionPins`](#classnotecard_1_1notecard_1_1_notecard_1a9eae8c9c039d3ac501e4ba6fcc8257e4)`(self,rtx_pin,ctx_pin)` | Set the pins used for RTX and CTX.

## Members

#### `public def `[`__init__`](#classnotecard_1_1notecard_1_1_notecard_1a442972f12bcd38ad54b77238db2b514b)`(self,debug)` 

Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) object.

#### `public def `[`Transaction`](#classnotecard_1_1notecard_1_1_notecard_1ad1f10d0d420850ecc665f134d16dea46)`(self,req,lock)` 

Send a request to the [Notecard](#classnotecard_1_1notecard_1_1_notecard) and read back a response.

If the request is a command (indicated by using 'cmd' in the request
   instead of 'req'), don't return a response.

   The underlying transport channel (serial or I2C) is locked for the
   duration of the request and response if `lock` is True.

#### `public def `[`Command`](#classnotecard_1_1notecard_1_1_notecard_1aed43fa69581140729fbe56f26884cfd8)`(self,req)` 

Send a command to the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

Unlike `Transaction`, `Command` doesn't return a response from the
   Notecard.

#### `public def `[`GetUserAgent`](#classnotecard_1_1notecard_1_1_notecard_1a3873873f525447a9414f8d45faa7556b)`(self)` 

Return the User Agent String for the host for debug purposes.

#### Returns

#### Returns
dict A dictionary containing user agent information including OS details and any application-specific user agent information.

#### `public def `[`SetAppUserAgent`](#classnotecard_1_1notecard_1_1_notecard_1a7e5a045afc15d8112afce726d15ea218)`(self,app_user_agent)` 

Set the User Agent info for the app.

#### Parameters
* `app_user_agent` Dictionary containing application-specific user agent information.

#### `public def `[`UserAgentSent`](#classnotecard_1_1notecard_1_1_notecard_1aa4248c7b4293e9e38f8e67aa955183ae)`(self)` 

Return true if the User Agent has been sent to the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### Returns

#### Returns
bool True if the User Agent has been sent to the [Notecard](#classnotecard_1_1notecard_1_1_notecard), False otherwise.

#### `public def `[`SetTransactionPins`](#classnotecard_1_1notecard_1_1_notecard_1a9eae8c9c039d3ac501e4ba6fcc8257e4)`(self,rtx_pin,ctx_pin)` 

Set the pins used for RTX and CTX.

#### Parameters
* `rtx_pin` The pin to use for Ready To Transact (RTX) signaling. 

* `ctx_pin` The pin to use for Clear To Transact (CTX) signaling.

# class `notecard::notecard::OpenSerial` 

```
class notecard::notecard::OpenSerial
  : public notecard.notecard.Notecard
```  

[Notecard](#classnotecard_1_1notecard_1_1_notecard) class for Serial communication.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`uart`](#classnotecard_1_1notecard_1_1_open_serial_1a535a6dffc769a9f55214ea22095f598f) | 
`public  `[`lock_handle`](#classnotecard_1_1notecard_1_1_open_serial_1a7b05b5cdd7e74ed816ca6c7dd426ede4) | 
`public def `[`receive`](#classnotecard_1_1notecard_1_1_open_serial_1ab62dc416d016c525be4364173de85995)`(self,timeout_secs,delay)` | Read a newline-terminated batch of data from the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`transmit`](#classnotecard_1_1notecard_1_1_open_serial_1a54c209ff27bcd9eff8297b2d47399613)`(self,data,delay)` | Send `data` to the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`Reset`](#classnotecard_1_1notecard_1_1_open_serial_1a849ee6e929c9dd79438f0fa6df78a3c0)`(self)` | Reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`lock`](#classnotecard_1_1notecard_1_1_open_serial_1ab0d433a64bf80a18617b676154a4d1fe)`(self)` | Lock access to the serial bus.
`public def `[`unlock`](#classnotecard_1_1notecard_1_1_open_serial_1a41fece5c52619e08fd768ab6695b973e)`(self)` | Unlock access to the serial bus.
`public def `[`__init__`](#classnotecard_1_1notecard_1_1_open_serial_1a040d9eca2e104251b5f41c750ab99b09)`(self,uart_id,debug,lock_path)` | Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) before a reset.

## Members

#### `public  `[`uart`](#classnotecard_1_1notecard_1_1_open_serial_1a535a6dffc769a9f55214ea22095f598f) 

#### `public  `[`lock_handle`](#classnotecard_1_1notecard_1_1_open_serial_1a7b05b5cdd7e74ed816ca6c7dd426ede4) 

#### `public def `[`receive`](#classnotecard_1_1notecard_1_1_open_serial_1ab62dc416d016c525be4364173de85995)`(self,timeout_secs,delay)` 

Read a newline-terminated batch of data from the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`transmit`](#classnotecard_1_1notecard_1_1_open_serial_1a54c209ff27bcd9eff8297b2d47399613)`(self,data,delay)` 

Send `data` to the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`Reset`](#classnotecard_1_1notecard_1_1_open_serial_1a849ee6e929c9dd79438f0fa6df78a3c0)`(self)` 

Reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`lock`](#classnotecard_1_1notecard_1_1_open_serial_1ab0d433a64bf80a18617b676154a4d1fe)`(self)` 

Lock access to the serial bus.

#### `public def `[`unlock`](#classnotecard_1_1notecard_1_1_open_serial_1a41fece5c52619e08fd768ab6695b973e)`(self)` 

Unlock access to the serial bus.

#### `public def `[`__init__`](#classnotecard_1_1notecard_1_1_open_serial_1a040d9eca2e104251b5f41c750ab99b09)`(self,uart_id,debug,lock_path)` 

Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) before a reset.

#### Parameters
* `uart_id` The serial port identifier. 

* `debug` Enable debug output if True. 

* `lock_path` Optional path for the serial lock file. Defaults to /tmp/serial.lock or the value of NOTECARD_SERIAL_LOCK_PATH environment variable.

# class `notecard::notecard::OpenI2C` 

```
class notecard::notecard::OpenI2C
  : public notecard.notecard.Notecard
```  

[Notecard](#classnotecard_1_1notecard_1_1_notecard) class for I2C communication.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`i2c`](#classnotecard_1_1notecard_1_1_open_i2_c_1a61669afca716a4ecad40774bb3fe2b21) | 
`public  `[`lock_fn`](#classnotecard_1_1notecard_1_1_open_i2_c_1ac8090b8bb0ce9967fd35c50c61246ed5) | 
`public  `[`unlock_fn`](#classnotecard_1_1notecard_1_1_open_i2_c_1a4699df095076f9d1915dd39562ab9715) | 
`public  `[`addr`](#classnotecard_1_1notecard_1_1_open_i2_c_1afff615bd9246ff99e985dc376a2231ae) | 
`public  `[`max`](#classnotecard_1_1notecard_1_1_open_i2_c_1a5e11ead325bcfc3751f3871b092ba106) | 
`public def `[`receive`](#classnotecard_1_1notecard_1_1_open_i2_c_1ad726819f3902a293bc560940d1fbea19)`(self,timeout_secs,delay)` | Read a newline-terminated batch of data from the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`transmit`](#classnotecard_1_1notecard_1_1_open_i2_c_1ad63819fde653bb8c23a525b65d00d550)`(self,data,delay)` | Send `data` to the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`Reset`](#classnotecard_1_1notecard_1_1_open_i2_c_1a97e342005debf13a760dfb883285cb1f)`(self)` | Reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`lock`](#classnotecard_1_1notecard_1_1_open_i2_c_1ad08fc53b1f65f65deadff51d4c0f2a55)`(self)` | Lock access to the I2C bus.
`public def `[`unlock`](#classnotecard_1_1notecard_1_1_open_i2_c_1ae703aacbde5912e8f829c99dd2f67564)`(self)` | Unlock access to the I2C bus.
`public def `[`__init__`](#classnotecard_1_1notecard_1_1_open_i2_c_1aa8d36c469c524c8910db32a6eb98d7d7)`(self,`[`i2c`](#classnotecard_1_1notecard_1_1_open_i2_c_1a61669afca716a4ecad40774bb3fe2b21)`,address,max_transfer,debug)` | Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) before a reset.

## Members

#### `public  `[`i2c`](#classnotecard_1_1notecard_1_1_open_i2_c_1a61669afca716a4ecad40774bb3fe2b21) 

#### `public  `[`lock_fn`](#classnotecard_1_1notecard_1_1_open_i2_c_1ac8090b8bb0ce9967fd35c50c61246ed5) 

#### `public  `[`unlock_fn`](#classnotecard_1_1notecard_1_1_open_i2_c_1a4699df095076f9d1915dd39562ab9715) 

#### `public  `[`addr`](#classnotecard_1_1notecard_1_1_open_i2_c_1afff615bd9246ff99e985dc376a2231ae) 

#### `public  `[`max`](#classnotecard_1_1notecard_1_1_open_i2_c_1a5e11ead325bcfc3751f3871b092ba106) 

#### `public def `[`receive`](#classnotecard_1_1notecard_1_1_open_i2_c_1ad726819f3902a293bc560940d1fbea19)`(self,timeout_secs,delay)` 

Read a newline-terminated batch of data from the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`transmit`](#classnotecard_1_1notecard_1_1_open_i2_c_1ad63819fde653bb8c23a525b65d00d550)`(self,data,delay)` 

Send `data` to the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`Reset`](#classnotecard_1_1notecard_1_1_open_i2_c_1a97e342005debf13a760dfb883285cb1f)`(self)` 

Reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`lock`](#classnotecard_1_1notecard_1_1_open_i2_c_1ad08fc53b1f65f65deadff51d4c0f2a55)`(self)` 

Lock access to the I2C bus.

#### `public def `[`unlock`](#classnotecard_1_1notecard_1_1_open_i2_c_1ae703aacbde5912e8f829c99dd2f67564)`(self)` 

Unlock access to the I2C bus.

#### `public def `[`__init__`](#classnotecard_1_1notecard_1_1_open_i2_c_1aa8d36c469c524c8910db32a6eb98d7d7)`(self,`[`i2c`](#classnotecard_1_1notecard_1_1_open_i2_c_1a61669afca716a4ecad40774bb3fe2b21)`,address,max_transfer,debug)` 

Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) before a reset.

# namespace `notecard::timeout` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`ticks_diff`](#namespacenotecard_1_1timeout_1ad9a90871e0e7a3cc0e8ff46d95793003)`(ticks1,ticks2)`            | Compute the signed difference between two ticks values.
`public def `[`has_timed_out`](#namespacenotecard_1_1timeout_1ab53cef58dd467a7dff2127c07d921869)`(start,timeout_secs)`            | Determine whether a timeout interval has passed during communication.
`public def `[`start_timeout`](#namespacenotecard_1_1timeout_1a8fb75238528751cd9f911d2b5cd71a25)`()`            | Start the timeout interval for I2C communication.

## Members

#### `public def `[`ticks_diff`](#namespacenotecard_1_1timeout_1ad9a90871e0e7a3cc0e8ff46d95793003)`(ticks1,ticks2)` 

Compute the signed difference between two ticks values.

#### `public def `[`has_timed_out`](#namespacenotecard_1_1timeout_1ab53cef58dd467a7dff2127c07d921869)`(start,timeout_secs)` 

Determine whether a timeout interval has passed during communication.

#### `public def `[`start_timeout`](#namespacenotecard_1_1timeout_1a8fb75238528751cd9f911d2b5cd71a25)`()` 

Start the timeout interval for I2C communication.

# namespace `notecard::transaction_manager` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`notecard::transaction_manager::TransactionManager`](#classnotecard_1_1transaction__manager_1_1_transaction_manager) | Class for managing the start and end of Notecard transactions.
`class `[`notecard::transaction_manager::NoOpTransactionManager`](#classnotecard_1_1transaction__manager_1_1_no_op_transaction_manager) | Class for transaction start/stop when no transaction pins are set.

# class `notecard::transaction_manager::TransactionManager` 

Class for managing the start and end of Notecard transactions.

Some Notecards need to be signaled via GPIO when a transaction is about to start. When the Notecard sees a particular GPIO, called RTX (ready to transact), go high, it responds with a high pulse on another GPIO, CTX (clear to transact). At this point, the transaction can proceed. This class implements this protocol in its start method.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`rtx_pin`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1adde705bd38d642cf6808a639a3104d21) | 
`public  `[`ctx_pin`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1abdabb2837e3be1c43db68c702420ad30) | 
`public def `[`__init__`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1a958f267c61309e6c9afcef48f434ad3b)`(self,`[`rtx_pin`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1adde705bd38d642cf6808a639a3104d21)`,`[`ctx_pin`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1abdabb2837e3be1c43db68c702420ad30)`)` | Initialize the [TransactionManager](#classnotecard_1_1transaction__manager_1_1_transaction_manager).
`public def `[`start`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1aaa0be5423323d22dc542d875eee2406a)`(self,timeout_secs)` | Prepare the Notecard for a transaction.
`public def `[`stop`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1a8d4c951f2958067adad37ff8ab711d3a)`(self)` | Make RTX an input to conserve power and remove the pull up on CTX.

## Members

#### `public  `[`rtx_pin`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1adde705bd38d642cf6808a639a3104d21) 

#### `public  `[`ctx_pin`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1abdabb2837e3be1c43db68c702420ad30) 

#### `public def `[`__init__`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1a958f267c61309e6c9afcef48f434ad3b)`(self,`[`rtx_pin`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1adde705bd38d642cf6808a639a3104d21)`,`[`ctx_pin`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1abdabb2837e3be1c43db68c702420ad30)`)` 

Initialize the [TransactionManager](#classnotecard_1_1transaction__manager_1_1_transaction_manager).

Even though RTX is an output, we set it as an input here to conserve
   power until we need to use it.

#### `public def `[`start`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1aaa0be5423323d22dc542d875eee2406a)`(self,timeout_secs)` 

Prepare the Notecard for a transaction.

#### `public def `[`stop`](#classnotecard_1_1transaction__manager_1_1_transaction_manager_1a8d4c951f2958067adad37ff8ab711d3a)`(self)` 

Make RTX an input to conserve power and remove the pull up on CTX.

# class `notecard::transaction_manager::NoOpTransactionManager` 

Class for transaction start/stop when no transaction pins are set.

If the transaction pins aren't set, the start and stop operations should be no-ops.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`start`](#classnotecard_1_1transaction__manager_1_1_no_op_transaction_manager_1a824ef28e518f4ffc0fb568831c3da8b0)`(self,timeout_secs)` | No-op start function.
`public def `[`stop`](#classnotecard_1_1transaction__manager_1_1_no_op_transaction_manager_1aaa8be92baadc71b99e3fe0182655bb9a)`(self)` | No-op stop function.

## Members

#### `public def `[`start`](#classnotecard_1_1transaction__manager_1_1_no_op_transaction_manager_1a824ef28e518f4ffc0fb568831c3da8b0)`(self,timeout_secs)` 

No-op start function.

#### `public def `[`stop`](#classnotecard_1_1transaction__manager_1_1_no_op_transaction_manager_1aaa8be92baadc71b99e3fe0182655bb9a)`(self)` 

No-op stop function.

# namespace `notecard::validators` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`validate_card_object`](#namespacenotecard_1_1validators_1ada114fe04694d162593e55bcffeeaa6b)`(func)`            | Ensure that the passed-in card is a Notecard.

## Members

#### `public def `[`validate_card_object`](#namespacenotecard_1_1validators_1ada114fe04694d162593e55bcffeeaa6b)`(func)` 

Ensure that the passed-in card is a Notecard.

Skip validation.

Generated by [Moxygen](https://sourcey.com/moxygen)