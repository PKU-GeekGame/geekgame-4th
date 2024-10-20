package main // require Go 1.20+

import (
	"bufio"
	"math/rand"
	"os"
)

func main() {
	flag, _ := os.ReadFile("flag.txt")
	reader := bufio.NewReader(os.Stdin)
	for i := 0; ; i++ {
		println(int64(rand.Uint32()) + int64(flag[i%len(flag)]))
		reader.ReadString('\n')
	}
}
