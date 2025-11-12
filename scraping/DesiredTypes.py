import attrs
import typing as t


@attrs.define(on_setattr=attrs.setters.validate)
class CarListing:
    id: str
    url: str
    tytul: str
    opis: str
    cena: int
    prywatne: bool  # handlarz czy osoba prywatne
    model: str | None
    rok_produkcji: int
    paliwo: t.Literal["Diesel", "Benzyna"]  # nie rozrużnaimy narazie lpg
    przebieg: int
    pojemnosc: int
    skrzynia_biegow: t.Literal["Automatyczna", "Manualna"]
    kraj_pochodzenia: str
    moc: int
