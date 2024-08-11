from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Cargar los datos desde el archivo JSON
def cargar_datos():
    try:
        with open('datos.json', 'r') as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

datos = cargar_datos()
compras = datos.get('compras', {}) if datos else {}
sugerencias = datos.get('sugerencias', {}) if datos else {}

def recomendar_juguetes(cliente):
    if cliente not in compras:
        return "Cliente no encontrado."
    
    juguetes_comprados = compras[cliente]
    recomendaciones = set()
    
    for juguete in juguetes_comprados:
        if juguete in sugerencias:
            recomendaciones.update(sugerencias[juguete])
    
    recomendaciones.difference_update(juguetes_comprados)
    
    return list(recomendaciones)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recomendaciones', methods=['POST'])
def recomendaciones():
    cliente = request.form.get('cliente').strip()
    recomendaciones = recomendar_juguetes(cliente)
    if isinstance(recomendaciones, str):
        return render_template('index.html', mensaje=recomendaciones)
    return render_template('index.html', cliente=cliente, recomendaciones=recomendaciones)

if __name__ == "__main__":
    app.run(debug=True)
