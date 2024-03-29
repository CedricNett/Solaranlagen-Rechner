import matplotlib
matplotlib.use('TkAgg') # Setze das Backend von Matplotlib auf 'TkAgg'

import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter.simpledialog import askstring

frame = None    # Globale Variable für den Rahmen

ertrag = 0.0    # Globale Variable für den erwarteten Ertrag

class SolarAnlage:
    def __init__(self, seite_l, seite_b, neigung, sonnenstunden, breitengrad, laengengrad, hoehe):
        self.seite_l = seite_l
        self.seite_b = seite_b
        self.neigung = neigung - 90  # Neigung in Grad
        self.sonnenstunden = sonnenstunden  # Sonnenstunden pro Tag
        self.nennleistung_pro_m2 = 0.2  # Nennleistung in kWp/m^2
        self.breitengrad = breitengrad  # Breitengrad des Standortes
        self.laengengrad = laengengrad  # Längengrad des Standortes
        self.hoehe = hoehe  # Höhe über dem Meeresspiegel

    def berechne_ertrag(self):
        # Anpassung basierend auf der Höhe
        # Eine einfache Annahme, dass höhere Höhen zu einem leicht erhöhten Ertrag führen könnten
        hoehe_faktor = 1 + (self.hoehe / 1000)  # Ein Faktor, der auf die Höhe basiert

        # Anpassung basierend auf dem Breitengrad
        breitengrad_faktor = math.cos(math.radians(self.breitengrad))  # Ein Faktor, der auf dem Breitengrad basiert

        # Sonnenstunden anpassen
        angepasste_sonnenstunden = self.sonnenstunden * hoehe_faktor * breitengrad_faktor

        # Restliche Berechnungen
        nennleistung = ((self.seite_l * self.seite_b) / 1000000) * self.nennleistung_pro_m2
        ertrag = nennleistung * angepasste_sonnenstunden
        faktor_neigung = math.cos(math.radians(self.neigung))
        ertrag *= faktor_neigung

        return ertrag

def berechne_ertrag_globally():
    global ertrag
    try:
        seite_l = float(seite_l_entry.get())
        seite_b = float(seite_b_entry.get())
        neigung = float(neigung_entry.get())
        sonnenstunden = float(sonnenstunden_entry.get())
        breitengrad = float(breitengrad_entry.get())
        laengengrad = float(laengengrad_entry.get())
        hoehe = float(hoehe_entry.get())

        solar_anlage = SolarAnlage(seite_l, seite_b, neigung, sonnenstunden, breitengrad, laengengrad, hoehe)
        ertrag = solar_anlage.berechne_ertrag()
        return ertrag

    except ValueError:
        return None

def on_submit():
    global ertrag
    ertrag = berechne_ertrag_globally()

    if ertrag is not None:
        output_label.config(text=f"Erwarteter Ertrag: {ertrag:.2f}".replace('.', ',') + " kWh pro Tag", foreground='green')
    else:
        output_label.config(text="Bitte gültige Zahlen eingeben!", foreground='red')


