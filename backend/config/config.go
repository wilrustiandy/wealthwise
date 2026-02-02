package config

import (
	"errors"
	"os"

	yaml "gopkg.in/yaml.v3"
)

type AppConfig struct {
	Address string `yaml:"address"`
	Port    string `yaml:"port"`
}

type LogConfig struct {
	Level string `yaml:"level"`
}

type Config struct {
	App AppConfig `yaml:"app"`
	Log LogConfig `yaml:"log"`
}

const configFileName = "config.yaml"

func Load() (*Config, error) {
	var cfg Config

	if err := yaml.Unmarshal([]byte(defaultConfig), &cfg); err != nil {
		return nil, err
	}

	if _, err := os.Stat(configFileName); errors.Is(err, os.ErrNotExist) {
		return &cfg, err
	}

	fileData, err := os.ReadFile(configFileName)
	if err != nil {
		return nil, err
	}

	if err := yaml.Unmarshal(fileData, &cfg); err != nil {
		return nil, err
	}

	return &cfg, nil
}
