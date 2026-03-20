#!/usr/bin/env python3
"""
Convierte el archivo Excel de inventario a JSON para el dashboard.
Uso: python scripts/excel_to_json.py
"""
import pandas as pd
import json
from datetime import datetime
import os
import sys

EXCEL_FILE = "Inventario_20_marzo.xlsx"
OUTPUT_FILE = "data/inventario.json"

def convert():
    if not os.path.exists(EXCEL_FILE):
        print(f"ERROR: No se encontró {EXCEL_FILE}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_excel(EXCEL_FILE)
    df = df.fillna({'Centro': 'N/A', 'Almacén': 0})
    df['Material'] = df['Material'].fillna(0).astype(int).astype(str)
    df['Almacén'] = df['Almacén'].astype(int)
    df['Libre utilización'] = df['Libre utilización'].fillna(0).astype(int)

    por_centro = (
        df.groupby('Centro')
        .agg(items=('Libre utilización', 'count'), stock_total=('Libre utilización', 'sum'))
        .reset_index().to_dict('records')
    )
    for r in por_centro:
        r['stock_total'] = int(r['stock_total'])

    por_almacen = (
        df.groupby('Almacén')
        .agg(items=('Libre utilización', 'count'), stock_total=('Libre utilización', 'sum'))
        .reset_index().to_dict('records')
    )
    for r in por_almacen:
        r['Almacén'] = int(r['Almacén'])
        r['stock_total'] = int(r['stock_total'])

    top_m = (
        df.groupby('Texto breve de material')['Libre utilización']
        .sum().sort_values(ascending=False).head(15).reset_index()
    )
    top_list = [
        {'material': r['Texto breve de material'], 'stock': int(r['Libre utilización'])}
        for _, r in top_m.iterrows()
    ]

    records = [
        {
            'material': str(row['Material']),
            'descripcion': str(row['Texto breve de material']),
            'centro': str(row['Centro']),
            'almacen': int(row['Almacén']),
            'stock': int(row['Libre utilización'])
        }
        for _, row in df.iterrows()
    ]

    output = {
        'fecha_actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'resumen': {
            'total_registros': len(df),
            'con_stock': int((df['Libre utilización'] > 0).sum()),
            'sin_stock': int((df['Libre utilización'] == 0).sum()),
            'stock_total': int(df['Libre utilización'].sum())
        },
        'por_centro': por_centro,
        'por_almacen': por_almacen,
        'top_materiales': top_list,
        'registros': records
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON generado: {OUTPUT_FILE} ({len(records)} registros)")

if __name__ == '__main__':
    convert()
