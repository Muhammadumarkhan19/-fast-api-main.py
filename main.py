from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

CONTACT_FILE = "contacts.json"
def load_contacts():
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, "r") as file:
            return json.load(file)
    return {}
def save_contacts(contacts):
    with open(CONTACT_FILE, "w") as file:
        json.dump(contacts, file, indent=4)
@app.post("/contacts/")
def add_contact(name: str, phone: str, email: str):
    contacts = load_contacts()
    if name in contacts:
        raise HTTPException(status_code=400, detail="Contact already exists!")
    contacts[name] = {"Phone": phone, "Email": email}
    save_contacts(contacts)
    return {"message": f"{name} added successfully!"}
@app.get("/contacts/")
def get_contacts():
    return load_contacts()
@app.get("/contacts/{name}")
def search_contact(name: str):
    contacts = load_contacts()
    if name in contacts:
        return contacts[name]
    raise HTTPException(status_code=404, detail="Contact not found!")
@app.put("/contacts/{name}")
def update_contact(name: str, phone: str = None, email: str = None):
    contacts = load_contacts()
    if name in contacts:
        if phone:
            contacts[name]["Phone"] = phone
        if email:
            contacts[name]["Email"] = email
        save_contacts(contacts)
        return {"message": f"{name} updated successfully!"}
    raise HTTPException(status_code=404, detail="Contact not found!")
@app.delete("/contacts/{name}")
def delete_contact(name: str):
    contacts = load_contacts()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        return {"message": f"{name} deleted successfully!"}
    raise HTTPException(status_code=404, detail="Contact not found!")
