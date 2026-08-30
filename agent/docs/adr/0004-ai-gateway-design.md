# ADR-0004: AI Gateway Design
Status: Accepted
Date: 2026-08-22
Supersedes: -
Superseded by: -

## Context
Bisnis logic ALR tidak boleh bergantung pada satu provider AI (DeepSeek dipilih sebagai daily driver, tapi harus bisa diganti/di-mix tanpa mengubah kode di luar gateway). Setiap pemanggilan AI juga harus tertelusur ke cost/credit.

## Decision

### Alur wajib untuk setiap pemanggilan AI
```
AITask (enum + payload)
   │
   ▼
Cost Estimation      -- estimasi token/biaya sebelum eksekusi
   │
   ▼
Model Selection       -- routing table: task_type → {provider, model}
   │
   ▼
Context Retrieval      -- RAG dari Content Memory kalau task butuh (lihat Fase 2 content pipeline)
   │
   ▼
Prompt Assembly        -- PromptTemplate (versioned) + context + user input
   │
   ▼
Generation              -- panggil provider adapter
   │
   ▼
Output Validation      -- validasi terhadap output_schema (serde/JSON schema)
   │
   ▼
Usage Tracking          -- tulis ke ai_tasks + transactions (credit)
```

### AITask enum (final untuk MVP, tambahan lewat ADR baru)
```typescript
type AITask =
  | "GrammarEvaluation"
  | "WritingEvaluation"
  | "SpeakingEvaluation"
  | "PronunciationEvaluation"
  | "LessonGeneration"
  | "QuestionGeneration"
  | "CurriculumGeneration"
  | "ExplanationGeneration"
  | "OCRToQuestion"
  | "LiveTutor"
  | "ContentValidation"; // dipakai AI Content QA Agent
```

### Provider abstraction (interface, bukan hardcode)
```typescript
interface AIProvider {
  generate(req: GenerationRequest): Promise<GenerationResponse>;
  estimateCost(req: GenerationRequest): CostEstimate;
}

class DeepSeekProvider implements AIProvider { /* ... */ }
class OpenAIProvider implements AIProvider { /* ... */ } // disiapkan interface-nya walau belum dipakai MVP
```

### Routing table (default MVP — hidup di config, bukan hardcode di kode)
| AITask | Provider default | Fallback |
|---|---|---|
| GrammarEvaluation | deepseek | - |
| WritingEvaluation | deepseek | - |
| SpeakingEvaluation | deepseek (dgn audio transcript dulu) | - |
| LessonGeneration | deepseek | - |
| QuestionGeneration | deepseek | - |
| CurriculumGeneration | deepseek | - |
| ContentValidation | deepseek (model lebih murah/cepat) | - |
| LiveTutor | deepseek | - |

Fallback provider kosong di MVP — kolomnya tetap ada di skema supaya nambah fallback nanti tidak perlu migration, cukup isi config.

### PromptTemplate (versioned, bukan string hardcode di kode)
```typescript
interface PromptTemplate {
  id: string; // "writing_evaluation_v1"
  task: AITask;
  version: string;
  systemPrompt: string;
  userPromptTemplate: string; // placeholder {{...}}
  outputSchema: unknown; // JSON schema
  model: string;
  temperature: number;
  maxTokens: number;
}
```
Disimpan sebagai file/config, bukan di database — supaya versioning lewat git, bisa di-review sebagai PR biasa.

### Output validation
Setiap response provider WAJIB divalidasi terhadap `output_schema` sebelum dipakai; gagal validasi → status `ai_tasks.status = failed`, tidak ada credit charge (lihat ADR-0005), dan tidak pernah langsung ditampilkan mentah ke user untuk task yang sifatnya generative-untuk-publish (lesson/question generation) — selalu lewat human review (lihat pipeline Content Factory di roadmap fase 2).

## Alternatives considered
- **Panggil DeepSeek API langsung dari business logic** — ditolak keras, mengunci ALR ke 1 provider dan menyulitkan cost tracking terpusat.
- **Simpan prompt di database supaya bisa diedit non-technical** — ditunda; untuk MVP prompt di git lebih aman untuk versioning & review, bisa dipindah ke DB-managed kalau ada kebutuhan non-engineer mengedit prompt.

## Consequences
- (+) Ganti/nambah provider = implementasi 1 trait baru + update routing table, tanpa sentuh business logic lain.
- (+) Semua biaya AI tertelusur by design (setiap task punya row di `ai_tasks`).
- (−) Overhead tambahan (assembly, validation) di setiap panggilan — diterima sebagai trade-off untuk auditability & fleksibilitas provider.
