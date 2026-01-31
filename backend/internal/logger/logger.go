package logger

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
	"time"

	ctxkey "github.com/wilrustiandy/wealthwise/backend/internal/context"
)

type Level int

const (
	DEBUG Level = iota
	INFO
	WARN
	ERROR
	FATAL
)

var levelNames = []string{"DEBUG", "INFO", "WARN", "ERROR", "FATAL"}

type Logger struct {
	level Level
	mu    sync.Mutex
}

func New(level Level) *Logger {
	return &Logger{level: level}
}

// Global instance for convenience
var logger *Logger

func Init(level Level) *Logger {
	logger = New(level)
	return logger
}

func GetLogger() *Logger {
	if logger == nil {
		Init(INFO)
	}
	return logger
}

func (l *Logger) Debug(format string, messages ...any) {
	l.log(DEBUG, format, messages...)
}

func (l *Logger) Info(format string, messages ...any) {
	l.log(INFO, format, messages...)
}

func (l *Logger) InfoCtx(ctx context.Context, format string, messages ...any) {
	l.logCtx(ctx, INFO, format, messages...)
}

func (l *Logger) Warn(format string, messages ...any) {
	l.log(WARN, format, messages...)
}

func (l *Logger) WarnCtx(ctx context.Context, format string, messages ...any) {
	l.logCtx(ctx, WARN, format, messages...)
}

func (l *Logger) Error(format string, messages ...any) {
	l.log(ERROR, format, messages...)
}

func (l *Logger) ErrorCtx(ctx context.Context, format string, messages ...any) {
	l.logCtx(ctx, ERROR, format, messages...)
}

func (l *Logger) Fatal(format string, messages ...any) {
	l.log(FATAL, format, messages...)
	os.Exit(1)
}

func (l *Logger) FatalCtx(ctx context.Context, format string, messages ...any) {
	l.logCtx(ctx, FATAL, format, messages...)
}

func (l *Logger) log(level Level, format string, messages ...any) {
	if level < l.level {
		return
	}
	l.internalLog(level, "", format, messages...)
}

func (l *Logger) logCtx(ctx context.Context, level Level, format string, messages ...any) {
	if level < l.level {
		return
	}

	var contextKeyValues []string

	for _, key := range ctxkey.ContextKeys {
		if value, ok := ctx.Value(key).(string); ok && value != "" {
			contextKeyValues = append(contextKeyValues, fmt.Sprintf("%s:%s", key, value))
		}
	}

	contextString := ""

	if len(contextKeyValues) > 0 {
		contextString = strings.Join(contextKeyValues, " ")
	}

	l.internalLog(level, contextString, format, messages...)
}

func (l *Logger) internalLog(level Level, context string, format string, messages ...any) {
	if level < l.level {
		return
	}

	message := fmt.Sprintf(format, messages...)

	timestamp := time.Now().UTC().Format("2006-01-02T15:04:05Z")

	_, file, line, ok := runtime.Caller(2)
	caller := "unknown"
	if ok {
		caller = fmt.Sprintf("%s:%d", filepath.Base(file), line)
	}

	output := fmt.Sprintf("[%s] %s %s %s - Message: %s\n", levelNames[level], timestamp, caller, context, message)

	l.mu.Lock()
	defer l.mu.Unlock()
	if level >= ERROR {
		os.Stderr.WriteString(output)
	} else {
		os.Stdout.WriteString(output)
	}
}
