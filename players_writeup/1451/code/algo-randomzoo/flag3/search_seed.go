package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"runtime"
	"sync"
	"time"
)

// 每个 worker 的任务
func searchSeeds(start, end, targetNum uint32, wg *sync.WaitGroup, writer *bufio.Writer, workerID int) {
	defer wg.Done()
	curIndex := uint32(0)
	length := end - start + 1

	for seed := start; seed < end; seed++ {
		rng := rand.New(rand.NewSource(int64(seed)))
		randNum := rng.Uint32()
		if randNum+102 == targetNum {
			_, err := writer.WriteString(fmt.Sprintf("Matched seed: %d (found by worker %d)\n", seed, workerID))
			if err != nil {
				fmt.Println("写入文件时出错:", err)
				return
			}
			fmt.Printf("Found matching seed: %d by worker %d\n", seed, workerID)
		}

		curIndex = seed - start + 1

		if curIndex%10000000 == 0 {
			currentTime := time.Now().Add(8 * time.Hour).Format("2006-01-02 15:04:05")
			fmt.Printf("Worker %d progress: %d/%d, Current time: %s\n", workerID, curIndex, length, currentTime)
		}
	}
}

func main() {
	var targetNum uint32 = 3343086319
	totalSeeds := uint32(0xFFFFFFFF)

	numWorkers := 16
	runtime.GOMAXPROCS(numWorkers)
	fmt.Printf("Using %d cores for parallel processing\n", numWorkers)

	// 打开文件并使用缓冲写入
	file, err := os.Create("matched_seeds.txt")
	if err != nil {
		fmt.Println("无法创建文件:", err)
		return
	}
	defer file.Close()
	writer := bufio.NewWriter(file)
	defer writer.Flush()

	// 定义同步等待组
	var wg sync.WaitGroup

	// 每个 worker 分配的种子范围
	seedsPerWorker := totalSeeds / uint32(numWorkers)

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		start := uint32(i) * seedsPerWorker
		var end uint32
		if i == numWorkers-1 {
			end = totalSeeds // 最后一个 worker 处理到最大值
		} else {
			end = start + seedsPerWorker
		}
		// 启动 goroutine 进行并行搜索
		go searchSeeds(start, end, targetNum, &wg, writer, i)
	}

	// 等待所有的 goroutine 完成
	wg.Wait()

	fmt.Println("Seed search completed.")
}