def plot_ertrag():
    try:
        seite_l = float(seite_l_entry.get())
        seite_b = float(seite_b_entry.get())
        neigung = float(neigung_entry.get())
        sonnenstunden = float(sonnenstunden_entry.get())
        breitengrad = float(breitengrad_entry.get())
        laengengrad = float(laengengrad_entry.get())
        hoehe = float(hoehe_entry.get())

        # Übergeben Sie alle erforderlichen Argumente an die SolarAnlage-Klasse
        solar_anlage = SolarAnlage(seite_l, seite_b, neigung, sonnenstunden, breitengrad, laengengrad, hoehe)
        
        tage = list(range(1, 31))
        ertragsliste = [solar_anlage.berechne_ertrag() for _ in tage]
        
        plt.figure(figsize=(10, 5))
        plt.plot(tage, ertragsliste, marker='o', linestyle='-')
        plt.title('Erwarteter Ertrag über 30 Tage')
        plt.xlabel('Tag')
        plt.ylabel('Ertrag (kWh)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except ValueError:
        output_label.config(text="Bitte gültige Zahlen eingeben!")


def zeige_tipps():
    tipps_text = """
    Tipps und Ratschläge zur optimalen Gestaltung und Platzierung von Solaranlagen:
    
    1. Ausrichtung: Die Ausrichtung der Solarpaneele sollte nach Süden zeigen, um die maximale Sonneneinstrahlung zu erhalten.

    2. Neigung: Die optimale Neigung der Paneele hängt vom geografischen Breitengrad ab. Ein typischer Richtwert liegt oft nahe dem Breitengrad des Standortes.

    3. Schatten: Vermeiden Sie Schattenwürfe auf den Solarmodulen, da diese die Effizienz der Anlage reduzieren können.

    4. Wartung: Regelmäßige Wartung und Reinigung der Module können die Leistung und Lebensdauer der Anlage erhöhen.
    
    Beachten Sie diese Tipps, um die Effizienz und Leistung Ihrer Solaranlage zu maximieren.
    """
    # Ein einfaches Dialogfenster zur Anzeige der Tipps
    tk.messagebox.showinfo("Tipps und Ratschläge", tipps_text)

def zeige_taschenrechner():
    # Funktion, um den Taschenrechner zu öffnen und das Ergebnis zurückzugeben
    def berechne_ausdruck(ausdruck):
        try:
            # Verwende die eval-Funktion, um den Ausdruck zu berechnen
            ergebnis = eval(ausdruck)
            return f"Ergebnis: {ergebnis}"
        except Exception as e:
            return f"Fehler: {str(e)}"

    # Zeige das Eingabefeld für den Taschenrechner an
    ausdruck = askstring("Taschenrechner", "Geben Sie einen mathematischen Ausdruck ein:")
    
    if ausdruck:
        # Berechne den Ausdruck und zeige das Ergebnis an
        ergebnis = berechne_ausdruck(ausdruck)
        tk.messagebox.showinfo("Taschenrechner", ergebnis)

# GUI erstellen
app = tk.Tk()
app.title("Solaranlagen & Balkonkraftwerke")

# Mindestgröße für das Fenster festlegen
app.minsize(400, 200)  # Beispielgrößen; Sie können dies nach Bedarf anpassen

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Konfiguration der Zeilen und Spalten für Skalierbarkeit
for i in range(10):  # Erhöht auf 10, um mehr Zeilen und Spalten zu haben
    frame.grid_rowconfigure(i, weight=1)
    frame.grid_columnconfigure(i, weight=1)

# Voreingestellte Werte für Breitengrad und Längengrad
DEFAULT_BREITENGRAD = "51.4818"
DEFAULT_LAENGENGRAD = "7.2162"
DEFAULT_HOEHE = "100" 

# Eingabe-Widgets
ttk.Label(frame, text="Seitenlänge L (mm):").grid(row=0, column=0, sticky=tk.W)
seite_l_entry = ttk.Entry(frame)
seite_l_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Seitenbreite (mm):").grid(row=1, column=0, sticky=tk.W)
seite_b_entry = ttk.Entry(frame)
seite_b_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Neigung (Grad):").grid(row=2, column=0, sticky=tk.W)
neigung_entry = ttk.Entry(frame)
neigung_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Sonnenstunden pro Tag:").grid(row=3, column=0, sticky=tk.W)
sonnenstunden_entry = ttk.Entry(frame)
sonnenstunden_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Breitengrad:").grid(row=4, column=0, sticky=tk.W)
breitengrad_entry = ttk.Entry(frame)
breitengrad_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))
breitengrad_entry.insert(0, DEFAULT_BREITENGRAD)

ttk.Label(frame, text="Längengrad:").grid(row=5, column=0, sticky=tk.W)
laengengrad_entry = ttk.Entry(frame)
laengengrad_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))
laengengrad_entry.insert(0, DEFAULT_LAENGENGRAD)

ttk.Label(frame, text="Höhe über dem Meeresspiegel (m):").grid(row=6, column=0, sticky=tk.W)
hoehe_entry = ttk.Entry(frame)
hoehe_entry.grid(row=6, column=1, sticky=(tk.W, tk.E))
hoehe_entry.insert(0, DEFAULT_HOEHE)

# Schaltfläche für Tipps und Ratschläge
tipps_button = ttk.Button(frame, text="Tipps und Ratschläge", command=zeige_tipps)
tipps_button.grid(row=7, columnspan=2, sticky=(tk.E, tk.N))

# Schaltfläche für den Taschenrechner
calculator_button = ttk.Button(frame, text="Taschenrechner", command=zeige_taschenrechner)
calculator_button.grid(row=7, columnspan=1, sticky=(tk.W, tk.N))

# Schaltfläche zum Berechnen
submit_button = ttk.Button(frame, text="Berechnen", command=on_submit)
submit_button.grid(row=8, columnspan=2, sticky=(tk.W, tk.E))

# Ausgabe-Label
output_label = ttk.Label(frame, text="", font=('Helvetica', 14, 'bold'), anchor='center')
output_label.grid(row=9, columnspan=2, sticky=(tk.W, tk.E))

# In der on_submit-Funktion (oder überall dort, wo du den Text des Labels aktualisierst):
output_label.config(text=f"Erwarteter Ertrag: {ertrag:.2f}".replace('.', ',') + " kWh pro Tag", foreground='green')

# Schaltfläche zum Anzeigen des Diagramms hinzufügen
plot_button = ttk.Button(frame, text="Ertrag über 30 Tage anzeigen", command=plot_ertrag)
plot_button.grid(row=10, columnspan=2)

app.mainloop()

## Echtzeit-Daten: Wenn möglich, integriere eine Funktion, die Echtzeitdaten von Sonneneinstrahlung, Temperatur oder anderen relevanten Parametern aus einer API oder einem externen Dienst abruft und in die Berechnungen einbezieht.

## Responsive Design: Stelle sicher, dass die Anwendung auf verschiedenen Bildschirmgrößen und Geräten gut funktioniert, indem du ein responsives Design verwendest.

## Integration von Speicherlösungen: Berücksichtige auch Speicherlösungen wie Batterien in den Berechnungen und zeige auf, wie diese die Rentabilität und Effizienz der Solaranlage beeinflussen können.
