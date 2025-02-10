import streamlit as st
import requests
import pdfplumber

# OpenAI API-Key (ersetzen!)
OPENAI_API_KEY = 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

st.set_page_config(page_title="KI Regulatory Affairs Chatbot", layout="wide")
st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio("Wähle eine Funktion:", ["🔍 Regulatory Chat", "📊 FDA-Suche", "📄 Dokumentenprüfung", "✅ MDR-Checkliste"])

# 📌 Regulatory Chat
if page == "🔍 Regulatory Chat":
    st.title("🔍 KI Regulatory Affairs Chatbot")
    user_input = st.text_input("Deine Frage:")
    if st.button("Antwort erhalten"):
        if user_input:
            st.write("💡 **Antwort:**")
            st.write("(Antwort von KI würde hier erscheinen)")
        else:
            st.warning("Bitte eine Frage eingeben!")

# 📊 FDA-Suche
elif page == "📊 FDA-Suche":
    st.title("📊 FDA-Zulassung prüfen")
    device_name = st.text_input("FDA-Zulassung für Produkt suchen:")
    
    def get_fda_data(device_name):
        """Ruft 510(k)-Daten für ein Gerät aus der FDA-Datenbank ab"""
        url = f"https://api.fda.gov/device/510k.json?search=device_name:{device_name}&limit=1"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                return data["results"][0]
            else:
                return {"message": "⚠️ Keine FDA-Daten für dieses Gerät gefunden. Bitte überprüfe den Namen."}
        else:
            return {"message": "❌ Fehler beim Abruf der FDA-Daten."}
    
    if st.button("FDA-Check"):
        result = get_fda_data(device_name)
        st.write(result)

# 📄 Dokumentenprüfung
elif page == "📄 Dokumentenprüfung":
    st.title("📄 Dokumentenprüfung für Regulatory Compliance")
    uploaded_file = st.file_uploader("Lade dein PDF hoch", type="pdf")
    
    def extract_text_from_pdf(file):
        with pdfplumber.open(file) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        with st.expander("📄 Dokumenteninhalt anzeigen"):
            st.write(text[:1000])

        if st.button("Analyse starten"):
            shortened_text = text[:2000]  # Begrenzung für KI
            st.write("💡 **Ergebnisse der Analyse:**")
            st.write("(Analyseergebnisse würden hier erscheinen)")

# ✅ MDR-Checkliste
elif page == "✅ MDR-Checkliste":
    st.title("✅ MDR-Checkliste")
    checklist = {
        "Klinische Bewertung nach MDR, Anhang XIV durchgeführt?": False,
        "UDI-System implementiert?": False,
        "Post-Market Surveillance (PMS) Plan vorhanden?": False,
        "Risikoanalyse nach ISO 14971 abgeschlossen?": False,
        "Konformitätserklärung nach MDR Artikel 19 erstellt?": False,
    }
    
    for key in checklist.keys():
        checklist[key] = st.checkbox(key, value=False)
    
    if all(checklist.values()):
        st.success("✅ Alle Anforderungen erfüllt!")
    else:
        st.warning("⚠️ Nicht alle Punkte sind erfüllt. Bitte überprüfe die offenen Punkte.")
