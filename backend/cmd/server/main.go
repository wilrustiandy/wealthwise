package main

import (
	"os"

	"github.com/wilrustiandy/wealthwise/backend/internal/app"
)

func main() {
	if err := app.Run(); err != nil {
		os.Exit(1)
	}
}
