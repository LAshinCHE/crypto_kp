package main

import (
	"encoding/hex"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
)

const (
	cntRounds = 80
	blockSize = 512
)

func main() {
	inputPtr := flag.String("input", "", "Input file to hash")
	roundsPtr := flag.Int("rounds", cntRounds, "Count rounds (<= 80)")
	flag.Parse()

	rounds := *roundsPtr
	filename := *inputPtr

	if _, err := os.Stat(filename); err == nil {
		text, err := ioutil.ReadFile(filename)
		if err != nil {
			fmt.Println("Error reading file:", err)
			return
		}
		fmt.Println("sha1:", sha1(text, rounds))
	} else {
		fmt.Println("Error, could not find", filename, "file.")
	}
}

func sha1(msg []byte, rounds int) string {
	h := [5]uint32{
		0x67452301,
		0xEFCDAB89,
		0x98BADCFE,
		0x10325476,
		0xC3D2E1F0,
	}

	lenMsg := uint64(len(msg) * 8)

	msg = append(msg, 0x80)

	for len(msg)%blockSize != blockSize-64 {
		msg = append(msg, 0)
	}

	msg = append(msg, byte(lenMsg>>56), byte(lenMsg>>48), byte(lenMsg>>40), byte(lenMsg>>32), byte(lenMsg>>24), byte(lenMsg>>16), byte(lenMsg>>8), byte(lenMsg))

	chunks := getChunks(msg)

	for _, chunk := range chunks {
		h = processChunk(chunk, h, rounds)
	}

	hash := make([]byte, 20)
	for i, v := range h {
		hash[i*4] = byte(v >> 24)
		hash[i*4+1] = byte(v >> 16)
		hash[i*4+2] = byte(v >> 8)
		hash[i*4+3] = byte(v)
	}

	return hex.EncodeToString(hash)
}

func getChunks(msg []byte) [][]byte {
	var chunks [][]byte
	for i := 0; i < len(msg); i += blockSize {
		end := i + blockSize
		if end > len(msg) {
			end = len(msg)
		}
		chunks = append(chunks, msg[i:end])
	}
	return chunks
}

func processChunk(chunk []byte, h [5]uint32, rounds int) [5]uint32 {
	w := make([]uint32, 80)

	for i := 0; i < 16; i++ {
		w[i] = uint32(chunk[i*4])<<24 | uint32(chunk[i*4+1])<<16 | uint32(chunk[i*4+2])<<8 | uint32(chunk[i*4+3])
	}

	for i := 16; i < 80; i++ {
		w[i] = rotl(w[i-3]^w[i-8]^w[i-14]^w[i-16], 1)
	}

	a, b, c, d, e := h[0], h[1], h[2], h[3], h[4]

	for i := 0; i < rounds; i++ {
		var f, k uint32
		switch {
		case 0 <= i && i <= 19:
			f = (b & c) | ((^b) & d)
			k = 0x5A827999
		case 20 <= i && i <= 39:
			f = b ^ c ^ d
			k = 0x6ED9EBA1
		case 40 <= i && i <= 59:
			f = (b & c) | (b & d) | (c & d)
			k = 0x8F1BBCDC
		case 60 <= i && i <= 79:
			f = b ^ c ^ d
			k = 0xCA62C1D6
		}

		a, b, c, d, e = rotl(a, 5)+f+e+k+w[i], a, rotl(b, 30), c, d
	}

	return [5]uint32{h[0] + a, h[1] + b, h[2] + c, h[3] + d, h[4] + e}
}

func rotl(n, k uint32) uint32 {
	return (n << k) | (n >> (32 - k))
}
