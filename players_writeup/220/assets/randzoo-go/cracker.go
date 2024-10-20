package main

import (
	"bufio"
	"flag"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"sync"
)

const knownResultsFile = "randzoo-input.txt"

// loadKnownResults loads the known results from the file into a slice of integers
func loadKnownResults(filename string) ([]uint32, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var results []uint32
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		result, err := strconv.Atoi(scanner.Text())
		if err != nil {
			return nil, err
		}
		results = append(results, uint32(result))
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return results, nil
}

// reseed reseeds the random number generator with the given seed and generates a number
func reseed(seed int64) *rand.Rand {
	rng := rand.New(rand.NewSource(seed)) // Create a new PRNG with its own seed
	return rng                            // Assume known results are in the range 0-999
}

// worker function that processes a seed range in a separate goroutine
func worker(startSeed, endSeed int64, knownResults []uint32, wg *sync.WaitGroup, resultsChan chan string) {
	defer wg.Done()
	for seed := startSeed; seed <= endSeed; seed++ {
		rng := reseed(seed)
		if seed%100000 == 0 {
			fmt.Printf("Seed: %d\n", seed)
		}
		match := true
		for _, known := range knownResults {
			if rng.Uint32() != known {
				match = false
				break
			}
		}
		if match {
			resultsChan <- fmt.Sprintf("Match found! Seed: %d\n", seed)
		}
	}
}

func main() {
	// Command-line flags for seed range
	startSeed := flag.Int64("start", 1, "Start of seed range")
	endSeed := flag.Int64("end", (2<<31)-1, "End of seed range")
	numWorkers := flag.Int("workers", 16, "Number of goroutines")
	flag.Parse()

	// Load known results from file
	knownResults, err := loadKnownResults(knownResultsFile)
	if err != nil {
		fmt.Println("Error loading known results:", err)
		return
	}

	// Channel for passing results from workers
	resultsChan := make(chan string)

	// WaitGroup to wait for all goroutines to finish
	var wg sync.WaitGroup

	// Calculate the seed range for each worker
	totalSeeds := *endSeed - *startSeed + 1
	seedsPerWorker := totalSeeds / int64(*numWorkers)

	fmt.Println("Starting workers...")

	// Launch workers (goroutines)
	for i := 0; i < *numWorkers; i++ {
		start := *startSeed + int64(i)*seedsPerWorker
		end := start + seedsPerWorker - 1
		if i == *numWorkers-1 { // Ensure the last worker takes the remaining seeds
			end = *endSeed
		}
		wg.Add(1)
		go worker(start, end, knownResults, &wg, resultsChan)
	}

	// Goroutine to close resultsChan once all workers are done
	go func() {
		wg.Wait()
		close(resultsChan)
	}()

	// Output results
	for result := range resultsChan {
		fmt.Print(result)
	}

	fmt.Println("All workers finished.")
}
