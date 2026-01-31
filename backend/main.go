package main

import (
	"context"
	"errors"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/wilrustiandy/wealthwise/backend/config"
	"github.com/wilrustiandy/wealthwise/backend/internal/logger"
)

func main() {
	log := logger.Init()

	cfg, err := config.Load()
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			log.Warn("Config file not found!! Apply default config")
		} else {
			log.Fatal("Failed to load config: %v", err)
		}
	}

	log.SetLevel(logger.ParseLevel(cfg.Log.Level))

	host := cfg.Address + ":" + cfg.Port

	server := &http.Server{
		Addr:    host,
		Handler: nil,
	}

	shutdown := make(chan os.Signal, 1)
	signal.Notify(shutdown, os.Interrupt, syscall.SIGTERM)

	log.Info("WealthWise Backend starting on %s", host)
	go func() {
		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Fatal("Server failed to start: %v", err)
		}
	}()

	sig := <-shutdown
	log.Warn("Received signal: %v. Shutting down gracefully...", sig)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Error("Graceful shutdown failed: %v", err)
		server.Close()
	}

	log.Info("WealthWise Backend stopped!!")
}
