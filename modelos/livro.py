from dataclasses import dataclass

@dataclass
class Livro:
    id: int | None
    titulo: str
    autor: str
    status: str
    paginas: int
    data: str | None
    formato: str
    anotacoes: str
    capa: str | None = None