from crewai_tools import tool

class FileManagementTools:
    @tool("Read project file")
    def read_file(file_path: str):
        """Useful to read content from a specific file in the project."""
        with open(file_path, 'r') as f:
            return f.read()

    @tool("Save refined content")
    def write_file(file_path: str, content: str):
        """Useful to save the final improved content back to the project file."""
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully saved to {file_path}"
