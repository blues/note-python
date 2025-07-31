# Notecard API Reference

## Card Commands

`from notecard import card`

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `card.attn`            | card.attn          |
| `card.aux`             | NOT IMPLEMENTED    |
| `card.contact`         | NOT IMPLEMENTED    |
| `card.location`        | card.location      |
| `card.location.mode`   | card.location_mode |
| `card.location.track`  | card.location_track|
| `card.motion.mode`     | NOT IMPLEMENTED    |
| `card.motion.sync`     | NOT IMPLEMENTED    |
| `card.motion.track`    | NOT IMPLEMENTED    |
| `card.power`           | card.power         |
| `card.restart`         | NOT IMPLEMENTED    |
| `card.restore`         | NOT IMPLEMENTED    |
| `card.status`          | card.status        |
| `card.temp`            | card.temp          |
| `card.time`            | card.time          |
| `card.transport`       | card.transport     |
| `card.usage.get`       | NOT IMPLEMENTED    |
| `card.usage.test`      | NOT IMPLEMENTED    |
| `card.version`         | card.version       |
| `card.voltage`         | card.voltage       |
| `card.wireless`        | card.wireless      |

## Note Commands

`from notecard import note`

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `note.add`             | note.add           |
| `note.changes`         | note.changes       |
| `note.delete`          | note.delete        |
| `note.get`             | note.get           |
| `note.update`          | note.update        |
| `note.template`        | note.template      |

## Hub Commands

`from notecard import hub`

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `hub.get`              | hub.get            |
| `hub.log`              | hub.log            |
| `hub.set`              | hub.set            |
| `hub.status`           | hub.status         |
| `hub.sync`             | hub.sync           |
| `hub.sync.status`      | hub.syncStatus     |

## DFU Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `dfu.get`              | NOT IMPLEMENTED    |
| `dfu.set`              | NOT IMPLEMENTED    |

## Env Commands

`from notecard import env`

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `env.default`          | env.default        |
| `env.get`              | env.get            |
| `env.modified`         | env.modified       |
| `set`                  | env.set            |

## File Commands

`from notecard import file`

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `file.changes`         | file.changes       |
| `file.delete`          | file.delete        |
| `file.stats`           | file.stats         |
| `file.changes.pending` | file.pendingChanges|

## Web Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `web.get`              | NOT IMPLEMENTED    |
| `web.post`             | NOT IMPLEMENTED    |
| `web.put`              | NOT IMPLEMENTED    |
