# SEMSEC-101
  - Namespace: picoctf
  - ID: semsec-101
  - Type: custom
  - Category: Cryptography
  - Points: 200
  - Templatable: yes

## Description

Crypto secure starts with "semantic security".  That's an SAT-level
word, but it's really just winning a guessing game.


## Details

The semantic security game is running at {{link_as('/', 'here')}}.

## Hints
 - The block cipher is secure, but do you know about encryption modes?
 - Try a plaintext attack using "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
   as one of your inputs.
 - You can hit the web interface or the API.

## Tags
 - beginner

## Challenge Options

```yaml
cpus: 0.5
memory: 128m
ulimits:
  - nofile=128:128
diskquota: 64m
init: true
```

## Solution Overview
This shows how using a block cipher in ECB mode is not semantically
secure because you can tell if two identical blocks encrypt
to the same values.

I.e., you can deterministically win this game by looking at:
encrypt(AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC)


## Attributes
- author: David Brumley
- event: RSAC picoCTF

