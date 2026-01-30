package main

import (
	"log"
	"net/http"
	"os"
)

func main() {
	// Initialize Modules
	// - Account
	// - Stocks
	// - Crypto

	// Setup Routes
	// - /account
	// - /crypto
	// - /stocks
	// - /health
	// - /metrics

	addr := "localhost"
	port := "8080"

	log.Printf("WealthWise Backend starting on %s:%s\n", addr, port)
	if err := http.ListenAndServe(addr, nil); err != nil {
		log.Fatalf("Server failed to start: %v", err)
		os.Exit(1)
	}
	log.Printf("WealthWise Backend started!!\n")
}
