#!/usr/bin/env python3
"""
Script de Validação de Dados e Integrity Check - BRAN Org Standard
Garante que arquivos de proveniência e datasets estão no padrão sem depender obrigatoriamente de pacotes externos,
mas utilizando jsonschema quando disponível para validação estrita do contrato formal.
"""

import os
import sys
import json
import hashlib
import glob

def calculate_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def validate_provenance(provenance_path, schema_path, data_dir=None):
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

    # Validação formal com jsonschema se disponível
    if os.path.exists(schema_path):
        try:
            import jsonschema
            with open(schema_path, "r", encoding="utf-8") as sf:
                schema = json.load(sf)
            jsonschema.validate(instance=data, schema=schema)
            print("  ✓ Validação formal contra provenance.v1.schema.json passou!")
        except ImportError:
            pass
        except Exception as e:
            print(f"❌ Erro de validação de schema em {provenance_path}: {e}")
            return False

    # Se houver pasta data, checar integridade de contagem e hash
    if data_dir and os.path.exists(data_dir):
        json_files = glob.glob(os.path.join(data_dir, "*.json"))
        total_items = 0
        for jf in json_files:
            try:
                with open(jf, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        total_items += len(content)
                        calculated_hash = calculate_sha256(jf)
                        if data.get("raw_data_sha256"):
                            if calculated_hash.lower() == data["raw_data_sha256"].lower():
                                print(f"  ✓ Hash SHA-256 verificado com sucesso para {os.path.basename(jf)}: {calculated_hash[:16]}...")
                            else:
                                print(f"  ⚠️ Aviso SHA-256: Calculado ({calculated_hash}) != Declarado ({data['raw_data_sha256']})")
            except Exception as e:
                print(f"⚠️ Aviso ao verificar arquivo {jf}: {e}")

        if data.get("total_records") != total_items and total_items > 0:
            print(f"  ⚠️ Discrepância de contagem: provenance declara {data.get('total_records')}, mas data/ contém {total_items} registros.")

    print(f"✅ Proveniência {provenance_path} validada com sucesso! Nível de Saúde: {data['health_level']}")
    return True

def validate_articles(data_dir, schema_path):
    if not os.path.exists(data_dir):
        return True

    json_files = glob.glob(os.path.join(data_dir, "*.json"))
    if not json_files:
        return True

    print(f"🔍 Validando datasets acadêmicos em {data_dir}...")
    schema = None
    if os.path.exists(schema_path):
        try:
            with open(schema_path, "r", encoding="utf-8") as sf:
                schema = json.load(sf)
        except Exception as e:
            print(f"⚠️ Erro ao carregar schema de artigos: {e}")

    try:
        import jsonschema
        can_validate_strict = True
    except ImportError:
        can_validate_strict = False

    for jf in json_files:
        print(f"  Auditando {os.path.basename(jf)}...")
        with open(jf, "r", encoding="utf-8") as f:
            records = json.load(f)

        if not isinstance(records, list):
            records = [records]

        print(f"  Total de registros a verificar: {len(records)}")

        if can_validate_strict and schema:
            try:
                jsonschema.validate(instance=records, schema=schema)
                print(f"  ✅ {os.path.basename(jf)}: 100% conforme ao article.v1.schema.json!")
            except Exception as e:
                print(f"❌ Falha de validação em {os.path.basename(jf)}: {e.message}")
                return False
        else:
            for idx, item in enumerate(records):
                if not item.get("title"):
                    print(f"❌ Item #{idx+1} sem título")
                    return False
                if not item.get("authors"):
                    print(f"❌ Item #{idx+1} sem autores")
                    return False
            print(f"  ✅ {os.path.basename(jf)}: validação estrutural básica concluída.")

    return True

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prov_file = os.path.join(base_dir, "provenance.json")
    prov_schema = os.path.join(base_dir, "schemas", "provenance.v1.schema.json")
    art_schema = os.path.join(base_dir, "schemas", "article.v1.schema.json")
    data_dir = os.path.join(base_dir, "data")
    
    success = True
    if os.path.exists(prov_file):
        success = validate_provenance(prov_file, prov_schema, data_dir) and success
    
    if os.path.exists(data_dir):
        success = validate_articles(data_dir, art_schema) and success
        
    sys.exit(0 if success else 1)
