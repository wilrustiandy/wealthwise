package main

import (
	"net/http"

	"github.com/wilrustiandy/wealthwise/backend/internal/logger"
)

func main() {
	log := logger.Init(logger.INFO)

	host := "localhost:8080"

	log.Info("WealthWise Backend starting on %s", host)
	if err := http.ListenAndServe(host, nil); err != nil {
		log.Fatal("Server failed to start: %v", err)
	}
	log.Info("WealthWise Backend started!!")
}
