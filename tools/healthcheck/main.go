package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
)

type HealthResponse struct {
	Status    string `json:"status"`
	Timestamp string `json:"timestamp"`
}

func checkEndpoint(url string) (bool, error) {
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	var health HealthResponse
	if err := json.NewDecoder(resp.Body).Decode(&health); err != nil {
		return false, err
	}
	return health.Status == "ok", nil
}

func main() {
	apiURL := "http://localhost:8000/health"
	if len(os.Args) > 1 {
		apiURL = os.Args[1]
	}

	fmt.Printf("Checking %s...
", apiURL)
	ok, err := checkEndpoint(apiURL)
	if err != nil {
		fmt.Printf("FAIL: %v
", err)
		os.Exit(1)
	}
	if ok {
		fmt.Println("OK: service is healthy")
	} else {
		fmt.Println("WARN: service returned unhealthy status")
		os.Exit(1)
	}
}
