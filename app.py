import streamlit as st
import sqlite3
import os
import datetime
import hashlib

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(page_title="Haiti Archives Nationales Database", layout="wide")

# ----------------------------------------------------------------------
# Multi-language dictionary
# ----------------------------------------------------------------------
lang_dict = {
    "en": {
        "title": "Haiti Archives Nationales Database",
        "login": "🔐 Login",
        "password": "Enter annual password",
        "wrong_password": "Incorrect password. Access denied.",
        "logout": "Logout",
        "dashboard": "Dashboard",
        "add_citizen": "Add New Citizen",
        "edit_citizen": "Edit Citizen",
        "search": "Search",
        "matricule": "Matricule Fiscale (NIF)",
        "full_name": "Full Name",
        "birth_date": "Date of Birth",
        "birth_place": "Place of Birth",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "cin": "CIN Card",
        "cin_number": "CIN Number",
        "cin_delivery": "Delivery Date",
        "cin_expiry": "Expiry Date",
        "passport": "Passport",
        "passport_number": "Passport Number",
        "passport_delivery": "Delivery Date",
        "passport_expiry": "Expiry Date",
        "drivers_license": "Driver's License",
        "license_number": "License Number",
        "license_delivery": "Delivery Date",
        "license_expiry": "Expiry Date",
        "voting": "Voting History (optional)",
        "voting_years": "Years voted (comma separated)",
        "sponsorships": "Sponsorships",
        "family_sponsorship": "Family Sponsorship ID",
        "school_sponsorship": "School Sponsorship ID",
        "other_sponsorship": "Other Sponsorship ID",
        "documents": "Upload Documents (PDF, JPG, PNG)",
        "minister_signature": "Minister's Signature (to validate this file)",
        "sign": "Sign and Validate",
        "signed_by": "Signed by Minister on",
        "not_signed": "Not yet validated",
        "developer": "Software Python Developer: Gesner Deslandes",
        "company": "GlobalInternet.py",
        "email": "deslndes78@gmail.com",
        "phone": "(509) 4738-5663",
        "save": "Save",
        "update": "Update",
        "delete": "Delete",
        "confirm_delete": "Are you sure you want to delete this citizen?",
        "year": "Year",
        "select_year": "Select Year",
        "new_year": "New Year Archive",
        "change_password": "Change Annual Password (for next year)",
        "current_password": "Current password",
        "new_password": "New password",
        "confirm_password": "Confirm new password",
        "password_updated": "Password updated successfully for next year.",
        "upload_success": "File uploaded successfully.",
        "citizen_saved": "Citizen record saved.",
        "citizen_updated": "Citizen record updated.",
        "citizen_deleted": "Citizen record deleted.",
    },
    "fr": {
        "title": "Base de données des Archives Nationales d'Haïti",
        "login": "🔐 Connexion",
        "password": "Entrez le mot de passe annuel",
        "wrong_password": "Mot de passe incorrect. Accès refusé.",
        "logout": "Déconnexion",
        "dashboard": "Tableau de bord",
        "add_citizen": "Ajouter un citoyen",
        "edit_citizen": "Modifier le citoyen",
        "search": "Rechercher",
        "matricule": "Matricule Fiscale (NIF)",
        "full_name": "Nom complet",
        "birth_date": "Date de naissance",
        "birth_place": "Lieu de naissance",
        "gender": "Genre",
        "male": "Homme",
        "female": "Femme",
        "cin": "Carte CIN",
        "cin_number": "Numéro CIN",
        "cin_delivery": "Date de délivrance",
        "cin_expiry": "Date d'expiration",
        "passport": "Passeport",
        "passport_number": "Numéro de passeport",
        "passport_delivery": "Date de délivrance",
        "passport_expiry": "Date d'expiration",
        "drivers_license": "Permis de conduire",
        "license_number": "Numéro de permis",
        "license_delivery": "Date de délivrance",
        "license_expiry": "Date d'expiration",
        "voting": "Historique de vote (optionnel)",
        "voting_years": "Années de vote (séparées par des virgules)",
        "sponsorships": "Parrainages",
        "family_sponsorship": "ID parrainage familial",
        "school_sponsorship": "ID parrainage scolaire",
        "other_sponsorship": "Autre ID de parrainage",
        "documents": "Télécharger des documents (PDF, JPG, PNG)",
        "minister_signature": "Signature du Ministre (pour valider ce dossier)",
        "sign": "Signer et valider",
        "signed_by": "Signé par le Ministre le",
        "not_signed": "Non encore validé",
        "developer": "Développeur Python: Gesner Deslandes",
        "company": "GlobalInternet.py",
        "email": "deslndes78@gmail.com",
        "phone": "(509) 4738-5663",
        "save": "Enregistrer",
        "update": "Mettre à jour",
        "delete": "Supprimer",
        "confirm_delete": "Voulez-vous vraiment supprimer ce citoyen ?",
        "year": "Année",
        "select_year": "Sélectionner l'année",
        "new_year": "Nouvelle archive annuelle",
        "change_password": "Changer le mot de passe annuel (pour l'année prochaine)",
        "current_password": "Mot de passe actuel",
        "new_password": "Nouveau mot de passe",
        "confirm_password": "Confirmer le nouveau mot de passe",
        "password_updated": "Mot de passe mis à jour avec succès pour l'année prochaine.",
        "upload_success": "Fichier téléchargé avec succès.",
        "citizen_saved": "Dossier citoyen enregistré.",
        "citizen_updated": "Dossier citoyen mis à jour.",
        "citizen_deleted": "Dossier citoyen supprimé.",
    },
    "es": {
        "title": "Base de Datos de los Archivos Nacionales de Haití",
        "login": "🔐 Iniciar sesión",
        "password": "Ingrese la contraseña anual",
        "wrong_password": "Contraseña incorrecta. Acceso denegado.",
        "logout": "Cerrar sesión",
        "dashboard": "Tablero",
        "add_citizen": "Agregar ciudadano",
        "edit_citizen": "Editar ciudadano",
        "search": "Buscar",
        "matricule": "Matrícula Fiscal (NIF)",
        "full_name": "Nombre completo",
        "birth_date": "Fecha de nacimiento",
        "birth_place": "Lugar de nacimiento",
        "gender": "Género",
        "male": "Hombre",
        "female": "Mujer",
        "cin": "Cédula CIN",
        "cin_number": "Número de CIN",
        "cin_delivery": "Fecha de entrega",
        "cin_expiry": "Fecha de vencimiento",
        "passport": "Pasaporte",
        "passport_number": "Número de pasaporte",
        "passport_delivery": "Fecha de entrega",
        "passport_expiry": "Fecha de vencimiento",
        "drivers_license": "Licencia de conducir",
        "license_number": "Número de licencia",
        "license_delivery": "Fecha de entrega",
        "license_expiry": "Fecha de vencimiento",
        "voting": "Historial de votación (opcional)",
        "voting_years": "Años votados (separados por comas)",
        "sponsorships": "Patrocinios",
        "family_sponsorship": "ID de patrocinio familiar",
        "school_sponsorship": "ID de patrocinio escolar",
        "other_sponsorship": "Otro ID de patrocinio",
        "documents": "Subir documentos (PDF, JPG, PNG)",
        "minister_signature": "Firma del Ministro (para validar este expediente)",
        "sign": "Firmar y validar",
        "signed_by": "Firmado por el Ministro el",
        "not_signed": "Aún no validado",
        "developer": "Desarrollador Python: Gesner Deslandes",
        "company": "GlobalInternet.py",
        "email": "deslndes78@gmail.com",
        "phone": "(509) 4738-5663",
        "save": "Guardar",
        "update": "Actualizar",
        "delete": "Eliminar",
        "confirm_delete": "¿Está seguro de eliminar este ciudadano?",
        "year": "Año",
        "select_year": "Seleccionar año",
        "new_year": "Nuevo archivo anual",
        "change_password": "Cambiar contraseña anual (para el próximo año)",
        "current_password": "Contraseña actual",
        "new_password": "Nueva contraseña",
        "confirm_password": "Confirmar nueva contraseña",
        "password_updated": "Contraseña actualizada correctamente para el próximo año.",
        "upload_success": "Archivo subido con éxito.",
        "citizen_saved": "Registro de ciudadano guardado.",
        "citizen_updated": "Registro de ciudadano actualizado.",
        "citizen_deleted": "Registro de ciudadano eliminado.",
    },
    "ht": {
        "title": "Baz Done Achiv Nasyonal Ayiti",
        "login": "🔐 Konekte",
        "password": "Antre modpas anyèl la",
        "wrong_password": "Modpas pa bon. Aksè refize.",
        "logout": "Dekonekte",
        "dashboard": "Tablo de bor",
        "add_citizen": "Ajoute yon sitwayen",
        "edit_citizen": "Modifye sitwayen",
        "search": "Chèche",
        "matricule": "Matrikil Fiskal (NIF)",
        "full_name": "Non konplè",
        "birth_date": "Dat nesans",
        "birth_place": "Kote li fèt",
        "gender": "Sèks",
        "male": "Gason",
        "female": "Fanm",
        "cin": "Kat CIN",
        "cin_number": "Nimewo CIN",
        "cin_delivery": "Dat livrezon",
        "cin_expiry": "Dat ekspirasyon",
        "passport": "Paspò",
        "passport_number": "Nimewo paspò",
        "passport_delivery": "Dat livrezon",
        "passport_expiry": "Dat ekspirasyon",
        "drivers_license": "Pèmi kondwi",
        "license_number": "Nimewo pèmi",
        "license_delivery": "Dat livrezon",
        "license_expiry": "Dat ekspirasyon",
        "voting": "Istwa vòt (opsyonèl)",
        "voting_years": "Ane li te vote (separe ak vigil)",
        "sponsorships": "Patenarya",
        "family_sponsorship": "ID patenarya fanmi",
        "school_sponsorship": "ID patenarya lekòl",
        "other_sponsorship": "Lòt ID patenarya",
        "documents": "Chaje dokiman (PDF, JPG, PNG)",
        "minister_signature": "Siyati Minis la (pou valide dosye sa a)",
        "sign": "Siyen ak valide",
        "signed_by": "Siyen pa Minis la le",
        "not_signed": "Pokò valide",
        "developer": "Devlopè Python: Gesner Deslandes",
        "company": "GlobalInternet.py",
        "email": "deslndes78@gmail.com",
        "phone": "(509) 4738-5663",
        "save": "Sere",
        "update": "Mete ajou",
        "delete": "Efase",
        "confirm_delete": "Èske w sèten ou vle efase sitwayen sa a?",
        "year": "Ane",
        "select_year": "Chwazi ane a",
        "new_year": "Nouvo achiv anyèl",
        "change_password": "Chanje modpas anyèl la (pou ane kap vini an)",
        "current_password": "Modpas aktyèl",
        "new_password": "Nouvo modpas",
        "confirm_password": "Konfime nouvo modpas",
        "password_updated": "Modpas mete ajou avèk siksè pou ane kap vini an.",
        "upload_success": "Dosye chaje avèk siksè.",
        "citizen_saved": "Dosye sitwayen anrejistre.",
        "citizen_updated": "Dosye sitwayen mete ajou.",
        "citizen_deleted": "Dosye sitwayen efase.",
    }
}

