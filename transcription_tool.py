from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YouTubeTranscriptTool:
    def __init__(self, wait_time=30):
        """
        Initializes the tool with Selenium WebDriver settings.
        :param driver_path: Path to the ChromeDriver executable.
        :param headless: Whether to run Chrome in headless mode.
        :param wait_time: Maximum wait time for elements to load.
        """
        self.wait_time = wait_time
        self.driver = None

    def _initialize_driver(self):
        """
        Initializes the Selenium WebDriver with the provided options.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def fetch_transcript(self, video_url):
        """
        Fetches the transcript of a YouTube video using youtubetranscript.com.
        :param video_url: URL of the YouTube video.
        :return: Transcript text if successful, None otherwise.
        """
        try:
            if not self.driver:
                self._initialize_driver()

            # Open the website
            print("[INFO] Opening website...")
            self.driver.get("https://youtubetranscript.com/")

            # Locate the input field and enter the video URL
            print("[INFO] Entering video URL...")
            input_box = self.driver.find_element(By.ID, "video_url")
            input_box.send_keys(video_url)
            input_box.send_keys(Keys.RETURN)  # Simulate pressing Enter

            # Wait for the transcript text to load and update
            print("[INFO] Waiting for transcript to load...")
            wait = WebDriverWait(self.driver, self.wait_time)

            # Wait for the #demo element to appear
            wait.until(EC.presence_of_element_located((By.ID, "demo")))

            # Wait for the transcript content to be ready
            def transcript_is_ready(driver):
                element = driver.find_element(By.ID, "demo")
                text = element.text.strip()
                return text and text != "Loading captions..."

            wait.until(transcript_is_ready)

            # Extract and return the transcript
            transcript_element = self.driver.find_element(By.ID, "demo")
            transcript = transcript_element.text

            if transcript:
                print("[INFO] Transcript successfully loaded.")
                return transcript
            else:
                print("[ERROR] Transcript element is empty.")
                return None

        except Exception as e:
            print(f"[ERROR] {e}")
            return None

    def close_driver(self):
        """
        Closes the Selenium WebDriver instance.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None

# Usage Example
if __name__ == "__main__":
      # Replace with the path to your ChromeDriver
    video_url = "https://www.youtube.com/watch?v=SATEUEKh7xA&t=3s&ab_channel=FullDisclosure"

    yt_tool = YouTubeTranscriptTool()
    transcript = yt_tool.fetch_transcript(video_url)
    yt_tool.close_driver()

    if transcript:
        print("Transcript:")
        print(transcript)
    else:
        print("Transcript could not be retrieved.")
