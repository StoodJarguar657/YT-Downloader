Version = "0.4"

import os, subprocess, importlib, requests, time

class PackageChecker():
    def __init__(self):
        self.FoundPackages = []
        self.ImportedPackages = dict()
        self.OutdatedPackages = []

    def CheckPackages(self, PackageList):
        print("[+] Checking packages")

        # Check if the packages are up-to-date
        Result = subprocess.run("pip list --outdated", capture_output=True, text=True)

        Lines = Result.stdout.splitlines()
        for Line in Lines:
            for Package in PackageList:
                if Line.startswith(Package):
                    self.OutdatedPackages.append(Package)
                    print(f"[-] Outdated package {Package}")
                    break

        # Update
        for Package in self.OutdatedPackages:
            subprocess.call(f"pip install --upgrade {Package}")

        print("-----------------------------------")

        # Try to import
        for Package in PackageList:
            Success = True
            Module = None
            try:
                Module = importlib.import_module(Package)
            except Exception as error:
                Success = False
                print("[-]", error)
                subprocess.call(f"pip install {Package}")
            print(f"[+] Found {Package}")

            if Success:
                self.ImportedPackages[Package] = Module
            else:
                self.ImportedPackages[Package] = importlib.import_module(Package)

            self.FoundPackages.append(Package)

        os.system("cls")



class YTDownloader():
    def __init__(self, PackageList):
        self.Packages = PackageList
        self.YT = None

    def CheckVersion(self):
        GithubVersion = requests.get("https://raw.githubusercontent.com/StoodJarguar657/YT-Downloader/main/main.py").content.decode().split("\n")[0].split(" ")[2].replace('"', "")
        if GithubVersion != Version:
            print("Update available!")
            Option = input("__________\n1: Update\n2: Convert link\n__________\n> ")
            if Option == "1":
                if "update.py" in os.listdir(os.getcwd()):
                    CurrentPath = os.path.dirname(os.path.abspath(__file__))
                    FilePath = CurrentPath + "\\update.py"
                    os.startfile(FilePath)
                    quit()

    def PrintProgress(self, Current, Total):
        Present = ("{0:.1f}").format(100 * (Current / float(Total)))
        FilledLength = int(100 * Current // Total)
        Bar = '#' * FilledLength + '-' * (100 - FilledLength)
        print(f'Progress\r |{Bar}| {Present}% Complete', end="\r")
        if Current == Total:
            print()

    def ProgressBar(self, Stream, ByteChunk, RemainingBytes):
        self.PrintProgress(Stream.filesize - RemainingBytes, Stream.filesize)

    def Query(self, YTLink):
        self.YT = self.Packages["pytube"].YouTube(YTLink, on_progress_callback=self.ProgressBar)

        # Prints the name, and duration of the track
        Seconds = self.YT.length
        Hours = Seconds // 3600
        Seconds %= 3600
        Minutes = Seconds // 60
        Seconds %= 60

        print(f"'{self.YT.title}' by '{self.YT.author}'  {Hours:02}:{Minutes:02}:{Seconds:02}")

    def RequestFormat(self):
        Format = input("Output: [mp3, mp4]: ")

        if "mp3" in Format:
            Format = "mp3"
        if "mp4" in Format:
            Format = "mp4"

        if Format != "mp4" and Format != "mp3":
            self.RequestFormat()
        return Format

    def Download(self, Format):

        CurrentDir = os.getcwd()
        Mp3File = os.path.join(CurrentDir, self.YT.title + ".mp3")
        Mp4File = os.path.join(CurrentDir, self.YT.title + ".mp4")

        if Format == "mp3":
            self.YT.streams.filter(file_extension=".mp3")
            if os.path.exists(Mp3File):
                print("File already exists!")
                time.sleep(2)
                os.system("cls")
                return

            try:
                Audio = self.YT.streams.get_audio_only()
                Audio.download()
            except Exception as error:
                os.system("cls")
                print("[ERROR]", error)
                time.sleep(5)
                os.system("cls")
                return

        if Format == "mp4":
            self.YT.streams.filter(file_extension=".mp4")
            if os.path.exists(Mp4File):
                print("File already exists!")
                time.sleep(2)
                os.system("cls")
                return

            try:
                Video = self.YT.streams.get_highest_resolution()
                Video.download()
            except Exception as error:
                os.system("cls")
                print("[ERROR]", error)
                time.sleep(5)
                os.system("cls")
                return

        print("Done!")
        time.sleep(2)
        os.system("cls")

PackageChecker = PackageChecker()
PackageChecker.CheckPackages(["pytube", "requests"])

Downloader = YTDownloader(PackageChecker.ImportedPackages)
Downloader.CheckVersion()

def main():
    print("Youtube link to mp3 / mp4 converter by StoodJarguar6577")

    YTLink = input("Link: ")
    Downloader.Query(YTLink)

    Format = Downloader.RequestFormat()
    Downloader.Download(Format)

    main()

if __name__ == "__main__":
    main()
