from selenium import webdriver
from scroll_to_end import ScrollToEnd
from extract_urls import ExtractUrls

if __name__ == '__main__':
    # Start a new browser session
    browser = webdriver.Firefox()

    url = "https://www.youtube.com/@jawed/videos"
    # Navigate to the website
    browser.get(url)

    # Scroll to the end of the page
    ScrollToEnd(browser).run()

    # Extract video URLs
    ExtractUrls(browser).run()
    video_urls = ExtractUrls(browser).get_video_urls()

    # Print the video URLs
    print(video_urls)

    # Close the browser
    browser.close()
