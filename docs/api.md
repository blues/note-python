# Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`namespace `[`notecard::card`](#namespacenotecard_1_1card) | 
`namespace `[`notecard::env`](#namespacenotecard_1_1env) | 
`namespace `[`notecard::file`](#namespacenotecard_1_1file) | 
`namespace `[`notecard::hub`](#namespacenotecard_1_1hub) | 
`namespace `[`notecard::note`](#namespacenotecard_1_1note) | 
`namespace `[`notecard::notecard`](#namespacenotecard_1_1notecard) | 
`namespace `[`notecard::validators`](#namespacenotecard_1_1validators) | 

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

* `mode` The wireless module mode to set. 

* `apn` Access Point Name (APN) when using an external SIM.

#### Returns

#### Returns
string The result of the Notecard request.

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

# namespace `notecard::hub` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`set`](#namespacenotecard_1_1hub_1a73cf5906caf41a3342c8838ad0bb8d48)`(card,product,sn,mode,outbound,inbound,duration,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`,align,voutbound,vinbound,host)`            | Configure Notehub behavior on the Notecard.
`public def `[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`(card)`            | Initiate a sync of the Notecard to Notehub.
`public def `[`syncStatus`](#namespacenotecard_1_1hub_1adeec5dd54d3ce966f7e08bee81105d2b)`(card,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`)`            | Retrieve the status of a sync request.
`public def `[`status`](#namespacenotecard_1_1hub_1a5c44efc254a08e2f8eb6d6b2d3d9ab82)`(card)`            | Retrieve the status of the Notecard's connection.
`public def `[`log`](#namespacenotecard_1_1hub_1aa78d6e2e3028e6022b3b9405527937b2)`(card,text,alert,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`)`            | Send a log request to the Notecard.
`public def `[`get`](#namespacenotecard_1_1hub_1a5c2687d0e446715d54c1dd7b4ac4c682)`(card)`            | Retrieve the current Notehub configuration parameters.

## Members

#### `public def `[`set`](#namespacenotecard_1_1hub_1a73cf5906caf41a3342c8838ad0bb8d48)`(card,product,sn,mode,outbound,inbound,duration,`[`sync`](#namespacenotecard_1_1hub_1a614f01eb985b28a45706183f7a7a20ea)`,align,voutbound,vinbound,host)` 

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

# namespace `notecard::note` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`changes`](#namespacenotecard_1_1note_1a660dda3f8fa6f9afff52e0a3be6bef84)`(card,file,tracker,maximum,start,stop,deleted,`[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`)`            | Incrementally retrieve changes within a Notefile.
`public def `[`get`](#namespacenotecard_1_1note_1ad7a4c296382c14a8efb54278c127d73b)`(card,file,note_id,`[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`,deleted)`            | Retrieve a note from an inbound or DB Notefile.
`public def `[`delete`](#namespacenotecard_1_1note_1a591ece0048b58f38acf22d97a533577f)`(card,file,note_id)`            | Delete a DB note in a Notefile by its ID.
`public def `[`update`](#namespacenotecard_1_1note_1a149f30ef24735181e7d55477a50bd9d5)`(card,file,note_id,body,payload)`            | Update a note in a DB Notefile by ID.
`public def `[`template`](#namespacenotecard_1_1note_1a1e625660366b3766ec9efa8270a7f5bb)`(card,file,body,length)`            | Create a template for new Notes in a Notefile.

## Members

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

#### `public def `[`template`](#namespacenotecard_1_1note_1a1e625660366b3766ec9efa8270a7f5bb)`(card,file,body,length)` 

Create a template for new Notes in a Notefile.

#### Parameters
* `card` The current Notecard object. 

* `file` The file name of the notefile. 

* `body` A sample JSON body that specifies field names and values as "hints" for the data type. 

* `length` If provided, the maximum length of a payload that can be sent in Notes for the template Notefile.

#### Returns

#### Returns
string The result of the Notecard request.

# namespace `notecard::notecard` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`serialReadByte`](#namespacenotecard_1_1notecard_1a86722827e14af53ddcd38c47ff9a119a)`(port)`            | Read a single byte from a [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`serialReset`](#namespacenotecard_1_1notecard_1aa1badb3c10bdc0321b9a556e8cd49148)`(port)`            | Send a reset command to a [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`serialTransaction`](#namespacenotecard_1_1notecard_1aee094fc03befdcbe4ee4a9d658d09841)`(port,req,debug)`            | Perform a single write to and read from a [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`serialCommand`](#namespacenotecard_1_1notecard_1af2b5752d8f67ffcebeda99511e37e7a1)`(port,req,debug)`            | Perform a single write to and read from a [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`class `[`notecard::notecard::Notecard`](#classnotecard_1_1notecard_1_1_notecard) | Base [Notecard](#classnotecard_1_1notecard_1_1_notecard) class.
`class `[`notecard::notecard::OpenI2C`](#classnotecard_1_1notecard_1_1_open_i2_c) | [Notecard](#classnotecard_1_1notecard_1_1_notecard) class for I2C communication.
`class `[`notecard::notecard::OpenSerial`](#classnotecard_1_1notecard_1_1_open_serial) | [Notecard](#classnotecard_1_1notecard_1_1_notecard) class for Serial communication.

## Members

#### `public def `[`serialReadByte`](#namespacenotecard_1_1notecard_1a86722827e14af53ddcd38c47ff9a119a)`(port)` 

Read a single byte from a [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`serialReset`](#namespacenotecard_1_1notecard_1aa1badb3c10bdc0321b9a556e8cd49148)`(port)` 

Send a reset command to a [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`serialTransaction`](#namespacenotecard_1_1notecard_1aee094fc03befdcbe4ee4a9d658d09841)`(port,req,debug)` 

Perform a single write to and read from a [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`serialCommand`](#namespacenotecard_1_1notecard_1af2b5752d8f67ffcebeda99511e37e7a1)`(port,req,debug)` 

Perform a single write to and read from a [Notecard](#classnotecard_1_1notecard_1_1_notecard).

# class `notecard::notecard::Notecard` 

Base [Notecard](#classnotecard_1_1notecard_1_1_notecard) class.

Primary [Notecard](#classnotecard_1_1notecard_1_1_notecard) Class, which provides a shared **init** to reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard) via Serial or I2C.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classnotecard_1_1notecard_1_1_notecard_1a126d43070dfa4b552bc92c06be1c6d1e)`(self)` | Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) through a reset.

## Members

#### `public def `[`__init__`](#classnotecard_1_1notecard_1_1_notecard_1a126d43070dfa4b552bc92c06be1c6d1e)`(self)` 

Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) through a reset.

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
`public  `[`addr`](#classnotecard_1_1notecard_1_1_open_i2_c_1afff615bd9246ff99e985dc376a2231ae) | 
`public  `[`max`](#classnotecard_1_1notecard_1_1_open_i2_c_1a5e11ead325bcfc3751f3871b092ba106) | 
`public def `[`Transaction`](#classnotecard_1_1notecard_1_1_open_i2_c_1ab09d0871a3242cc1b7dec217fcd81939)`(self,req)` | Perform a [Notecard](#classnotecard_1_1notecard_1_1_notecard) transaction and return the result.
`public def `[`Reset`](#classnotecard_1_1notecard_1_1_open_i2_c_1a97e342005debf13a760dfb883285cb1f)`(self)` | Reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`lock`](#classnotecard_1_1notecard_1_1_open_i2_c_1ad08fc53b1f65f65deadff51d4c0f2a55)`(self)` | Lock the I2C port so the host can interact with the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`unlock`](#classnotecard_1_1notecard_1_1_open_i2_c_1ae703aacbde5912e8f829c99dd2f67564)`(self)` | Unlock the I2C port.
`public def `[`__init__`](#classnotecard_1_1notecard_1_1_open_i2_c_1aa8d36c469c524c8910db32a6eb98d7d7)`(self,`[`i2c`](#classnotecard_1_1notecard_1_1_open_i2_c_1a61669afca716a4ecad40774bb3fe2b21)`,address,max_transfer,debug)` | Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) before a reset.

## Members

#### `public  `[`i2c`](#classnotecard_1_1notecard_1_1_open_i2_c_1a61669afca716a4ecad40774bb3fe2b21) 

#### `public  `[`addr`](#classnotecard_1_1notecard_1_1_open_i2_c_1afff615bd9246ff99e985dc376a2231ae) 

#### `public  `[`max`](#classnotecard_1_1notecard_1_1_open_i2_c_1a5e11ead325bcfc3751f3871b092ba106) 

#### `public def `[`Transaction`](#classnotecard_1_1notecard_1_1_open_i2_c_1ab09d0871a3242cc1b7dec217fcd81939)`(self,req)` 

Perform a [Notecard](#classnotecard_1_1notecard_1_1_notecard) transaction and return the result.

#### `public def `[`Reset`](#classnotecard_1_1notecard_1_1_open_i2_c_1a97e342005debf13a760dfb883285cb1f)`(self)` 

Reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`lock`](#classnotecard_1_1notecard_1_1_open_i2_c_1ad08fc53b1f65f65deadff51d4c0f2a55)`(self)` 

Lock the I2C port so the host can interact with the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`unlock`](#classnotecard_1_1notecard_1_1_open_i2_c_1ae703aacbde5912e8f829c99dd2f67564)`(self)` 

Unlock the I2C port.

#### `public def `[`__init__`](#classnotecard_1_1notecard_1_1_open_i2_c_1aa8d36c469c524c8910db32a6eb98d7d7)`(self,`[`i2c`](#classnotecard_1_1notecard_1_1_open_i2_c_1a61669afca716a4ecad40774bb3fe2b21)`,address,max_transfer,debug)` 

Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) before a reset.

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
`public  `[`lock`](#classnotecard_1_1notecard_1_1_open_serial_1afbc7e0e12502762f8d7a205085ec9deb) | 
`public def `[`Request`](#classnotecard_1_1notecard_1_1_open_serial_1aed3df72d86f07f5960500b811213db68)`(self,req)` | Call the Transaction method and discard the result.
`public def `[`RequestResponse`](#classnotecard_1_1notecard_1_1_open_serial_1aec9d0d2754f4d8744c4db8d9488c859f)`(self,req)` | Call the Transaction method and return the result.
`public def `[`Command`](#classnotecard_1_1notecard_1_1_open_serial_1aa6f70223bc2bfdaf9da2667f4181d4ad)`(self,req)` | Perform a [Notecard](#classnotecard_1_1notecard_1_1_notecard) command and exit with no response.
`public def `[`Transaction`](#classnotecard_1_1notecard_1_1_open_serial_1aeb9a39cf7f794a38e8aadd1d9db6f7c7)`(self,req)` | Perform a [Notecard](#classnotecard_1_1notecard_1_1_notecard) transaction and return the result.
`public def `[`Reset`](#classnotecard_1_1notecard_1_1_open_serial_1a849ee6e929c9dd79438f0fa6df78a3c0)`(self)` | Reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard).
`public def `[`__init__`](#classnotecard_1_1notecard_1_1_open_serial_1a917a4086f15fe6b83e5342a36a1b2dbc)`(self,uart_id,debug)` | Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) before a reset.

## Members

#### `public  `[`uart`](#classnotecard_1_1notecard_1_1_open_serial_1a535a6dffc769a9f55214ea22095f598f) 

#### `public  `[`lock`](#classnotecard_1_1notecard_1_1_open_serial_1afbc7e0e12502762f8d7a205085ec9deb) 

#### `public def `[`Request`](#classnotecard_1_1notecard_1_1_open_serial_1aed3df72d86f07f5960500b811213db68)`(self,req)` 

Call the Transaction method and discard the result.

#### `public def `[`RequestResponse`](#classnotecard_1_1notecard_1_1_open_serial_1aec9d0d2754f4d8744c4db8d9488c859f)`(self,req)` 

Call the Transaction method and return the result.

#### `public def `[`Command`](#classnotecard_1_1notecard_1_1_open_serial_1aa6f70223bc2bfdaf9da2667f4181d4ad)`(self,req)` 

Perform a [Notecard](#classnotecard_1_1notecard_1_1_notecard) command and exit with no response.

#### `public def `[`Transaction`](#classnotecard_1_1notecard_1_1_open_serial_1aeb9a39cf7f794a38e8aadd1d9db6f7c7)`(self,req)` 

Perform a [Notecard](#classnotecard_1_1notecard_1_1_notecard) transaction and return the result.

#### `public def `[`Reset`](#classnotecard_1_1notecard_1_1_open_serial_1a849ee6e929c9dd79438f0fa6df78a3c0)`(self)` 

Reset the [Notecard](#classnotecard_1_1notecard_1_1_notecard).

#### `public def `[`__init__`](#classnotecard_1_1notecard_1_1_open_serial_1a917a4086f15fe6b83e5342a36a1b2dbc)`(self,uart_id,debug)` 

Initialize the [Notecard](#classnotecard_1_1notecard_1_1_notecard) before a reset.

# namespace `notecard::validators` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`validate_card_object`](#namespacenotecard_1_1validators_1a67c61d583c23a6be17354d84575bdc93)`(func)`            | Ensure that the passed-in card is a Notecard.

## Members

#### `public def `[`validate_card_object`](#namespacenotecard_1_1validators_1a67c61d583c23a6be17354d84575bdc93)`(func)` 

Ensure that the passed-in card is a Notecard.

Generated by [Moxygen](https://sourcey.com/moxygen)