from transcription_tool import YouTubeTranscriptTool
from content_creator import ContentCreator
import os


class App:
    def __init__(self):
        self.transcription_tool = YouTubeTranscriptTool()
        self.content_creator = ContentCreator()

    @staticmethod
    def create_project_folder(proj_name):
        if not os.path.exists(proj_name):
            os.makedirs(f"projects/{proj_name}")
            print(f"Project created: {proj_name}")
        else:
            print(f"project already exists: {proj_name}, new content will be overlapped!!!")

    def run(self):
        print()
        print("                *reelScriptor*")
        print("*__WELCOME TO YT VIDEO TO REELS SCRIPT CREATOR__*\n")

        project = input("Enter Project Name: ")
        self.create_project_folder(project)

        vid_url = input("Enter YouTube Video URL (it should contain video id): ")

        transcript = self.transcription_tool.fetch_transcript(vid_url)    
        self.transcription_tool.close_driver()
        
        responses = self.content_creator.generate(transcript)

        with (
            open(f"projects/{project}/transcript.txt", 'w', encoding='utf-8') as tr_file,
            open(f"projects/{project}/summary.txt", 'w', encoding='utf-8') as sm_file,
            open(f"projects/{project}/response1.txt", 'w', encoding='utf-8') as r1_file,
            open(f"projects/{project}/scripts.txt", 'w', encoding='utf-8') as sc_file
            ):
                tr_file.write(transcript)
                sm_file.write(responses[0])
                r1_file.write(responses[1])
                sc_file.write(responses[2])

        print(f"\nDone\nPlease check: projects/{project} folder for the content")
        print("\nThankYou\n")

if __name__ == "__main__":
    app = App()
    app.run()