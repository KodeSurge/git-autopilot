"""
Unit tests for CI/CD workflow configuration and repo structure.

Verifies that:
1. The CI/CD workflow file exists and is valid YAML.
2. The workflow includes a resources copy step.
3. The workflow uses explicit -o flag for build output.
4. The resources/ directory exists in the repo.
5. The Go source files exist and are well-formed.
"""

import os
import unittest

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW_PATH = os.path.join(REPO_ROOT, ".github", "workflows", "build.yml")
RESOURCES_DIR = os.path.join(REPO_ROOT, "resources")
GO_MOD = os.path.join(REPO_ROOT, "go.mod")
MAIN_GO = os.path.join(REPO_ROOT, "main.go")


class TestWorkflowFileExists(unittest.TestCase):
    """Verify the CI/CD workflow file exists and is valid."""

    def test_workflow_file_exists(self):
        self.assertTrue(
            os.path.isfile(WORKFLOW_PATH),
            f"CI workflow file not found at {WORKFLOW_PATH}"
        )

    def test_workflow_is_valid_yaml(self):
        with open(WORKFLOW_PATH) as f:
            data = yaml.safe_load(f)
        self.assertIsNotNone(data, "Workflow file is empty or invalid YAML")

    def test_workflow_has_jobs(self):
        with open(WORKFLOW_PATH) as f:
            data = yaml.safe_load(f)
        self.assertIn("jobs", data, "Workflow missing 'jobs' key")

    def test_workflow_has_build_job(self):
        with open(WORKFLOW_PATH) as f:
            data = yaml.safe_load(f)
        self.assertIn("build", data["jobs"], "Workflow missing 'build' job")


class TestWorkflowBuildConfig(unittest.TestCase):
    """Verify the build step in the workflow is correctly configured."""

    def _get_build_steps(self):
        with open(WORKFLOW_PATH) as f:
            data = yaml.safe_load(f)
        job = data["jobs"]["build"]
        return job["steps"]

    def test_build_step_exists(self):
        steps = self._get_build_steps()
        build_steps = [s for s in steps if "Build" in str(s.get("name", ""))]
        self.assertGreater(
            len(build_steps), 0,
            "No build step found in workflow"
        )

    def test_build_uses_explicit_output_flag(self):
        """The go build command must use -o to specify output path explicitly."""
        with open(WORKFLOW_PATH) as f:
            content = f.read()
        # Check that -o build/bin/ pattern is present
        self.assertIn(
            "-o build/bin/",
            content,
            "Build step must use '-o build/bin/' to specify output path explicitly"
        )

    def test_resources_copy_step_exists(self):
        """The workflow must copy resources into build/bin before packaging."""
        with open(WORKFLOW_PATH) as f:
            content = f.read()
        # Check that resources are copied to build/bin
        self.assertIn(
            "cp -r resources build/bin/resources",
            content,
            "Workflow must include 'cp -r resources build/bin/resources'"
        )

    def test_verify_step_exists(self):
        """The workflow must verify build artifacts before packaging."""
        steps = self._get_build_steps()
        verify_steps = [s for s in steps if "Verify" in str(s.get("name", ""))]
        self.assertGreater(
            len(verify_steps), 0,
            "No verification step found in workflow"
        )

    def test_matrix_covers_all_platforms(self):
        """The build matrix must cover linux, windows, and darwin."""
        with open(WORKFLOW_PATH) as f:
            data = yaml.safe_load(f)
        job = data["jobs"]["build"]
        matrix = job["strategy"]["matrix"]
        include = matrix.get("include", [])
        goos_values = [entry.get("goos") for entry in include]
        self.assertIn("linux", goos_values, "Matrix must include linux")
        self.assertIn("windows", goos_values, "Matrix must include windows")
        self.assertIn("darwin", goos_values, "Matrix must include darwin")

    def test_windows_binary_has_exe_extension(self):
        """Windows binary must have .exe extension."""
        with open(WORKFLOW_PATH) as f:
            data = yaml.safe_load(f)
        job = data["jobs"]["build"]
        matrix = job["strategy"]["matrix"]
        include = matrix.get("include", [])
        for entry in include:
            if entry.get("goos") == "windows":
                self.assertTrue(
                    entry.get("binary", "").endswith(".exe"),
                    "Windows binary must have .exe extension"
                )


class TestResourcesDirectory(unittest.TestCase):
    """Verify the resources directory exists in the repo."""

    def test_resources_directory_exists(self):
        self.assertTrue(
            os.path.isdir(RESOURCES_DIR),
            f"resources/ directory not found at {RESOURCES_DIR}"
        )

    def test_resources_not_in_gitignore(self):
        gitignore_path = os.path.join(REPO_ROOT, ".gitignore")
        if os.path.isfile(gitignore_path):
            with open(gitignore_path) as f:
                content = f.read()
            lines = [line.strip() for line in content.splitlines()]
            # Check that resources is not excluded
            self.assertNotIn("resources", lines,
                             "resources/ should not be in .gitignore")
            self.assertNotIn("resources/", lines,
                             "resources/ should not be in .gitignore")


class TestGoSourceFiles(unittest.TestCase):
    """Verify Go source files exist and are well-formed."""

    def test_go_mod_exists(self):
        self.assertTrue(
            os.path.isfile(GO_MOD),
            "go.mod not found"
        )

    def test_go_mod_has_module(self):
        with open(GO_MOD) as f:
            content = f.read()
        self.assertIn("module", content, "go.mod must declare a module")

    def test_main_go_exists(self):
        self.assertTrue(
            os.path.isfile(MAIN_GO),
            "main.go not found"
        )

    def test_main_go_has_package_declaration(self):
        with open(MAIN_GO) as f:
            content = f.read()
        self.assertIn("package main", content,
                      "main.go must declare 'package main'")

    def test_main_go_has_main_function(self):
        with open(MAIN_GO) as f:
            content = f.read()
        self.assertIn("func main()", content,
                      "main.go must define func main()")


if __name__ == "__main__":
    unittest.main()
