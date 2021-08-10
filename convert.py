from pydub import AudioSegment

mp3_audio = AudioSegment.from_mp3("sounds/default.mp3")
mp3_audio.export("sounds/default.ogg", format="ogg")
