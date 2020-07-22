# Notecard API Reference

## Card Commands

`from notecard import card`

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `card.attn`            | card.attn          |
| `card.aux`             | NOT IMPLEMENTED                |
| `card.contact`         | NOT IMPLEMENTED                 |
| `card.location.mode`   | NOT IMPLEMENTED                 |
| `card.location.track`  | NOT IMPLEMENTED                 |
| `card.motion.mode`     | NOT IMPLEMENTED                 |
| `card.motion.sync`     | NOT IMPLEMENTED                 |
| `card.motion.track`    | NOT IMPLEMENTED                 |
| `card.restart`         | NOT IMPLEMENTED                 |
| `card.restore`         | NOT IMPLEMENTED                 |
| `card.status`          | card.status        |
| `card.temp`            | card.temp          |
| `card.time`            | card.time          |
| `card.usage.get`       | NOT IMPLEMENTED                 |
| `card.usage.test`      | NOT IMPLEMENTED                 |
| `card.version`         | NOT IMPLEMENTED                 |
| `card.voltage`         | NOT IMPLEMENTED                 |
| `card.wireless`        | card.wireless      |

## Note Commands

`from notecard import note`

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `note.add`             | note.add           |
| `note.changes`         | NOT IMPLEMENTED                 |
| `note.delete`          | NOT IMPLEMENTED                 |
| `note.get`             | note.get           |
| `note.update`          | NOT IMPLEMENTED                 |

## Hub Commands

`from notecard import hub`

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `hub.get`          | hub.get        |
| `hub.log`          | hub.log        |
| `hub.set`          | hub.set        |
| `hub.status`       | hub.status     |
| `hub.sync`         | hub.sync       |
| `hub.sync.status`  | hub.syncStatus |

## DFU Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `dfu.get`              | NOT IMPLEMENTED    |
| `dfu.set`              | NOT IMPLEMENTED    |

## Env Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `get`                  | NOT IMPLEMENTED                 |

## File Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `file.changes`         | NOT IMPLEMENTED                 |
| `file.delete`          | NOT IMPLEMENTED                 |
| `file.stats`           | NOT IMPLEMENTED                 |

## Web Commands

| Notecard API           | Python Library API |
| -----------------------| -------------------|
| `web.get`              | NOT IMPLEMENTED                 |
| `web.post`             | NOT IMPLEMENTED                 |
| `web.put`              | NOT IMPLEMENTED                 |