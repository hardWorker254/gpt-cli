PREFIX := /usr/local/bin
INSTALL_DIR := $(PREFIX)/gpt-clil
CXX := g++
CXXFLAGS := -O2 -Wall

SRC_CPP := gpt-cli.cpp
TARGET := gpt-cli
PY_FILES := main.py promt.py

.PHONY: all install clean

all: $(TARGET)

$(TARGET): $(SRC_CPP)
	$(CXX) $(CXXFLAGS) $< -o $@

install: all
	mkdir -p $(INSTALL_DIR)
	cp $(PY_FILES) $(INSTALL_DIR)/
	cp $(TARGET) $(PREFIX)/

clean:
	rm -f $(TARGET)
