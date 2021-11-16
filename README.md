# FAI GLI AUGURI AI TUOI AMICI DA PARTE DI MACCIO CAPATONDA

Da qualche giorno, Maccio Capatonda, di cui sono un grande fan, ha pubblicato [questa simpatica clip][1], una sorta di kit per creare degli auguri video personalizzati, montando un nome di persona su una delle quattro diverse occasioni, previste dal simpatico comico:

- Compleanno
- Laurea
- Matrimonio
- Morte

Appena ho visto video, ho cominciato a pensare come automatizzare il tutto senza utilizzare un software di video editing.

Sono riuscito a generare tutti i video possibili, utilizzando [Python][2], [MoviePy][3] e questo semplicissimo script.

## Istruzioni

Installare le dipendenze con il comando:

`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

Installare le dipendenze con il comando:

`poetry install`

Per lanciare la generazione batch dei video, utilizzare il comando:

`poetry run python -m main`

I video saranno organizzati nella cartella `output`, generata eseguendo il programma.

[1]: https://www.youtube.com/watch?v=D_J1mAN1Hm4
[2]: https://www.python.org/
[3]: https://zulko.github.io/moviepy/