# ----------------------------------------------------------------------
# Database setup (SQLite)
# ----------------------------------------------------------------------
DB_NAME = "haiti_archives.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS citizens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        matricule TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        birth_date TEXT,
        birth_place TEXT,
        gender TEXT,
        cin_number TEXT,
        cin_delivery TEXT,
        cin_expiry TEXT,
        passport_number TEXT,
        passport_delivery TEXT,
        passport_expiry TEXT,
        license_number TEXT,
        license_delivery TEXT,
        license_expiry TEXT,
        voting_years TEXT,
        family_sponsorship TEXT,
        school_sponsorship TEXT,
        other_sponsorship TEXT,
        minister_signed BOOLEAN DEFAULT 0,
        minister_signature_date TEXT,
        minister_name TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS citizen_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        citizen_id INTEGER,
        file_name TEXT,
        file_path TEXT,
        upload_date TEXT,
        FOREIGN KEY (citizen_id) REFERENCES citizens (id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS app_config (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')
    conn.commit()
    conn.close()

def get_current_year():
    return datetime.datetime.now().year

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def verify_password(pwd):
    stored_hash = get_config("password_hash")
    if not stored_hash:
        set_config("password_hash", hash_password("18032026"))
        stored_hash = hash_password("18032026")
    return stored_hash == hash_password(pwd)

def set_config(key, value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("REPLACE INTO app_config (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_config(key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM app_config WHERE key = ?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def change_password(new_pwd):
    set_config("password_hash", hash_password(new_pwd))

# ----------------------------------------------------------------------
# Streamlit app
# ----------------------------------------------------------------------
init_db()

# Language selection
lang = st.sidebar.selectbox("Language", list(lang_dict.keys()), format_func=lambda x: {"en":"English","fr":"Français","es":"Español","ht":"Kreyòl"}[x])
t = lang_dict[lang]

# Login mechanism
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Official Haitian flag with coat of arms (reliable URL)
    st.image("https://www.countryflags.com/wp-content/uploads/haiti-flag-png-large.png", width=200)
    st.title(t["title"])
    st.markdown("### 🇭🇹 " + t["login"])
    pwd = st.text_input(t["password"], type="password")
    if st.button(t["login"]):
        if verify_password(pwd):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error(t["wrong_password"])
    st.stop()

# Main app after login
st.sidebar.image("https://www.countryflags.com/wp-content/uploads/haiti-flag-png-large.png", width=150)
st.sidebar.title(t["title"])
st.sidebar.write(f"**{t['developer']}**")
st.sidebar.write(f"🏢 {t['company']}")
st.sidebar.write(f"📧 {t['email']}")
st.sidebar.write(f"📞 {t['phone']}")
if st.sidebar.button(t["logout"]):
    st.session_state.authenticated = False
    st.rerun()

# Year selection
years = list(range(2020, get_current_year()+2))
selected_year = st.sidebar.selectbox(t["select_year"], years, index=years.index(get_current_year()))
st.sidebar.markdown("---")
# Admin: change password
with st.sidebar.expander(t["change_password"]):
    old = st.text_input(t["current_password"], type="password")
    new1 = st.text_input(t["new_password"], type="password")
    new2 = st.text_input(t["confirm_password"], type="password")
    if st.button("Update"):
        if verify_password(old):
            if new1 == new2 and new1:
                change_password(new1)
                st.success(t["password_updated"])
            else:
                st.error("New passwords do not match or empty.")
        else:
            st.error("Current password incorrect.")

# Main content
st.markdown(f"<h1 style='text-align: center; color: #00209F;'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>🇭🇹 {t['year']}: {selected_year} 🇭🇹</h3>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([t["dashboard"], t["add_citizen"], t["search"]])

# ----------------------------------------------------------------------
# Dashboard: list citizens for selected year
# ----------------------------------------------------------------------
with tab1:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, matricule, full_name, minister_signed FROM citizens WHERE year = ?", (selected_year,))
    citizens = c.fetchall()
    conn.close()
    if citizens:
        for cit in citizens:
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                st.write(f"**{cit[1]}** - {cit[2]}")
            with col2:
                if cit[3]:
                    st.success(t["signed_by"] + " " + "✓")
                else:
                    st.warning(t["not_signed"])
            with col3:
                if st.button(t["edit_citizen"], key=f"edit_{cit[0]}"):
                    st.session_state.edit_id = cit[0]
                    st.rerun()
                if st.button(t["delete"], key=f"del_{cit[0]}"):
                    if st.checkbox(t["confirm_delete"], key=f"confirm_{cit[0]}"):
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute("DELETE FROM citizens WHERE id = ?", (cit[0],))
                        c.execute("DELETE FROM citizen_files WHERE citizen_id = ?", (cit[0],))
                        conn.commit()
                        conn.close()
                        st.success(t["citizen_deleted"])
                        st.rerun()
            st.divider()
    else:
        st.info(f"No citizens found for year {selected_year}. Use 'Add Citizen' tab.")

# ----------------------------------------------------------------------
# Add / Edit Citizen (with unique keys)
# ----------------------------------------------------------------------
with tab2:
    edit_mode = "edit_id" in st.session_state
    if edit_mode:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM citizens WHERE id = ?", (st.session_state.edit_id,))
        cit_data = c.fetchone()
        conn.close()
        if not cit_data:
            del st.session_state.edit_id
            st.rerun()
        st.subheader(t["edit_citizen"])
        key_suffix = "_edit"
    else:
        st.subheader(t["add_citizen"])
        key_suffix = ""

    with st.form(key=f"citizen_form{key_suffix}"):
        if edit_mode:
            cit_id = cit_data[0]
            matricule = st.text_input(t["matricule"], value=cit_data[2], key=f"matricule{key_suffix}")
            full_name = st.text_input(t["full_name"], value=cit_data[3], key=f"full_name{key_suffix}")
            birth_date = st.date_input(t["birth_date"], value=datetime.date.fromisoformat(cit_data[4]) if cit_data[4] else None, key=f"birth_date{key_suffix}")
            birth_place = st.text_input(t["birth_place"], value=cit_data[5] or "", key=f"birth_place{key_suffix}")
            gender = st.radio(t["gender"], [t["male"], t["female"]], index=0 if cit_data[6] == t["male"] else 1, key=f"gender{key_suffix}")
            cin_number = st.text_input(t["cin_number"], value=cit_data[7] or "", key=f"cin_number{key_suffix}")
            cin_delivery = st.date_input(t["cin_delivery"], value=datetime.date.fromisoformat(cit_data[8]) if cit_data[8] else None, key=f"cin_delivery{key_suffix}")
            cin_expiry = st.date_input(t["cin_expiry"], value=datetime.date.fromisoformat(cit_data[9]) if cit_data[9] else None, key=f"cin_expiry{key_suffix}")
            passport_number = st.text_input(t["passport_number"], value=cit_data[10] or "", key=f"passport_number{key_suffix}")
            passport_delivery = st.date_input(t["passport_delivery"], value=datetime.date.fromisoformat(cit_data[11]) if cit_data[11] else None, key=f"passport_delivery{key_suffix}")
            passport_expiry = st.date_input(t["passport_expiry"], value=datetime.date.fromisoformat(cit_data[12]) if cit_data[12] else None, key=f"passport_expiry{key_suffix}")
            license_number = st.text_input(t["license_number"], value=cit_data[13] or "", key=f"license_number{key_suffix}")
            license_delivery = st.date_input(t["license_delivery"], value=datetime.date.fromisoformat(cit_data[14]) if cit_data[14] else None, key=f"license_delivery{key_suffix}")
            license_expiry = st.date_input(t["license_expiry"], value=datetime.date.fromisoformat(cit_data[15]) if cit_data[15] else None, key=f"license_expiry{key_suffix}")
            voting_years = st.text_input(t["voting_years"], value=cit_data[16] or "", key=f"voting_years{key_suffix}")
            family_sponsorship = st.text_input(t["family_sponsorship"], value=cit_data[17] or "", key=f"family_sponsorship{key_suffix}")
            school_sponsorship = st.text_input(t["school_sponsorship"], value=cit_data[18] or "", key=f"school_sponsorship{key_suffix}")
            other_sponsorship = st.text_input(t["other_sponsorship"], value=cit_data[19] or "", key=f"other_sponsorship{key_suffix}")
            minister_signed = cit_data[20]
        else:
            matricule = st.text_input(t["matricule"], key=f"matricule{key_suffix}")
            full_name = st.text_input(t["full_name"], key=f"full_name{key_suffix}")
            birth_date = st.date_input(t["birth_date"], key=f"birth_date{key_suffix}")
            birth_place = st.text_input(t["birth_place"], key=f"birth_place{key_suffix}")
            gender = st.radio(t["gender"], [t["male"], t["female"]], key=f"gender{key_suffix}")
            cin_number = st.text_input(t["cin_number"], key=f"cin_number{key_suffix}")
            cin_delivery = st.date_input(t["cin_delivery"], key=f"cin_delivery{key_suffix}")
            cin_expiry = st.date_input(t["cin_expiry"], key=f"cin_expiry{key_suffix}")
            passport_number = st.text_input(t["passport_number"], key=f"passport_number{key_suffix}")
            passport_delivery = st.date_input(t["passport_delivery"], key=f"passport_delivery{key_suffix}")
            passport_expiry = st.date_input(t["passport_expiry"], key=f"passport_expiry{key_suffix}")
            license_number = st.text_input(t["license_number"], key=f"license_number{key_suffix}")
            license_delivery = st.date_input(t["license_delivery"], key=f"license_delivery{key_suffix}")
            license_expiry = st.date_input(t["license_expiry"], key=f"license_expiry{key_suffix}")
            voting_years = st.text_input(t["voting_years"], key=f"voting_years{key_suffix}")
            family_sponsorship = st.text_input(t["family_sponsorship"], key=f"family_sponsorship{key_suffix}")
            school_sponsorship = st.text_input(t["school_sponsorship"], key=f"school_sponsorship{key_suffix}")
            other_sponsorship = st.text_input(t["other_sponsorship"], key=f"other_sponsorship{key_suffix}")
            minister_signed = False

        uploaded_files = st.file_uploader(t["documents"], accept_multiple_files=True, type=["pdf","jpg","jpeg","png"], key=f"files{key_suffix}")

        if not minister_signed:
            minister_name = st.text_input(t["minister_signature"] + " (Name of Minister)", key=f"minister{key_suffix}")
            sign_button = st.form_submit_button(t["sign"])
        else:
            st.info(t["signed_by"] + " " + cit_data[21] if edit_mode else "")
            sign_button = False

        submitted = st.form_submit_button(t["save"] if not edit_mode else t["update"])

        if submitted:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            if edit_mode:
                c.execute("""UPDATE citizens SET
                    year=?, matricule=?, full_name=?, birth_date=?, birth_place=?, gender=?,
                    cin_number=?, cin_delivery=?, cin_expiry=?,
                    passport_number=?, passport_delivery=?, passport_expiry=?,
                    license_number=?, license_delivery=?, license_expiry=?,
                    voting_years=?, family_sponsorship=?, school_sponsorship=?, other_sponsorship=?
                    WHERE id=?""",
                    (selected_year, matricule, full_name, str(birth_date), birth_place, gender,
                     cin_number, str(cin_delivery), str(cin_expiry),
                     passport_number, str(passport_delivery), str(passport_expiry),
                     license_number, str(license_delivery), str(license_expiry),
                     voting_years, family_sponsorship, school_sponsorship, other_sponsorship, cit_id))
                st.success(t["citizen_updated"])
            else:
                c.execute("""INSERT INTO citizens (
                    year, matricule, full_name, birth_date, birth_place, gender,
                    cin_number, cin_delivery, cin_expiry,
                    passport_number, passport_delivery, passport_expiry,
                    license_number, license_delivery, license_expiry,
                    voting_years, family_sponsorship, school_sponsorship, other_sponsorship
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (selected_year, matricule, full_name, str(birth_date), birth_place, gender,
                 cin_number, str(cin_delivery), str(cin_expiry),
                 passport_number, str(passport_delivery), str(passport_expiry),
                 license_number, str(license_delivery), str(license_expiry),
                 voting_years, family_sponsorship, school_sponsorship, other_sponsorship))
                cit_id = c.lastrowid
                st.success(t["citizen_saved"])
            conn.commit()
            conn.close()

        if sign_button and minister_name:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("UPDATE citizens SET minister_signed=1, minister_signature_date=?, minister_name=? WHERE id=?",
                      (str(datetime.datetime.now()), minister_name, cit_id))
            conn.commit()
            conn.close()
            st.success("File validated by Minister.")
            st.rerun()

        if uploaded_files:
            os.makedirs("uploads", exist_ok=True)
            for file in uploaded_files:
                file_path = os.path.join("uploads", f"{cit_id}_{file.name}")
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO citizen_files (citizen_id, file_name, file_path, upload_date) VALUES (?,?,?,?)",
                          (cit_id, file.name, file_path, str(datetime.datetime.now())))
                conn.commit()
                conn.close()
            st.success(t["upload_success"])

    if edit_mode:
        if st.button("Cancel Edit"):
            del st.session_state.edit_id
            st.rerun()

# ----------------------------------------------------------------------
# Search tab
# ----------------------------------------------------------------------
with tab3:
    search_term = st.text_input("Search by name, matricule, or document ID")
    if search_term:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM citizens WHERE year=? AND (full_name LIKE ? OR matricule LIKE ?)", (selected_year, f"%{search_term}%", f"%{search_term}%"))
        results = c.fetchall()
        if results:
            for r in results:
                st.write(f"**{r[2]}** - {r[3]} - Signed: {'Yes' if r[20] else 'No'}")
                c2 = conn.cursor()
                c2.execute("SELECT file_name, upload_date FROM citizen_files WHERE citizen_id=?", (r[0],))
                files = c2.fetchall()
                if files:
                    st.write("Documents:")
                    for f in files:
                        st.write(f"  - {f[0]} (uploaded {f[1]})")
                st.divider()
        else:
            st.info("No records found.")
        conn.close()

# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------
st.markdown("---")
st.markdown(f"<center>{t['developer']} | {t['company']} | {t['email']} | {t['phone']}</center>", unsafe_allow_html=True)
