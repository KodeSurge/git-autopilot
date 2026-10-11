# Project Constraints

## Build Artifact Layout

The CI/CD pipeline expects the following build artifact layout after compilation:

```
build/bin/
├── xssh           (or xssh.exe on Windows)
└── resources/     (copied from repo-root resources/ directory)
```

### Rules

1. **Binary output path**: The `go build` command MUST use `-o build/bin/<binary_name>` to place the binary at the expected location. The binary name must match the platform convention:
   - `xssh` for Linux/macOS
   - `xssh.exe` for Windows

2. **Resources directory**: The `resources/` directory MUST be copied into `build/bin/resources/` before packaging. The CI pipeline packages both the binary and `resources/` into the release archive.

3. **Packaging**: Each platform produces a zip archive:
   - `xssh-linux-amd64.zip` containing `xssh` + `resources/`
   - `xssh-windows-amd64.zip` containing `xssh.exe` + `resources/`
   - `xssh-darwin-amd64.zip` containing `xssh` + `resources/`

4. **Verification**: Before packaging, the CI MUST verify that both the binary and `resources/` directory exist in `build/bin/`.
