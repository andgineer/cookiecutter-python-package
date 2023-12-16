"""Post generation hook to rename files and folders."""
import os
import shutil


def main():
    """Rename files and folders."""
    os.rename('_github', '.github')

    readme_path = 'README.md'
    if os.path.exists(readme_path):
        os.remove(readme_path)
    os.rename('PROJECT_README.md', readme_path)


if __name__ == "__main__":
    main()
