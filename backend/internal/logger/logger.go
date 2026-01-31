package logger

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"sync"
	"time"
)

type Level int

const (
	DEBUG Level = iota
	INFO
	WARN
	ERROR
)

var levelNames = []string{"DEBUG", "INFO", "WARN", "ERROR"}

type Logger struct {
	level Level
	mu    sync.Mutex
}

func New(level Level) *Logger {
	return &Logger{level: level}
}

// Global instance for convenience
var logger *Logger

func Init(level Level) {
	logger = New(level)
}

func Debug(msg string) {
	logger.log(DEBUG, msg)
}

func Info(msg string) {
	logger.log(INFO, msg)
}

func Warn(msg string) {
	logger.log(WARN, msg)
}

func Error(msg string) {
	logger.log(ERROR, msg)
}

func (l *Logger) log(level Level, msg string) {
	if level < l.level {
		return
	}

	timestamp := time.Now().UTC().Format("2006-01-02T15:04:05Z")

	_, file, line, ok := runtime.Caller(2)
	caller := "unknown"
	if ok {
		caller = fmt.Sprintf("%s:%d", filepath.Base(file), line)
	}

	output := fmt.Sprintf("[%s] %s %s - %s\n", levelNames[level], timestamp, caller, msg)

	l.mu.Lock()
	defer l.mu.Unlock()
	os.Stdout.WriteString(output)
}
