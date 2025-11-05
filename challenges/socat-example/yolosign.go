package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io/ioutil"
	"log"
	"math/big"
	"os"
)

var key_size = 768

func read_key() *rsa.PrivateKey {
	pemData, err := ioutil.ReadFile("private_key.rsa")
	if err != nil {
		log.Fatalf("read key file: %s", err)
	}

	block, _ := pem.Decode(pemData)
	if block == nil {
		log.Fatalf("bad key data: %s", "not PEM-encoded")
	}

	switch block.Type {
	case "RSA PRIVATE KEY":
		// PKCS#1 format
		priv, err := x509.ParsePKCS1PrivateKey(block.Bytes)
		if err != nil {
			log.Fatalf("bad PKCS#1 private key: %s", err)
		}
		return priv
	case "PRIVATE KEY":
		// PKCS#8 format
		key, err := x509.ParsePKCS8PrivateKey(block.Bytes)
		if err != nil {
			log.Fatalf("bad PKCS#8 private key: %s", err)
		}
		rsaKey, ok := key.(*rsa.PrivateKey)
		if !ok {
			log.Fatalf("not an RSA private key")
		}
		return rsaKey
	default:
		log.Fatalf("unknown key type %q", block.Type)
		return nil
	}
}

func verify(message, signature *big.Int, key *rsa.PrivateKey) bool {
	return signature.Exp(signature, big.NewInt(int64(key.PublicKey.E)), key.PublicKey.N).Cmp(message) == 0
}

func main() {
	urandom, err := os.Open("/dev/urandom")
	if err != nil {
		log.Fatal(err)
	}
	key := read_key()
	flag, err := ioutil.ReadFile("flag.txt")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Signature Service!\n")
	fmt.Printf("Fingerprint: %x\n", key.PublicKey.N)

	for true {
		fmt.Printf("Menu:\t1. Sign message\n\t2. Get Flag\n\t3. Exit\n > ")
		choice := 0
		fmt.Scanf("%d", &choice)
		if choice == 1 {
			message := new(big.Int)
			fmt.Printf("Message to sign > ")
			fmt.Scanf("%x", message)
			message.Mod(message, key.PublicKey.N)
			message.Exp(message, key.D, key.PublicKey.N)
			fmt.Printf("Signature: %x\n", message)
		} else if choice == 2 {
			challenge, err := rand.Int(urandom, key.PublicKey.N)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Challenge: %x\n", challenge)
			signature := new(big.Int)
			fmt.Printf("Signature > ")
			fmt.Scanf("%x", signature)
			if verify(challenge, signature, key) {
				fmt.Printf("Here is the flag: %s\n", flag)
			} else {
				fmt.Printf("Nope!\n")
			}
			break
		} else {
			fmt.Printf("Good Bye.\n")
			break
		}
	}
}
