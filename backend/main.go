package main

import (
	"log/slog"
	"net/http"
	"os"

	"github.com/wilrustiandy/wealthwise/internal/logger"
)

func main() {
	logger.InitLogger()

	addr := "localhost"
	port := "8080"

	slog.Info("WealthWise Backend starting on %s:%s", addr, port)
	if err := http.ListenAndServe(addr, nil); err != nil {
		logger.Fatal("Server failed to start: %v", err)
		os.Exit(1)
	}
	slog.Info("WealthWise Backend started!!")
}
