import uvicorn
import random
import os
import jinja2
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Creazione dell'app FastAPI
webapp = FastAPI(
    title='Gruppo Pydantic Persona',
    description= "Visualizzare la liste di utenti, permettere la modifica dei campi di un utente, l'eliminazione e l'aggiunta di nuovi contatti."
)

# Configurazione dei template Jinja2
templates = Jinja2Templates(
    directory='templates',
    autoescape=False,
    auto_reload=True
)

# Montaggio della cartella 'static' per i file statici
webapp.mount(
    '/static',
    app=StaticFiles(directory='static'),
    name='static'
)

# Definizione dell'oggetto Person utilizzando pydantic (altrimenti dovevamo usare dataclasses)
class Person(BaseModel):
    id: int
    firstName: str
    lastname: str
    isMale: bool

# Lista di esempio di persone
persone = [
    Person(id=10, firstName="Catello", lastname="Dapice", isMale=True),
    Person(id=3, firstName="Pio", lastname="Lange", isMale=False)
]

# Rotta che restituisce tutte le persone
@webapp.get("/api")
async def getAllPerson():
    return persone

# Rotta per aggiungere una nuova persona
@webapp.post("/api/{persona}")
async def addPersona(p: Person):
    # Controllo se la persona non esiste già
    if p and p not in persone:
        # Controllo che l'ID sia univoco
        per: Person
        for per in persone:
            if per.id == p.id:
                return {
                    "err": "Id già in uso, non puoi aggiungere questa persona. Cambia id"
                }

        persone.append(p)
        return {
            "msg": f"{p.firstName} {p.lastname} aggiunto alla lista"
        }
    return {
        "err": f"{p.firstName} {p.lastname} non è stato aggiunto alla lista"
    }

# Rotta per eliminare una persona dato l'indice della lista
@webapp.delete("/apiOld/{id}")
async def deletePerson(id: int):
    if 0 <= id < len(persone):
        persone.pop(id)
        return {
            "msg": "Andato"
        }
    return {
        "err": "errore"
    }


# Rotta per eliminare una persona dato l'ID
@webapp.delete("/api/{id}")
async def deletePerson(id: int):
    p: Person
    for p in persone:
        if p.id == id:
            persone.remove(p)
            return {
                "msg": f"La persona con Id {id} è stata eliminata con successo"
            }
    return {
        "err": f"La persona con Id {id} non è stata eliminata"
    }

# Rotta per aggiornare una persona dato l'ID
@webapp.put("/api/{id}/{person}")
async def updatePerson(id: int, daAggiungere: Person):
    p: Person
    for p in persone:
        if p.id == id:
            persone.remove(p)
            per: Person
            for per in persone:
                if per.id == daAggiungere.id:
                    persone.append(p)
                    return {
                        "err": "Id già in uso, non puoi aggiornare questa persona con un id già in uso. Modifica id"
                    }

            persone.append(daAggiungere)
            return {
                "msg": "Persona aggiornata con successo"
            }
    return {
        "msg": "Id non trovato, non possibile aggiornare"
    }

# Avvio dell'applicazione utilizzando uvicorn
if __name__ == '__main__':
    uvicorn.run(
        'main:webapp',
        reload=True
    )
