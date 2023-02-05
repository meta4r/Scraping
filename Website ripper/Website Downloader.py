import requests
from bs4 import BeautifulSoup

url = "http://www.charlescosimano.com/"

def download_page(url):
    # Send a request to the page
    response = requests.get(url)

    # Check if the response is a PDF file
    if "content-type" in response.headers and response.headers["content-type"] == "application/pdf":
        # Save the PDF file
        filename = url.split("/")[-1]
        with open(filename, "wb") as file:
            file.write(response.content)
        return filename

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all the content
    content = str(soup)

    # Create an HTML file for the page
    filename = url.split("/")[-1] + ".html"
    with open(filename, "w") as file:
        file.write(content)
    return filename

# Send a request to the website
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Extract all the links on the website
links = [link.get("href") for link in soup.find_all("a") if link.get("href") is not None]

# Filter the links to only include internal links
internal_links = [link for link in links if link.startswith("/")]

# Download all the pages and PDF files on the website
downloaded_files = []
for link in internal_links:
    url = url + link
    filename = download_page(url)
    downloaded_files.append((link, filename))

# Create an HTML file for the main page
with open("index.html", "w") as file:
    file.write(str(soup))

# Update the links on the main page to point to the downloaded pages and PDF files
soup = BeautifulSoup(open("index.html"), "html.parser")
for link, filename in downloaded_files:
    soup.find("a", href=link).replace_with(soup.new_tag("a", href=filename))

# Save the updated HTML file for the main page
with open("index.html", "w") as file:
    file.write(str(soup))