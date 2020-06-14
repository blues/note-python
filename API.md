# Notecard API Reference

## Card Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `card.attn`            | CardAttn           |
| `card.aux`             | CardAux            |
| `card.contact`         | CardContact        |
| `card.location.mode`   | CardLocationMode   |
| `card.location.track`  | CardLocationTrack  |
| `card.motion.mode`     | CardMotionMode     |
| `card.motion.sync`     | CardMotionSync     |
| `card.motion.track`    | CardMotionTrack    |
| `card.restart`         | CardRestart        |
| `card.restore`         | CardRestore        |
| `card.status`          | CardStatus         |
| `card.temp`            | CardTemp           |
| `card.time`            | CardTime           |
| `card.usage.get`       | CardGetUsage       |
| `card.usage.set`       | CardSetUsage       |
| `card.version`         | CardVersion        |
| `card.voltage`         | CardVoltage        |
| `card.wireless`        | CardWireless       |

## Note Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `note.add`             | AddNote            |
| `note.changes`         | GetNoteChanges     |
| `note.delete`          | DeleteNote         |
| `note.get`             | GetNote            |
| `note.update`          | UpdateNote         |

## Service Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `service.get`          | GetService         |
| `service.log`          | ServiceLog         |
| `service.set`          | SetService         |
| `service.status`       | ServiceStatus      |
| `service.sync`         | Sync               |
| `service.sync.status`  | SyncStatus         |

## DFU Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `dfu.get`              | DFUGet             |
| `dfu.set`              | DFUSet             |

## Env Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `get`                  | EnvGet             |

## File Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `file.changes`         | GetFileChanges     |
| `file.delete`          | DeleteFile         |
| `file.stats`           | GetFileStats       |

## Hub Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `hub.env.get`          | HubEnvGet          |
| `hub.env.set`          | HubEnvSet          |

## Web Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `web.get`              | WebGet             |
| `web.post`             | WebPost            |
| `web.put`              | WebPut             |