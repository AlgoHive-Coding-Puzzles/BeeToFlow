# BeeToFlow

## Overview

BeeToFlow is a Dockerized Python utility that is aim to compile a set of opened puzzle folders into `.alghive` files.
This tool exists as a convenient way to use the [`Hivecraft`](https://github.com/AlgoHive-Coding-Puzzles/HiveCraft) tool to compile the puzzles. Includes this tool in your GitHub actions workflow to automatically compile your opened puzzles into `.alghive` files.

## Usage

Add the following to your GitHub actions workflow:

```yaml
- name: Use Compile Puzzles Action
  uses: AlgoHive-Coding-Puzzles/BeeToFlow@v1.0.0
  with:
    target-directories: "B1, B2"
```

Example of a GitHub Actions workflow file that uses the BeeToFlow action to compile puzzles:

```yaml
name: Compile Puzzles
on: [push]
jobs:
  compile:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Use Compile Puzzles Action
        uses: AlgoHive-Coding-Puzzles/BeeToFlow@v1.0.0
        with:
          target-directories: "Catalog1, Catalog2"

      - name: Upload Compiled Files as Artifactories
        uses: actions/upload-artifact@v2
        with:
          name: compiled-puzzles
          path: |
            out/Catalog1.tar
            out/Catalog2.tar
          retention-days: 7
```

## Parameters

| Parameter            | Description                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| `target-directories` | A comma-separated list of directories to compile. Each directory should contain a set of opened puzzles. |
| `output-directory`   | The directory where the compiled `.alghive` files will be saved. Default is `out`.                       |
| `hivecraft-version`  | The version of Hivecraft to use. Default is `latest`.                                                    |

## Behavior

- The action will compile the puzzles in the specified directories and save the `.alghive` files in the `out` directory.
- If the `target-directories` parameter is not provided, the action will compile all opened puzzle folders in the repository.
- The action will automatically create the `out` directory if it does not exist.
- The action will use the specified version of Hivecraft to compile the puzzles. If no version is specified, it will use the latest version.
- The action will create a tar file for each directory containing the compiled `.alghive` files.
- If the action fails, it will return an error message indicating the reason for the failure.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
