# fastapi-projekt

Kod składający się z trzech endpointów 

1. Endpoint sprawdzający, czy dana liczba jest pierwsza (zakres do 9223372036854775807)
GET <host>/prime/<number>
NIE zakładamy, że dane wejściowe są poprawne

2. Endpoint do zwrócenia inwersji kolorów obrazka.
Inwersja odbywa się w insturkcji POST 
POST <host>/picture/invert
Zakładamy, że dane wejściowe są poprawne.

3. Endpoint za uwierzytelnianiem zwracający aktualną godzinę, również w instrukcji POST.
