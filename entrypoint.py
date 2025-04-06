#!/usr/bin/env python3
import os
import sys
import subprocess
import tarfile
import shutil
import importlib.util
import site
import traceback  # Add traceback module for stack traces

def install_hivecraft(version):
    """Install Hivecraft from GitHub"""
    print(f"🐝 Installing Hivecraft version: {version}")
    
    # if version.lower() == "latest":
    #     cmd = ["pip", "install", "git+https://github.com/AlgoHive-Coding-Puzzles/HiveCraft.git"]
    # else:
    #     cmd = ["pip", "install", f"git+https://github.com/AlgoHive-Coding-Puzzles/HiveCraft.git@{version}"]
    
    hivecraft_p = "hivecraft"
    if version and version.lower() != "latest":
        hivecraft_p += f"=={version}"
    
    # Install the latest version of Hivecraft from PyPI
    cmd = ["pip", "install", hivecraft_p]
    
    subprocess.run(cmd, check=True)
    print("✅ Hivecraft installed successfully")

def compile_puzzles(directory, output_dir):
    """Compile puzzles in the specified directory"""
    from hivecraft.alghive import Alghive
    
    print(f"🔨 Processing puzzles in {directory}...")
    
    successful = []
    failed = []
    
    for puzzle in os.listdir(directory):
        puzzle_path = os.path.join(directory, puzzle)
        
        if not os.path.isdir(puzzle_path):
            continue
        
        try:
            print(f"  📝 Compiling puzzle: {puzzle}")
            alghive = Alghive(puzzle_path)
            
            # Check if the puzzle respects the constraints
            alghive.check_integrity()
            
            # Run tests to ensure the puzzle is working correctly
            alghive.run_tests(100)
            
            # Zip the folder to create the .alghive file
            alghive.zip_folder()
            
            # Move the .alghive file to the output directory
            source_file = f"{puzzle}{Alghive.EXTENSION}"
            if os.path.exists(source_file):
                dest_file = os.path.join(output_dir, source_file)
                shutil.move(source_file, dest_file)
                successful.append(puzzle)
                print(f"  ✅ Successfully compiled {puzzle}")
            else:
                failed.append(f"{puzzle}: alghive file not created")
                print(f"  ❌ Failed to create alghive file for {puzzle}")
                
        except Exception as e:
            stack_trace = traceback.format_exc()
            failed.append(f"{puzzle}: {str(e)}\n{stack_trace}")
            print(f"  ❌ Failed to compile {puzzle}: {str(e)}")
            print(f"    Stack trace:\n{stack_trace}")
    
    return successful, failed

def create_tar_archive(output_dir, directory):
    """Create a tar archive of the compiled puzzles"""
    from hivecraft.alghive import Alghive
    tar_filename = os.path.join(output_dir, f"{os.path.basename(directory)}.tar")
    dir_output = os.path.join(output_dir, directory)
    
    print(f"📦 Creating tar archive: {tar_filename}")
    
    with tarfile.open(tar_filename, "w") as tar:
        for file in os.listdir(dir_output):
            file_path = os.path.join(dir_output, file)
            if file.endswith(Alghive.EXTENSION) and os.path.isfile(file_path):
                tar.add(file_path, arcname=os.path.basename(file_path))
    
    print(f"✅ Tar archive created successfully: {tar_filename}")

def main():
    # Get action inputs
    if len(sys.argv) < 2:
        print("❌ Error: No target directories provided")
        sys.exit(1)
    
    target_dirs = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "out"
    hivecraft_version = sys.argv[3] if len(sys.argv) > 3 else "latest"
    
    # Install Hivecraft
    install_hivecraft(hivecraft_version)
    
    # Ensure we can import Hivecraft components
    import hivecraft
    from hivecraft.alghive import Alghive
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert target directories to list
    directories = [dir.strip() for dir in target_dirs.split(',')]
    
    print("\n📂 Directories to process:")
    all_successful = {}
    all_failed = {}
    
    for directory in directories:
        directory = directory.strip()
        if os.path.isdir(directory):
            print(f"✅ Processing {directory}")
            
            # Create a specific output directory for this target directory
            dir_output = os.path.join(output_dir, directory)
            os.makedirs(dir_output, exist_ok=True)
            
            # Compile puzzles
            successful, failed = compile_puzzles(directory, dir_output)
            
            # Store results
            all_successful[directory] = successful
            all_failed[directory] = failed
            
            # Create tar archive
            if successful:
                create_tar_archive(output_dir, directory)
        else:
            print(f"⚠️ Directory '{directory}' does not exist")
            all_failed[directory] = ["Directory not found"]
    
    # Print summary
    print("\n📊 Compilation Summary:")
    for directory in directories:
        print(f"\n📁 {directory}:")
        if directory in all_successful and all_successful[directory]:
            print(f"  ✅ Successfully compiled {len(all_successful[directory])} puzzles")
            for puzzle in all_successful[directory]:
                print(f"    - {puzzle}")
        
        if directory in all_failed and all_failed[directory]:
            print(f"  ❌ Failed to compile {len(all_failed[directory])} puzzles")
            for failure in all_failed[directory]:
                print(f"    - {failure}")
    
    # Exit with error if any compilation failed
    if any(failed for failed in all_failed.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()
