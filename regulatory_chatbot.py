import openai
import streamlit as st
import requests
import PyPDF2

# OpenAI API-Key (ersetzen!)
OPENAI_API_KEY = "DEIN_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

st.title("🔍 KI Regulatory Affairs Chatbot")
st.subheader("Fragen zur MDR, IVDR oder FDA?")

# Nutzerfrage eingeben
user_input = st.text_input("Deine Frage:")

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
        return f"Fehler: {str(e)}"

# Antwort generieren
if st.button("Antwort erhalten"):
    if user_input:
        response = ask_gpt(user_input)
        st.write("💡 **Antwort:**")
        st.write(response)
    else:
        st.warning("Bitte eine Frage eingeben!")

# FDA-Datenabruf
def get_fda_data(device_name):
    """Ruft 510(k)-Daten für ein Gerät aus der FDA-Datenbank ab"""
    url = f"https://api.fda.gov/device/510k.json?search=device_name:{device_name}&limit=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            return data["results"][0]
        else:
            return "Keine FDA-Daten gefunden."
    else:
        return "Fehler beim Abruf der FDA-Daten."

device_name = st.text_input("FDA-Zulassung für Produkt suchen:")
if st.button("FDA-Check"):
    result = get_fda_data(device_name)
    st.write(result)

# Dokumentenprüfung
st.subheader("📄 Dokumentenprüfung für Regulatory Compliance")
uploaded_file = st.file_uploader("Lade dein PDF hoch", type="pdf")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.write("📄 **Dokumenteninhalt (Auszug):**")
    st.write(text[:500])

    if st.button("Analyse starten"):
        response = ask_gpt(f"Prüfe dieses Dokument auf MDR-Compliance: {text[:2000]}")
        st.write("💡 **Ergebnisse der Analyse:**")
        st.write(response)

st.subheader("✅ MDR-Checkliste")
st.write("""
- ✅ Klinische Bewertung nach MDR, Anhang XIV durchgeführt?
- ✅ UDI-System implementiert?
- ✅ Post-Market Surveillance (PMS) Plan vorhanden?
- ✅ Risikoanalyse nach ISO 14971 abgeschlossen?
- ✅ Konformitätserklärung nach MDR Artikel 19 erstellt?
""")
