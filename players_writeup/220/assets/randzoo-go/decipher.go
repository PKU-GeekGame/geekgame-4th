package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strconv"
)

const numsFilename = "randzoo-nums.txt"
const randSeed = 1566025109

func main() {
	// for each line, load the number and sub random number from seed, convert to char, print
	file, err := os.Open(numsFilename)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	rng := rand.New(rand.NewSource(randSeed))
	for scanner.Scan() {
		num, err := strconv.Atoi(scanner.Text())
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		fmt.Printf("%c", uint32(num)-rng.Uint32())
	}
}
