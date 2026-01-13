list_of_files=(
    "src/__init__.py"
    "src/helper.py"
    "src/prompt.py"
    "research/trials.ipynb"
    "app.py"
    "setup.py"
    "requirements.txt"
    ".env"
)

for filepath in "${list_of_files[@]}"; do
    # Get the directory name using parameter expansion
    dir_name="${filepath%/*}"
    
    # Only run mkdir if the file is in a subdirectory
    if [[ "$dir_name" != "$filepath" ]]; then
        mkdir -p "$dir_name"
    fi

    # Avoid updating timestamps of existing files
    if [[ ! -f "$filepath" ]]; then
        touch "$filepath"
        echo "Created: $filepath"
    else
        echo "Skipped: $filepath (already exists)"
    fi
done

echo "Project structure initialization complete."