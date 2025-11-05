# Yolosign

- Namespace: picoctf
- ID: yolosign
- Type: custom
- Category: Cryptography
- Points: 200
- Templatable: yes
- MaxUsers: 1

## Description

Forge a 768-bit RSA signature and get the flag. Easy right?

## Details

Connect to the remote service with netcat:

`$ nc {{server}} {{port}}`

## Hints

- The key is identical across connections.

## Solution Overview

## Challenge Options

```yaml
cpus: 0.5
memory: 128m
pidslimit: 200
ulimits:
  - nofile=128:128
diskquota: 64m
init: true
```

## Learning Objective

## Attributes

- author: ForAllSecure
- organization: picoCTF
- event: RSAC picoCTF
