import requests
import json
import time
import os
from statistics import mean

print("Iniciando pruebas...")

inicio_total = time.time()

url = "http://localhost:11434/api/generate"

with open("../prompts/suite.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)

resultados = []
tiempos = []

for item in prompts:

    print(f"Procesando: {item['categoria']}")

    inicio = time.time()

    respuesta = requests.post(
        url,
        json={
            "model": "mistral:latest",
            "prompt": item["prompt"],
            "stream": False,
            "options": {
                "num_predict": 80
            }
        },
        timeout=180
    )

    fin = time.time()

    tiempo_respuesta = round(fin - inicio, 2)
    tiempos.append(tiempo_respuesta)

    datos = respuesta.json()

    resultados.append({
        "categoria": item["categoria"],
        "prompt": item["prompt"],
        "respuesta": datos["response"],
        "tiempo_segundos": tiempo_respuesta
    })

os.makedirs("../results", exist_ok=True)

with open("../results/resultados.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=4, ensure_ascii=False)

fin_total = time.time()

tiempo_total = round(fin_total - inicio_total, 2)
tiempo_promedio = round(mean(tiempos), 2)

metricas = {
    "cantidad_pruebas": len(prompts),
    "tiempo_total_segundos": tiempo_total,
    "tiempo_promedio_segundos": tiempo_promedio,
    "tiempos_individuales": tiempos
}

with open("../results/metricas.json", "w", encoding="utf-8") as f:
    json.dump(metricas, f, indent=4, ensure_ascii=False)

print("\n========== RESUMEN ==========")
print(f"Cantidad de pruebas: {len(prompts)}")
print(f"Tiempo total: {tiempo_total} segundos")
print(f"Tiempo promedio: {tiempo_promedio} segundos")
print("=============================")

print("Archivo resultados.json guardado")
print("Archivo metricas.json guardado")
print("Pruebas completadas")