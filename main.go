// Package main implements xssh, a minimal SSH configuration management tool.
package main

import (
	"fmt"
	"os"
)

var version = "0.1.0"

// printVersion prints the current version to stdout.
func printVersion() {
	fmt.Printf("xssh version %s\n", version)
}

func main() {
	if len(os.Args) > 1 {
		switch os.Args[1] {
		case "--version", "-v":
			printVersion()
			return
		case "--help", "-h":
			printUsage()
			return
		default:
			fmt.Fprintf(os.Stderr, "unknown command: %s\n", os.Args[1])
			printUsage()
			os.Exit(1)
		}
	}
	printVersion()
}

// printUsage prints usage information to stdout.
func printUsage() {
	const usage = `Usage: xssh [flags]

Flags:
  -h, --help       Show this help message
  -v, --version    Print version information
`
	fmt.Print(usage)
}
