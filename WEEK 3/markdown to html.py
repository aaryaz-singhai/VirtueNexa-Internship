import markdown
import os

def convert_md_to_html():
    # Ask user for input file path
    input_path = input("Enter the full path to the Markdown (.md) file: ").strip()

    # Check if the file exists
    if not os.path.isfile(input_path):
        print("Error: The specified file does not exist.")
        return

    # Check if the file is a markdown file
    if not input_path.endswith(".md"):
        print("Error: Please provide a file with a .md extension.")
        return

    # Read markdown content
    with open(input_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Convert to HTML
    html_content = markdown.markdown(md_content)

    # Define output path (same name with .html extension)
    output_path = os.path.splitext(input_path)[0] + ".html"

    # Write HTML content to new file
    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"✅ Successfully converted to HTML: {output_path}")

if __name__ == "__main__":
    convert_md_to_html()
