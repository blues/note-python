# Notecard API Reference

## Card Commands

`from notecard import card`

| Notecard API            | Python Library API  |
| ----------------------- | ------------------- |
| `card.attn`             | card.attn           |
| `card.aux`              | card.aux            |
| `card.aux.serial`       | card.aux_serial     |
| `card.binary`           | card.binary         |
| `card.binary.get`       | card.binary_get     |
| `card.binary.put`       | card.binary_put     |
| `card.carrier`          | card.carrier        |
| `card.contact`          | card.contact        |
| `card.dfu`              | NOT IMPLEMENTED     |
| `card.illumination`     | NOT IMPLEMENTED     |
| `card.io`               | NOT IMPLEMENTED     |
| `card.led`              | NOT IMPLEMENTED     |
| `card.location`         | card.location       |
| `card.location.mode`    | card.location_mode  |
| `card.location.track`   | card.location_track |
| `card.monitor`          | NOT IMPLEMENTED     |
| `card.motion`           | NOT IMPLEMENTED     |
| `card.motion.mode`      | NOT IMPLEMENTED     |
| `card.motion.sync`      | NOT IMPLEMENTED     |
| `card.motion.track`     | NOT IMPLEMENTED     |
| `card.power`            | card.power          |
| `card.restart`          | NOT IMPLEMENTED     |
| `card.restore`          | NOT IMPLEMENTED     |
| `card.sleep`            | NOT IMPLEMENTED     |
| `card.status`           | card.status         |
| `card.temp`             | card.temp           |
| `card.time`             | card.time           |
| `card.trace`            | NOT IMPLEMENTED     |
| `card.transport`        | card.transport      |
| `card.triangulate`      | NOT IMPLEMENTED     |
| `card.usage.get`        | NOT IMPLEMENTED     |
| `card.usage.test`       | NOT IMPLEMENTED     |
| `card.version`          | card.version        |
| `card.voltage`          | card.voltage        |
| `card.wifi`             | NOT IMPLEMENTED     |
| `card.wireless`         | card.wireless       |
| `card.wireless.penalty` | NOT IMPLEMENTED     |

## DFU Commands

| Notecard API | Python Library API |
| ------------ | ------------------ |
| `dfu.get`    | NOT IMPLEMENTED    |
| `dfu.set`    | NOT IMPLEMENTED    |

## Env Commands

`from notecard import env`

| Notecard API   | Python Library API |
| -------------- | ------------------ |
| `env.default`  | env.default        |
| `env.get`      | env.get            |
| `env.modified` | env.modified       |
| `env.set`      | env.set            |
| `env.template` | NOT IMPLEMENTED    |

## File Commands

`from notecard import file`

| Notecard API           | Python Library API  |
| ---------------------- | ------------------- |
| `file.changes`         | file.changes        |
| `file.delete`          | file.delete         |
| `file.stats`           | file.stats          |
| `file.changes.pending` | file.pendingChanges |

## Hub Commands

`from notecard import hub`

| Notecard API      | Python Library API |
| ----------------- | ------------------ |
| `hub.get`         | hub.get            |
| `hub.log`         | hub.log            |
| `hub.set`         | hub.set            |
| `hub.status`      | hub.status         |
| `hub.sync`        | hub.sync           |
| `hub.sync.status` | hub.syncStatus     |

## Note Commands

`from notecard import note`

| Notecard API    | Python Library API |
| --------------- | ------------------ |
| `note.add`      | note.add           |
| `note.changes`  | note.changes       |
| `note.delete`   | note.delete        |
| `note.get`      | note.get           |
| `note.update`   | note.update        |
| `note.template` | note.template      |

## NTN Commands

`from notecard import ntn`

| Notecard API | Python Library API |
| ------------ | ------------------ |
| `ntn.gps`    | NOT IMPLEMENTED    |
| `ntn.reset`  | NOT IMPLEMENTED    |
| `ntn.status` | NOT IMPLEMENTED    |

## Var Commands

| Notecard API | Python Library API |
| ------------ | ------------------ |
| `var.delete` | NOT IMPLEMENTED    |
| `var.get`    | NOT IMPLEMENTED    |
| `var.set`    | NOT IMPLEMENTED    |

## Web Commands

| Notecard API | Python Library API |
| ------------ | ------------------ |
| `web.get`    | NOT IMPLEMENTED    |
| `web.post`   | NOT IMPLEMENTED    |
| `web.put`    | NOT IMPLEMENTED    |
| `web.delete` | NOT IMPLEMENTED    |
| `web`        | NOT IMPLEMENTED    |
