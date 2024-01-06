Version = "0.3"
try:
    import pytube
except:
    import subprocess
    subprocess.call("pip install pytube")

try:
    import moviepy
except:
    import subprocess
    subprocess.call("pip install moviepy")

import pytube, os, requests
import moviepy.editor as ed

def GetFormat():
    Format = input("Output: [mp3, mp4]: ")

    if "mp3" in Format:
        Format = "mp3"
    if "mp4" in Format:
        Format = "mp4"

    if Format != "mp4" and Format != "mp3":
        GetFormat()
    return Format

def main():
    GithubVersion = requests.get("https://raw.githubusercontent.com/StoodJarguar657/YT-Downloader/main/main.py").content.decode().split("\n")[0].split(" ")[2].replace('"', "")
    print("Youtube link to mp3 / mp4 converter by StoodJarguar6577")
    if GithubVersion != Version:
        print("Update available!")
        Option = input("__________\n1: Update\n2: Convert link\n__________\n> ")
        if Option == "1":
            if "update.py" in os.listdir(os.getcwd()):
                CurrentPath = os.path.dirname(os.path.abspath(__file__))
                FilePath = CurrentPath + "\\update.py"
                os.startfile(FilePath)
                quit()


    link = input("Link: ")

    format = GetFormat()

    yt = pytube.YouTube(link)
    print("Downloading mp4")
    Succeed = True
    try:
        video = yt.streams.get_highest_resolution()
        video.download()
    except Exception as error:
        Succeed = False
        os.system("cls")
        print("[ERROR]", error)

    if format == "mp3" and Succeed:
        paths = os.listdir(os.getcwd())
        FinalPath = ""
        HighestTime = 0
        for Path in paths:
            if Path.endswith(".mp4"):
                Stats = os.stat(Path)
                Time = Stats.st_mtime

                if Time > HighestTime:
                    HighestTime = Time
                    FinalPath = os.getcwd() + "\\" + Path

        video = ed.VideoFileClip(FinalPath)
        audio = video.audio
        print("Saving as: ", FinalPath.replace(".mp4", ".mp3"))
        audio.write_audiofile(FinalPath.replace(".mp4", ".mp3"))

        audio.close()
        video.close()

        os.remove(FinalPath)

        os.system("cls")

    main()
main()
