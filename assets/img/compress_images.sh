#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install it first."
    exit 1
fi

# Check for minimum arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_directory> <file_extension> [ffmpeg_args...]"
    echo ""
    echo "Examples:"
    echo "  $0 ./images jpg -vf \"scale=1080:-1\" -q:v 30"
    echo "  $0 ./photos png -vf \"scale=1080:-1\" -compression_level 9"
    echo "  $0 . jpeg -vf \"scale=720:-1\" -q:v 25"
    exit 1
fi

INPUT_DIR="$1"
EXT="$2"
shift 2
FFMPEG_ARGS="$@"

# Create output directory
OUTPUT_DIR="${INPUT_DIR}/compressed"
mkdir -p "$OUTPUT_DIR"

# Counters
count=0
total_original_size=0
total_compressed_size=0

# Function to get file size in bytes
get_size() {
    stat -f%z "$1" 2>/dev/null || stat -c%s "$1" 2>/dev/null
}

# Function to convert bytes to human readable
human_readable() {
    local bytes=$1
    if [ $bytes -lt 1024 ]; then
        echo "${bytes}B"
    elif [ $bytes -lt 1048576 ]; then
        echo "$(awk "BEGIN {printf \"%.2f\", $bytes/1024}")KB"
    elif [ $bytes -lt 1073741824 ]; then
        echo "$(awk "BEGIN {printf \"%.2f\", $bytes/1048576}")MB"
    else
        echo "$(awk "BEGIN {printf \"%.2f\", $bytes/1073741824}")GB"
    fi
}

# Process all files with the given extension
for file in "$INPUT_DIR"/*.${EXT} "$INPUT_DIR"/*.${EXT^^}; do
    # Skip if no matching files found
    [ -e "$file" ] || continue
    
    # Get filename without path
    filename=$(basename "$file")
    
    # Output file path
    output="$OUTPUT_DIR/$filename"
    
    # Get original size
    original_size=$(get_size "$file")
    
    echo "Processing: $filename ($(human_readable $original_size))"
    
    # Run ffmpeg with custom args
    ffmpeg -i "$file" $FFMPEG_ARGS "$output" -y -loglevel error
    
    if [ $? -eq 0 ]; then
        compressed_size=$(get_size "$output")
        savings=$((original_size - compressed_size))
        percent=$(awk "BEGIN {printf \"%.1f\", ($savings*100.0/$original_size)}")
        
        echo "✓ Processed: $filename → $(human_readable $compressed_size) (${percent}% reduction)"
        
        total_original_size=$((total_original_size + original_size))
        total_compressed_size=$((total_compressed_size + compressed_size))
        ((count++))
    else
        echo "✗ Failed: $filename"
    fi
done

echo ""
echo "================================"
echo "Done! Processed $count images."
echo "Original total:    $(human_readable $total_original_size)"
echo "Compressed total:  $(human_readable $total_compressed_size)"
echo "Total saved:       $(human_readable $((total_original_size - total_compressed_size)))"
if [ $total_original_size -gt 0 ]; then
    overall_percent=$(awk "BEGIN {printf \"%.1f\", ((($total_original_size - $total_compressed_size)*100.0/$total_original_size))}")
    echo "Overall reduction: ${overall_percent}%"
fi
echo "================================"
echo "Compressed images saved to: $OUTPUT_DIR"