package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/hex"
	"fmt"
	"log"
	"os"
)

var key = []byte{
    0x1e, 0xd7, 0x8b, 0xfc,
    0x49, 0x74, 0xfc, 0xb5,
    0x3c, 0x29, 0x77, 0xa0,
    0xae, 0xfa, 0xea, 0x26,
}

var iv = []byte{
    0x2f, 0x9d, 0x0d, 0xb7,
    0x9f, 0x4f, 0x58, 0xc2,
    0xcb, 0x01, 0xe1, 0xcb,
    0x07, 0xfd, 0x71, 0x51,
}

func decrypt(ciphertext, key, iv []byte) ([]byte, error) {

	if len(ciphertext) % aes.BlockSize != 0 {

		return nil, fmt.Errorf("Ciphertext length is not a multiple of 16")
	}

	block, err := aes.NewCipher(key)

	if err != nil {

		return nil, fmt.Errorf("error: %w", err)
	}

	mode := cipher.NewCBCDecrypter(block, iv)
	plain := make([]byte, len(ciphertext))
	mode.CryptBlocks(plain, ciphertext)

	unpadded, err := unpad_data(plain, aes.BlockSize)
	if err != nil {

		return nil, err
	}
	return unpadded, nil
}

func unpad_data(data []byte, blockSize int) ([]byte, error) {

	if len(data) == 0 || len(data)%blockSize != 0 {

		return nil, fmt.Errorf("invalid data length")
	}
	padding_length := int(data[len(data)-1])
	if padding_length < 1 || padding_length > blockSize {

		return nil, fmt.Errorf("invalid padding length")
	}
	for i := 0; i < padding_length; i++ {

		if data[len(data)-1-i] != byte(padding_length) {
			return nil, fmt.Errorf("invalid padding bytes")
		}
	}
	return data[:len(data)-padding_length], nil
}

func bytesEqual(a, b []byte) bool {

	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func main() {

	ciphertext, err := os.ReadFile("ciphertext.bin")
	if err != nil {
		log.Fatalf("failed to read ciphertext.bin: %s", err)
	}
	fmt.Printf("Ciphertext:%s\n\n", hex.EncodeToString(ciphertext))

	checkmate, err := os.ReadFile("board_target.txt")
	if err != nil {
		log.Fatalf("failed to read board_target.txt: %s", err)
	}

	flag, err := os.ReadFile("flag.txt")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Can you figure out how to get checkmate?\n> ")

	var line string

	if _, err := fmt.Scanf("%s", &line); err != nil {
		return
	}

	if line == "" {
		fmt.Printf("No input received\n")
		return
	}

	user_ciphertext, err := hex.DecodeString(line)
	if err != nil {
		fmt.Printf("Input was not valid hex\n")
		return
	}

	plaintext, err := decrypt(user_ciphertext, key, iv)
	if err != nil {
		fmt.Printf("Decryption failed or invalid padding: %s\n", err)
		return
	}

	if bytesEqual(plaintext, checkmate) {
		fmt.Printf("Here is your flag:\n%s\n", flag)
	} else {
		fmt.Printf("You did not get checkmate\n")
	}
}