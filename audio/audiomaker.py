# Script to create audio files
from gtts import gTTS
import os

# Delete all the audio existing files

folder = r"audio/"
for fichier in os.listdir(folder):
    if fichier.endswith(".mp3"):
        chemin_fichier = os.path.join(folder, fichier)
        os.remove(chemin_fichier)



words = ["cześć", ]
for word in words:  
    tts = gTTS(text=word, lang='pl')

    audio_name = word + ".mp3"
    path = r"audio/"
    tts.save(path + audio_name)




