# Gkom Animation Program
## Temat projektu
    W ramach projektu stworzyliśmy prosty program, który umożliwia
    proste animacji wczytanych modeli.
## Podstawowe założenia
    1. Wsparcie typu: obj, dla plików wejściowych z modelem 3D.
    2. Cieniowanie Phonga.
    3. Interpretację właściwości materiału: diffuse, specular.
    4. Wsparcie dla światła punktowego - możliwość poruszania światłem, edycja
    właściwości światła.
    5. Możliwość zrobienia prostej animacji, a w niej:
        a. wstawianie i edycja klatek kluczowych dla transformacji (translacja,
        rotacja, skalowanie)
        b. interpolacja stała i liniowa między klatkami.
    6. Kamerę perspektywiczną - możliwość poruszania się po scenie oraz obrotu.
    7. Możliwość renderu animacji do pliku wideo.
## Szczegóły implementacji
### main.py 
    W głównej pętli programu, która jest obsługiwana przez wątek Pygame,
    symulacja graficzna jest ciągle odświeżana na ekranie. Program nasłuchuje
    zdarzeń interakcji użytkownika (np. naciśnięcie klawiszy, zamknięcie okna),
    które mogą wpływać na transformacje obiektów (translacja, rotacja, skalowanie)
    oraz na ustawienia kamery i siatki. W tle, każdy ruch lub zmiana jest synchronizowana
    z suwakiem klatek, pozwalając na płynną animację między zdefiniowanymi klatkami kluczowymi
    poprzez interpolację. Równolegle, interfejs użytkownika Tkinter obsługuje kontrolki animacji,
    światła i materiału, które są zintegrowane z renderowanym środowiskiem w Pygame.

### moduł src
    Moduł src zawiera implementację poszczegolnych funkcjonalności programu, min. kamery, interpolacji, klatek kluczowych, sposobu zachowywania ise światła, wczytywania plików oraz renderowania animacji do pliku wideo.

    camera.py - Klasa Camera umożliwia manipulację widokiem w scenie 3D poprzez regulowanie odległości (zoom), kierunku patrzenia (azymut i elewacja) oraz pola widzenia (FOV), reagując na interakcje użytkownika z klawiaturą.

    keyframe.py - Klasa Keyframe w programie służy do definiowania i zarządzania klatkami kluczowymi w animacji, przechowując informacje o położeniu, orientacji i skali obiektu w danej klatce. Umożliwia ona modyfikację tych parametrów poprzez reakcję na zdarzenia klawiatury, co pozwala na dynamiczne zmiany transformacji obiektów w czasie, wspierając płynne animacje dzięki interpolacji między klatkami.

    light.py - Klasa Material w programie zarządza właściwościami materiału obiektów renderowanych w scenie, takimi jak kolor ambient, diffuse, specular oraz połysk (shininess). Pozwala na dynamiczną zmianę tych właściwości w celu dostosowania wyglądu obiektów w zależności od potrzeb użytkownika i sceny.Klasa Light obsługuje konfigurację oświetlenia w scenie, przechowując i zarządzając właściwościami takimi jak kolor światła ambient, diffuse, specular, oraz jego pozycję. Metoda setup_lighting inicjuje te ustawienia w kontekście graficznym OpenGL, łącząc je z właściwościami materiału, aby efektywnie symulować oświetlenie i cienie w scenie.

    render.py - Funkcja save_frame() zapisuje bieżący stan renderowanego obrazu w scenie OpenGL, przechwytując piksele z bufora ramki i konwertując je na obraz w formacie RGB, który jest następnie odwracany do odpowiedniej orientacji. Wynikowy obraz może być wykorzystany do dalszej analizy lub jako pojedyncza klatka w animacji. Funkcja save_video() agreguje serię obrazów w formie klatek animacji i zapisuje je do pliku wideo w formacie MP4 z określoną liczbą klatek na sekundę (FPS). Ta metoda umożliwia łatwe tworzenie plików wideo z sekwencji renderowanych klatek, co jest przydatne w produkcji wizualizacji i animacji 3D.

## Instrukcja użytkownika
### Uruchamianie programu:
    pipenv install
    pipenv shell
    python main.py "ściezka do pliku z obiektem 3D"
### Obsługa programu:
    Sterowanie kamerą:
        Strzałka w górę (↑): Zmniejsz zoom, przybliżając kamerę do środka sceny.
        Strzałka w dół (↓): Zwiększ zoom, oddalając kamerę od środka sceny.
        W: Zwiększ elewację, podnosząc kąt patrzenia kamery w górę.
        S: Zmniejsz elewację, opuszczając kąt patrzenia kamery w dół.
        A: Zmniejsz azymut, obracając kamerę w lewo.
        D: Zwiększ azymut, obracając kamerę w prawo.
    Dodawanie klatki kluczowej:
        1. Na suwaku wybierz klatkę
        2. Wstaw klatkę kluczową
        3. Sterowanie keyframe:
            Zmiana położenia obiektu
                1/KP1: Zwiększ przesunięcie w osi X.
                2/KP2: Zwiększ przesunięcie w osi Y.
                3/KP3: Zwiększ przesunięcie w osi Z.
                4/KP4: Zmniejsz przesunięcie w osi X.
                5/KP5: Zmniejsz przesunięcie w osi Y.
                6/KP6: Zmniejsz przesunięcie w osi Z.
            Zmiana orientacji obiektu
                1/KP1: Zwiększ obrót wokół osi X.
                2/KP2: Zwiększ obrót wokół osi Y.
                3/KP3: Zwiększ obrót wokół osi Z.
                4/KP4: Zmniejsz obrót wokół osi X.
                5/KP5: Zmniejsz obrót wokół osi Y.
                6/KP6: Zmniejsz obrót wokół osi Z.
            Zmiana skali obiektu
                1/KP1: Zwiększ skalę w osi X.
                2/KP2: Zwiększ skalę w osi Y.
                3/KP3: Zwiększ skalę w osi Z.
                4/KP4: Zmniejsz skalę w osi X.
                5/KP5: Zmniejsz skalę w osi Y.
                6/KP6: Zmniejsz skalę w osi Z.
        4. Zapisz klatkę kluczową.