from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Art(BaseModel):
    name: str
    artist: str
    style: str

#The Mock Database thingy
art_gallery = [
    {"name": "Mona Lisa", "artist": "Leonardo da Vinci", "style": "Renaissance"},
    {"name": "The Starry Night", "artist": "Vincent van Gogh", "style": "Post-Impressionism"}
]

@app.get("/")
async def ArtWelcome():
    return {"message": "Hi there, Wanna find some art? Yeah me too!"}

#GET: Returns 200 OK (and handles empty database)
@app.get("/api/art", status_code=200)
async def get_all_art():
    if len(art_gallery) == 0:
        #This Fulfills "maneja errores" for GET
        raise HTTPException(status_code=404, detail="No art found in the gallery")
    return art_gallery

#GET by Name: This Fulfills the 404 requirement
@app.get("/api/art/{art_name}", status_code=200)
async def get_art_by_name(art_name: str):
    for art in art_gallery:
        if art["name"].lower() == art_name.lower():
            return art
    #If the loop finishes and finds nothing, trigger a 404!
    raise HTTPException(status_code=404, detail="Art piece not found")

#POST: This Fulfills 201, 400, and Validations
@app.post("/api/art", status_code=201)
async def create_art(new_art: Art):
    #This Fulfills "valida entradas" and 400 status code requirement
    if new_art.name.strip() == "" or new_art.artist.strip() == "":
        raise HTTPException(status_code=400, detail="Name and Artist cannot be empty")
        
    art_gallery.append(new_art.dict())
    return new_art

#PUT: This Fulfills 200, 400, and Validations
@app.put("/api/art/{art_name}", status_code=200)
async def update_art(art_name: str, updated_art: Art):
    for i, art in enumerate(art_gallery):
        if art["name"].lower() == art_name.lower():
            art_gallery[i] = updated_art.dict()
            return {"message": "Artwork updated successfully", "art": updated_art}
    #If the loop finishes and finds nothing, trigger a 404!
    raise HTTPException(status_code=404, detail="Art piece not found")

#DELETE: This Fulfills 200 and 404
@app.delete("/api/art/{art_name}", status_code=200)
async def delete_art(art_name: str):
    #Loop through the gallery to find the artwork
    for i, art in enumerate(art_gallery):
        if art["name"].lower() == art_name.lower():
            #.pop() removes the item from the list
            deleted_art = art_gallery.pop(i)
            return {"message": "Artwork deleted successfully", "art": deleted_art}
            
    #If it can't find it to delete, return a 404 Error
    raise HTTPException(status_code=404, detail="Art piece not found to delete")