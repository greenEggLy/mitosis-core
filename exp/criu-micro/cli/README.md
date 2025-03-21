# Quick Restore Usage

## Prepearation

1. A runnable base image with criu and python
2. Dump to $ROOTFS_ABS_PATH


## Run cli tools
```bash
python cli.py checkpoint --rootfs_path <rootfs_path> [--function <function_name>] [--payload <payload>] [--function_file <function_file>]
python cli.py restore --number <number> --rootfs_path <rootfs_path> [--parallel] [--name <name>] 
```

NOTE: Checkpoint should be triggered when a function file is uploaded