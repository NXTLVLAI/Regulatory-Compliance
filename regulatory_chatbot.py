import openai
import streamlit as st
import requests
import pdfplumber

# OpenAI API-Key (ersetzen!)
OPENAI_API_KEY = "DEIN_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="KI Regulatory Affairs Chatbot", layout="wide")
st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio("Wähle eine Funktion:", ["🔍 Regulatory Chat", "📊 FDA-Suche", "📄 Dokumentenprüfung", "✅ MDR-Checkliste"])

# GPT-4 Kommunikation
def ask_gpt(question):
    """Kommunikation mit GPT-4 zur Beantwortung von Regulatory-Fragen"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Du bist ein Experte für Regulatory Affairs in der Medizintechnik."},
                      {"role": "user", "content": question}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Fehler: {str(e)}"

# 📌 Regulatory Chat
if page == "🔍 Regulatory Chat":
    st.title("🔍 KI Regulatory Affairs Chatbot")
    user_input = st.text_input("Deine Frage:")
    if st.button("Antwort erhalten"):
        if user_input:
            response = ask_gpt(user_input)
            st.write("💡 **Antwort:**")
            st.write(response)
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
            shortened_text = text[:2000]  # Begrenzung für GPT
            response = ask_gpt(f"Prüfe dieses Dokument auf MDR-Compliance: {shortened_text}")
            st.write("💡 **Ergebnisse der Analyse:**")
            st.write(response)

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
