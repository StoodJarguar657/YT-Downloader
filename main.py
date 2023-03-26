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

import pytube, os
import moviepy.editor as ed

def get_format():
    format = input("Output: [mp3, mp4]: ")

    if "mp3" in format:
        format = "mp3"
    if "mp4" in format:
        format = "mp4"

    if format != "mp4" and format != "mp3":
        get_format()
    return format




def main():
    print("Youtube link to mp3 / mp4 converter by StoodJarguar6577")
    link = input("Link: ")
    format = get_format()


    yt = pytube.YouTube(link)
    print("Downloading mp4")
    video_name = yt.title
    video = yt.streams.get_highest_resolution()
    video.download()

    if format == "mp3":
        paths = os.listdir(os.getcwd())

        # find most matching words since the video name doesnt math
        # Olexesh - MAGISCH feat.Edin(prod.von PzY) [Official 4K Video] > Olexesh - MAGISCH feat Edin (prod von PzY) [Official 4K Video]
        Elements = video_name.replace(".", "").split(" ")

        # iterate over all paths
        Final = 0
        FinalPath = ""
        for path in paths:
            # split at every  " "
            Target = path.split(" ")
            match = 0
            for i1 in range(0, len(Target)):
                for i2 in range(0, len(Elements)):
                    if Elements[i2].lower() in Target[i1].lower():
                        match += 1

            if match > Final:
                Final = match
                FinalPath = path

        video = ed.VideoFileClip(FinalPath)
        audio = video.audio
        audio_name = video_name
        print("Saving as: ", FinalPath.replace(".mp4", ".mp3"))
        audio.write_audiofile(FinalPath.replace(".mp4", ".mp3"))

        audio.close()
        video.close()
    
        os.remove(FinalPath)

        os.system("cls")
    main()
main()
