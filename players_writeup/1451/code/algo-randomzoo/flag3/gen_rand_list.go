package main

import (
	"fmt"
	"math/rand"
	"os"
)

func main() {
	file, err := os.Create("rand_list.txt")
	if err != nil {
		fmt.Println("无法创建文件:", err)
		return
	}
	defer file.Close()

	rng := rand.New(rand.NewSource(int64(169628184)))

	for i := uint32(0); i < 100; i++ {
		randNum := rng.Uint32()
		file.WriteString(fmt.Sprintf("%d\n", randNum))
	}
}
