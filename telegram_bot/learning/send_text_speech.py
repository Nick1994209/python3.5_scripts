from gtts import gTTS

tts = gTTS(text='А Маша простокваша!', lang='ru', slow=True, debug=True)
tts.save("hello.mp3")

# f = TemporaryFile()
# tts.write_to_fp(f)
# # <Do something with f>
# f.close()
