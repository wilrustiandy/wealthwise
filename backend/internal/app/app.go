package app

import (
	"context"
	"errors"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/wilrustiandy/wealthwise/backend/config"
	"github.com/wilrustiandy/wealthwise/backend/pkg/logger"
)

func Run() error {
	log := logger.Init()

	cfg, err := config.Load()
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		log.Error("Failed to load config: %v", err)
		return err
	}
	if errors.Is(err, os.ErrNotExist) {
		log.Warn("Config file not found!! Applying defaults.")
	}

	log.SetLevel(logger.ParseLevel(cfg.Log.Level))

	host := cfg.App.Address + ":" + cfg.App.Port
	server := &http.Server{
		Addr:    host,
		Handler: nil,
	}

	shutdown := make(chan os.Signal, 1)
	signal.Notify(shutdown, os.Interrupt, syscall.SIGTERM)
	serverErrors := make(chan error, 1)

	log.Info("WealthWise Backend starting on %s", host)
	go func() {
		serverErrors <- server.ListenAndServe()
	}()

	select {
	case err := <-serverErrors:
		log.Error("Server failed to start: %v", err)
		return err

	case sig := <-shutdown:
		log.Warn("Received signal: %v. Shutting down gracefully...", sig)

		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		if err := server.Shutdown(ctx); err != nil {
			log.Error("Graceful shutdown failed: %v", err)
			server.Close()
			return err
		}
	}

	log.Info("WealthWise Backend stopped!!")
	return nil
}
