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
        cd file-validation   
    ```

3. Run the script:
    
   ```bash 
        cd file-validation
    ```

## Features 🌟

- Validates file existence and metadata consistency.
- Checks column names, order, and structure.


## How to Use 🤔

1. Provide the path to your data file.
2. Specify the metadata file containing validation rules.

```python
path = '../files/your_data_file.csv'
metadata = '../metadata/your_metadata_file.yaml'

file_val = FileValidator(path, metadata)

metadata_dict = file_val._get_metadata_info()

print(metadata_dict)

print(file_val._header_validation())
```

## Dependencies 📦

- Python 3.x
- PyYAML Library

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to contribute, report issues, or suggest improvements! 🙌
