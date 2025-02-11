import random

def chatbot():
    print("Willkommen zum Regulatorik-Chatbot für Medizinprodukte!")
    print("Stellen Sie Ihre Frage oder geben Sie 'exit' ein, um das Gespräch zu beenden.")
    
    antworten = {
        "was ist die MDR?": "Die Medical Device Regulation (MDR, Verordnung (EU) 2017/745) ist die europäische Verordnung für Medizinprodukte.",
        "was ist ein Klasse IIa Produkt?": "Ein Klasse IIa Medizinprodukt hat ein mittleres Risiko und unterliegt einer Konformitätsbewertung durch eine Benannte Stelle.",
        "was ist ein Benannte Stelle?": "Eine Benannte Stelle ist eine unabhängige Organisation, die die Konformität eines Medizinprodukts mit der MDR überprüft.",
        "welche Normen gelten für Medizinprodukte?": "Zu den wichtigsten Normen gehören ISO 13485 für Qualitätsmanagement und ISO 14971 für Risikomanagement."
    }
    
    while True:
        user_input = input("Frage: ").lower()
        if user_input == "exit":
            print("Vielen Dank für das Gespräch!")
            break
        
        antwort = antworten.get(user_input, "Das kann ich leider nicht beantworten. Bitte stellen Sie eine andere Frage.")
        print("Antwort:", antwort)

if __name__ == "__main__":
    chatbot()
