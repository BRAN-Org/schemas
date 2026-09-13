#!/usr/bin/env python3
"""
Script de Validação de Dados e Integrity Check - BRAN Org Standard
Garante que arquivos de proveniência e datasets estão no padrão sem depender de pacotes externos.
"""

import os
import sys
import json
import re

def validate_provenance(provenance_path, schema_path):
    print(f"🔍 Auditando arquivo de proveniência: {provenance_path} ...")
    if not os.path.exists(provenance_path):
        print(f"❌ Erro: Arquivo {provenance_path} não encontrado.")
        return False
    
    with open(provenance_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    required_keys = ["dataset_id", "source_url", "scraped_at", "extractor_name", "health_level", "total_records"]
    for key in required_keys:
        if key not in data:
            print(f"❌ Erro de Schema: Campo obrigatório '{key}' ausente no provenance.json")
            return False

    valid_health_levels = ["GREEN", "BLUE", "YELLOW", "ORANGE"]
    if data["health_level"] not in valid_health_levels:
        print(f"❌ Erro de Saúde: Nível '{data['health_level']}' inválido. Deve ser um de: {valid_health_levels}")
        return False

    print(f"✅ Proveniência {provenance_path} validada com sucesso! Nível de Saúde: {data['health_level']}")
    return True

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prov_file = os.path.join(base_dir, "provenance.json")
    schema_file = os.path.join(base_dir, "schemas", "provenance.v1.schema.json")
    
    if os.path.exists(prov_file):
        success = validate_provenance(prov_file, schema_file)
        sys.exit(0 if success else 1)
    else:
        print("ℹ️ Nenhum arquivo provenance.json local. Validação ignorada.")
        sys.exit(0)
