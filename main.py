from fastapi import FastAPI, Form, HTTPException
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pymysql


app = FastAPI()


# Modèle Pydantic pour valider les données

# Connexion à MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dv_lottery"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# route d'accueil
@app.get("/")
async def get_users():
    return {"message": "Bienvenue sur l'API de gestion des utilisateurs du DvLottery"}

# Liste des utilisateurs
@app.get("/users")
async def get_users():
    connection = get_db_connection()
    if connection is None:
        return {"message": "Erreur de connexion à la base de données"}

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        return result
    finally:
        connection.close() 



# Ajout d'un utilisateur
@app.post("/users")
async def create_user(
        nom: str = Form(...),
        prenom: str = Form(...),
        email: str = Form(...),
        sexe: str = Form(...),
        date_naissance: str = Form(...),
        adresse: str = Form(...),
        telephone: str = Form(...),
        nbre_enfant: str = Form(...),
        code_postal: str = Form(...),
        niveau_scolaire: str = Form(...),
    ):
    
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Erreur de connexion à la base de données")
    
    try:
        cursor = connection.cursor()
        created_at = datetime.now().isoformat()  # Utilisez datetime.now() au lieu de datetime.today()
        sql = """INSERT INTO users 
                 (nom, prenom, email, sexe, date_naissance, adresse, telephone, nbre_enfant, code_postal, niveau_scolaire, created_at) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (nom, prenom, email, sexe, date_naissance, adresse, telephone, nbre_enfant, code_postal, niveau_scolaire, created_at)
        cursor.execute(sql, values)
        connection.commit()  
        return {"message": "Utilisateur créé avec succès"}
    except pymysql.MySQLError as e:
        connection.rollback()  
        raise HTTPException(status_code=500, detail=f"Erreur de base de données : {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inattendue : {e}")
    finally:
        cursor.close()
        connection.close() 




# supprimer un utilisateur
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    connection = get_db_connection()
    if connection is None:
        return {"message": "Erreur de connexion à la base de données"}
    
    cursor = connection.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(sql, values)
    if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    connection.commit()
    return {"message": "Utilisateur supprimé avec succès"}


