from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class ExtractUrls:
    def __init__(self, browser):
        self.browser = browser
        self.video_urls = []
    def run(self):
        thumbnails = self.browser.find_elements(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row/div/ytd-rich-item-renderer/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a")
        for thumbnail in thumbnails:
            try:
                ActionChains(self.browser).move_to_element(thumbnail).perform()
                video_url = thumbnail.get_attribute("href")
                self.video_urls.append(video_url)
            except Exception as e:
                print(f"Error extracting video URL: {e}")
    def get_video_urls(self):
        return self.video_urls
