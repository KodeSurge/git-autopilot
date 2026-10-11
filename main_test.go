package main

import (
	"io"
	"os"
	"strings"
	"testing"
)

// captureStdout captures the output written to stdout by fn.
func captureStdout(t *testing.T, fn func()) string {
	t.Helper()
	old := os.Stdout
	r, w, err := os.Pipe()
	if err != nil {
		t.Fatalf("failed to create pipe: %v", err)
	}
	os.Stdout = w
	defer func() { os.Stdout = old }()

	fn()

	if err := w.Close(); err != nil {
		t.Fatalf("failed to close write pipe: %v", err)
	}
	var buf strings.Builder
	if _, err := io.Copy(&buf, r); err != nil {
		t.Fatalf("failed to read stdout: %v", err)
	}
	if err := r.Close(); err != nil {
		t.Fatalf("failed to close read pipe: %v", err)
	}
	return buf.String()
}

func TestPrintVersionOutput(t *testing.T) {
	got := captureStdout(t, printVersion)
	want := "xssh version 0.1.0\n"
	if got != want {
		t.Errorf("printVersion() = %q, want %q", got, want)
	}
}

func TestPrintUsageContainsExpectedText(t *testing.T) {
	got := captureStdout(t, printUsage)
	for _, substr := range []string{"Usage: xssh", "--help", "--version"} {
		if !strings.Contains(got, substr) {
			t.Errorf("printUsage() output missing %q", substr)
		}
	}
}

func TestVersionNotEmpty(t *testing.T) {
	if version == "" {
		t.Fatal("version variable must not be empty")
	}
}
