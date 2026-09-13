# 📐 BRAN Org - Schemas Oficiais de Dados Acadêmicos (`BRAN-Org/schemas`)

Este repositório centraliza os **JSON Schemas oficiais (v1)** da **BRAN Org** (**Brazilian Research Archive Network**). 

Estes esquemas atuam como **contratos de dados rígidos** para garantir o **compromisso com a verdade**, a não-alucinação de metadados e a interoperabilidade de todas as bases de dados acadêmicas brasileiras resgatadas pela organização.

---

## 📜 Schemas Disponíveis

| Schema | Versão | Arquivo | Descrição |
| :--- | :--- | :--- | :--- |
| **Artigos & Anais** | `v1` | [`schemas/article.v1.schema.json`](schemas/article.v1.schema.json) | Especificação de metadados para artigos científicos, trabalhos de congressos e anais resgatados. |
| **Eventos Acadêmicos** | `v1` | [`schemas/event.v1.schema.json`](schemas/event.v1.schema.json) | Especificação para simpósios, conferências e coleções de anais. |
| **Proveniência & Auditoria** | `v1` | [`schemas/provenance.v1.schema.json`](schemas/provenance.v1.schema.json) | Especificação obrigatória de proveniência (`source_url`, `scraped_at`, `raw_data_sha256`, `health_level`). |

---

## 🧪 Validação Local de Dados

Você pode validar seus arquivos JSON contra estes esquemas executando o script incluído:

```bash
python3 scripts/validate_data.py
```

---

## 🔗 Referência nos Repositórios da BRAN Org

Cada repositório de dados (como `abec-open-database`, `ebbc-open-database`) referencia este repositório no `$id` do schema:

```json
"$schema": "https://raw.githubusercontent.com/BRAN-Org/schemas/main/schemas/article.v1.schema.json"
```
