from pydub import AudioSegment

# Carregar o arquivo de áudio
audio = AudioSegment.from_file('sounds/musica_fundo.ogg', format='ogg')

# Diminuir o volume pela metade (-6 dB)
audio = audio - 6

# Salvar o arquivo com o volume reduzido
audio.export('sounds/musica_fundo-red.ogg', format='ogg')
