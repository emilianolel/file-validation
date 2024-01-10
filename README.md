# File Validation 📁✅

This Python script, `FileValidator`, is designed to validate files based on metadata. It ensures that the file structure conforms to the specified rules.

## Usage 🚀

To use the script, follow these steps:

1. Clone the repository:

   ```bash 
    git clone https://github.com/your-username/file-validation.git
    ```

2. Navigate to the repository directory:

   ```bash 
    cd src/
    ```

3. Run the script:
    
   ```bash 
    python3 file-validator.py
    ```

## Features 🌟

- Validates file existence and metadata consistency.
- Checks column names, order, and structure.


## How to Use 🤔

1. **Import the `FileValidator` class:**

    ```python
    from file_validator import FileValidator
    ```

2. **Instantiate the `FileValidator` class:**

    ```python
    # Provide the paths to the data file and metadata file
    data_file_path = 'path/to/your/data/file.csv'
    metadata_file_path = 'path/to/your/metadata/file.yaml'

    file_validator = FileValidator(data_file_path, metadata_file_path)
    ```

3. **Perform Validation:**

    To perform the validation, call the `validation` method:

    ```python
    try:
        file_validator.validation()
        print("Validation successful!")
    except ValueError as ve:
        print(f"Validation failed: {ve}")
    ```

4. **Customization:**

    - Customize the paths to your data file and metadata file.
    - Adjust the separator in the metadata file based on your data file's structure.


## Example

Here's an example using the provided data file and metadata:

```python
# Paths to the data file and metadata file
data_file_path = 'path/to/your/data/file.csv'
metadata_file_path = 'path/to/your/metadata/file.yaml'

# Read the data file into a pandas DataFrame
df = pd.read_csv(data_file_path, sep='|')

# Instantiate and validate using the FileValidator
file_validator = FileValidator(data_file_path, metadata_file_path)

try:
    file_validator.validation()
    print("Validation successful!")
except ValueError as ve:
    print(f"Validation failed: {ve}")

```

## Dependencies 📦

- Python 3.x
- PyYAML Library

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to contribute, report issues, or suggest improvements! 🙌
