# BRAN Org - Schemas Oficiais de Dados Acadêmicos (`BRAN-Org/schemas`)

Este repositório centraliza os **JSON Schemas oficiais (v1)** da **BRAN Org** (**Brazilian Research Archive Network**). 

Estes esquemas atuam como **contratos de dados rígidos** para garantir a **fidelidade à fonte**, a **validação externa independente**, a **não-alucinação de metadados** e a **rastreabilidade de proveniência** de todas as bases de dados acadêmicas resgatadas pela organização.

---

## Os Três Pilares de Integridade da BRAN Org

1. **Fidelidade à fonte:** Garantia de que copiamos exatamente o que estava publicado no evento/portal original, preservando o dado bruto com hash criptográfico.
2. **Validação externa:** Confirmação independente dos dados contra infraestruturas abertas globais (Crossref, DataCite, OpenAlex, ORCID).
3. **Completude:** Rastreamento explícito da cobertura e lacunas inerentes do acervo (edições históricas físicas não digitalizadas, DOIs ausentes na origem).

---

## Schemas Disponíveis

| Schema | Versão | Arquivo | Descrição |
| :--- | :--- | :--- | :--- |
| **Artigos & Anais** | `v1` | [`schemas/article.v1.schema.json`](schemas/article.v1.schema.json) | Especificação de metadados para artigos, resumos e anais, incluindo objetos de `provenance`, `validation` e histórico de `corrections`. |
| **Eventos Acadêmicos** | `v1` | [`schemas/event.v1.schema.json`](schemas/event.v1.schema.json) | Especificação para simpósios, conferências e coleções de anais. |
| **Proveniência & Auditoria** | `v1` | [`schemas/provenance.v1.schema.json`](schemas/provenance.v1.schema.json) | Especificação de integridade de datasets (`source_url`, `raw_data_sha256`, `health_level`, métricas de resolução e validação externa). |

---

## Validação e Auditoria Local de Dados

### 1. Validação Estrutural e Integridade de Schemas
```bash
python3 scripts/validate_data.py
```

### 2. Auditoria Multi-Camadas e Resolução de DOIs (Crossref)
```bash
# Executar auditoria em dataset com geração de relatório Markdown
python3 scripts/audit_dataset.py --dataset /caminho/para/dataset.json --report-md AUDIT_REPORT.md
```

---

## Referência nos Repositórios da BRAN Org

Cada repositório de dados (como `abec-open-database`, `ebbc-open-database`) referencia este repositório no `$id` do schema:

```json
"$schema": "https://raw.githubusercontent.com/BRAN-Org/schemas/main/schemas/article.v1.schema.json"
```

---

## Submissão de Dados

Possui dados acadêmicos ou acervos científicos que gostaria de disponibilizar publicamente pela BRAN Org? Preencha o formulário de submissão:

 **[Formulário de Submissão de Datasets](https://forms.gle/jNBuP1mjyUXc6v1fA)**

