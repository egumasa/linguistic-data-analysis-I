#!/bin/bash
# convert-to-jekyll.sh
# Converts Quarto markdown files to Jekyll-compatible format

# Create Jekyll-compatible versions
mkdir -p jekyll-output

for file in $(find . -name "*.md" -o -name "*.qmd" | grep -v jekyll-output); do
    # Get relative path
    rel_path=${file#./}
    
    # Create output directory
    mkdir -p "jekyll-output/$(dirname "$rel_path")"
    
    # Convert the file
    output_file="jekyll-output/${rel_path%.qmd}.md"
    
    # Process the file
    awk '
    BEGIN { in_yaml = 0; print_yaml = 1 }
    /^---$/ { 
        if (in_yaml == 0) { 
            in_yaml = 1
            print "---"
            print "layout: default"
            next
        } else {
            in_yaml = 0
            print "---"
            print_yaml = 0
            next
        }
    }
    in_yaml {
        # Convert Quarto YAML to Jekyll YAML
        if ($1 == "subtitle:") {
            sub(/subtitle:/, "description:", $0)
        }
        # Skip toc line for Jekyll
        if ($1 == "toc:") next
        
        print $0
        next
    }
    # Convert Quarto callouts to Jekyll
    /^:::.*{\.callout-.*}/ {
        type = $0
        sub(/.*callout-/, "", type)
        sub(/}.*/, "", type)
        print "> **" toupper(substr(type, 1, 1)) substr(type, 2) "**"
        next
    }
    /^:::$/ && !in_yaml { next }  # Skip closing :::
    
    # Regular content
    { print }
    ' "$file" > "$output_file"
done

echo "Jekyll-compatible files created in jekyll-output/"
