# ALR Domain Model — ERD Final v1

> **Backend sedang dimigrasi dari Rust ke Go (ADR-0020).** Skema tidak berubah. Berkas migrasi yang sama (`0000`–`0096`, lalu seterusnya) ada di `titian-backend-rust/migrations/` dan `titian-backend-go/db/migrations/`; tabel pencatatnya tetap `_sqlx_migrations`. Migrasi baru ditulis sekali dan disalin ke keduanya sampai Rust diarsipkan.

Rujukan: ADR-0001. File ini adalah representasi teknis (SQL) dari ADR-0001, dipakai langsung sebagai dasar migration P0-007.

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USER_ORGANIZATION_ROLES : has
    USERS ||--o{ USER_ORGANIZATION_ROLES : has
    SUBJECTS ||--o{ CURRICULA : has
    CURRICULA ||--o{ LEVELS : has
    LEVELS ||--o{ UNITS : has
    UNITS ||--o{ LESSONS : has
    LESSONS ||--o{ CONTENT_BLOCKS : has
    SUBJECTS ||--o{ CONCEPTS : has
    LESSONS ||--o{ LESSON_CONCEPTS : maps
    CONCEPTS ||--o{ LESSON_CONCEPTS : maps
    SUBJECTS ||--o{ QUESTION_BANKS : has
    QUESTION_BANKS ||--o{ QUESTIONS : has
    QUESTIONS ||--o{ QUESTION_CONCEPTS : maps
    CONCEPTS ||--o{ QUESTION_CONCEPTS : maps
    ASSESSMENTS ||--o{ ASSESSMENT_QUESTIONS : has
    QUESTIONS ||--o{ ASSESSMENT_QUESTIONS : used_in
    USERS ||--o{ ATTEMPTS : makes
    ASSESSMENTS ||--o{ ATTEMPTS : has
    ATTEMPTS ||--o{ EVALUATIONS : has
    EVALUATIONS ||--o{ FEEDBACK : has
    USERS ||--o{ LEARNING_EVENTS : generates
    USERS ||--o{ MASTERIES : has
    CONCEPTS ||--o{ MASTERIES : tracked_by
    USERS ||--o{ FRSS_SCHEDULE : has
    USERS ||--|| CREDITS : has
    USERS ||--o{ TRANSACTIONS : has
    USERS ||--o{ AI_TASKS : requests
    ASSESSMENTS ||--o{ EXAM_SESSIONS : has
    EXAM_SESSIONS ||--o{ PROCTORING_SESSIONS : has
    PROCTORING_SESSIONS ||--o{ PROCTORING_EVENTS : logs
    PROCTORING_POLICIES ||--o{ PROCTORING_SESSIONS : governs
```

## Migration SQL (PostgreSQL) — siap dipakai P0-007

```sql
-- === Identity & Organization ===
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('platform','school','tutor_org')),
    settings JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    google_id TEXT UNIQUE,
    name TEXT NOT NULL,
    avatar_url TEXT,
    locale TEXT NOT NULL DEFAULT 'id',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE user_organization_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    role TEXT NOT NULL CHECK (role IN (
        'platform_admin','org_owner','academic_director','curriculum_developer',
        'reviewer','teacher','tutor','student','parent')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(user_id, organization_id, role)
);

-- === Curriculum Tree ===
CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE curricula (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID NOT NULL REFERENCES subjects(id),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    framework TEXT NOT NULL CHECK (framework IN ('cefr','cambridge','kurikulum_id','custom')),
    version INT NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','published','archived'))
);

CREATE TABLE levels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    curriculum_id UUID NOT NULL REFERENCES curricula(id),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    order_index INT NOT NULL
);

CREATE TABLE units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    level_id UUID NOT NULL REFERENCES levels(id),
    code TEXT NOT NULL,
    title TEXT NOT NULL,
    order_index INT NOT NULL
);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_id UUID NOT NULL REFERENCES units(id),
    title TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('learn','practice','speaking','writing','review','assessment')),
    order_index INT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','in_review','published','archived')),
    version INT NOT NULL DEFAULT 1,
    superseded_by UUID REFERENCES lessons(id),  -- ADR-0008, added migration 0012
    qa_report JSONB  -- P2-014, added migration 0015
);

CREATE TABLE content_blocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lesson_id UUID NOT NULL REFERENCES lessons(id),
    type TEXT NOT NULL,
    order_index INT NOT NULL,
    data JSONB NOT NULL DEFAULT '{}',
    raw_source TEXT
);

-- === Concept Graph ===
CREATE TABLE concepts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID NOT NULL REFERENCES subjects(id),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('grammar','vocabulary','skill','pronunciation')),
    parent_concept_id UUID REFERENCES concepts(id),  -- ADR-0007, added migration 0011; containment hierarchy, distinct from concept_prerequisites below
    indonesian_difficulty_tag TEXT,  -- P2-012, added migration 0014; free-form for now
    UNIQUE(subject_id, code)
);

CREATE TABLE lesson_concepts (
    lesson_id UUID NOT NULL REFERENCES lessons(id),
    concept_id UUID NOT NULL REFERENCES concepts(id),
    weight FLOAT NOT NULL DEFAULT 1.0,
    PRIMARY KEY (lesson_id, concept_id)
);

CREATE TABLE concept_prerequisites (
    concept_id UUID NOT NULL REFERENCES concepts(id),
    prerequisite_concept_id UUID NOT NULL REFERENCES concepts(id),
    PRIMARY KEY (concept_id, prerequisite_concept_id)
);

-- === Question Bank ===
CREATE TABLE question_banks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID NOT NULL REFERENCES subjects(id),
    name TEXT NOT NULL
);

CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bank_id UUID NOT NULL REFERENCES question_banks(id),
    type TEXT NOT NULL,
    difficulty FLOAT NOT NULL DEFAULT 0.5 CHECK (difficulty >= 0 AND difficulty <= 1),
    data JSONB NOT NULL,
    correct_answer JSONB NOT NULL,
    explanation JSONB,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','in_review','published','archived')),
    version INT NOT NULL DEFAULT 1,
    superseded_by UUID REFERENCES questions(id),  -- ADR-0008, added migration 0012
    qa_report JSONB,  -- P2-014, added migration 0015
    cefr_tag TEXT CHECK (cefr_tag IN ('a1','a2','b1','b2','c1','c2'))  -- P2-014, added migration 0015
);

CREATE TABLE question_concepts (
    question_id UUID NOT NULL REFERENCES questions(id),
    concept_id UUID NOT NULL REFERENCES concepts(id),
    PRIMARY KEY (question_id, concept_id)
);

-- === Assessment & Attempt ===
CREATE TABLE assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type TEXT NOT NULL CHECK (type IN ('unit_test','level_assessment','mock_exam','ielts','toefl','pte')),
    title TEXT NOT NULL,
    config JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE assessment_questions (
    assessment_id UUID NOT NULL REFERENCES assessments(id),
    question_id UUID NOT NULL REFERENCES questions(id),
    order_index INT NOT NULL,
    points FLOAT NOT NULL DEFAULT 1.0,
    PRIMARY KEY (assessment_id, question_id)
);

CREATE TABLE attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    assessment_id UUID REFERENCES assessments(id),
    lesson_id UUID REFERENCES lessons(id),
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    submitted_at TIMESTAMPTZ,
    answers JSONB NOT NULL DEFAULT '{}',
    score FLOAT,
    status TEXT NOT NULL DEFAULT 'in_progress' CHECK (status IN ('in_progress','submitted','evaluated')),
    question_snapshot JSONB,  -- ADR-0008, added migration 0012; question content as of submit time
    CHECK (assessment_id IS NOT NULL OR lesson_id IS NOT NULL)
);
CREATE INDEX idx_attempts_user ON attempts(user_id);

-- === Evaluation & Feedback ===
CREATE TABLE rubrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    criteria JSONB NOT NULL
);

CREATE TABLE evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL REFERENCES attempts(id),
    evaluator_type TEXT NOT NULL CHECK (evaluator_type IN ('ai','human')),
    rubric_id UUID REFERENCES rubrics(id),
    scores JSONB NOT NULL DEFAULT '{}',
    evidence JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID NOT NULL REFERENCES evaluations(id),
    type TEXT NOT NULL CHECK (type IN ('annotation','comment','voice_note')),
    content TEXT NOT NULL,
    position JSONB,
    created_by UUID REFERENCES users(id)
);

-- === Learning Engine ===
CREATE TABLE learning_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    event_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_learning_events_user_time ON learning_events(user_id, created_at);
CREATE INDEX idx_learning_events_entity ON learning_events(entity_type, entity_id);

CREATE TABLE masteries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    concept_id UUID NOT NULL REFERENCES concepts(id),
    score FLOAT NOT NULL DEFAULT 0,
    confidence FLOAT NOT NULL DEFAULT 0,
    last_reviewed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(user_id, concept_id)
);

CREATE TABLE frss_schedule (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    concept_id UUID NOT NULL REFERENCES concepts(id),
    interval_days FLOAT NOT NULL DEFAULT 1.0,
    ease_factor FLOAT NOT NULL DEFAULT 2.5,
    due_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_result TEXT CHECK (last_result IN ('recalled','partial','forgot')),
    UNIQUE(user_id, concept_id)
);
CREATE INDEX idx_frss_due ON frss_schedule(user_id, due_at);

-- === Economy ===
CREATE TABLE credits (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    balance BIGINT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    type TEXT NOT NULL CHECK (type IN ('earn','spend','purchase','refund','payout_earned','payout_withdrawn')),
    amount BIGINT NOT NULL,
    reference TEXT,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_transactions_user ON transactions(user_id);

CREATE TABLE ai_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    task_type TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_id TEXT NOT NULL,
    tokens_used INT,
    cost NUMERIC,
    status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued','running','done','failed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- === Exam Runtime & Proctoring ===
CREATE TABLE exam_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID NOT NULL REFERENCES assessments(id),
    user_id UUID NOT NULL REFERENCES users(id),
    status TEXT NOT NULL DEFAULT 'not_started' CHECK (status IN ('not_started','in_progress','submitted','timed_out')),
    started_at TIMESTAMPTZ,
    submitted_at TIMESTAMPTZ
);

CREATE TABLE proctoring_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_type TEXT NOT NULL,
    camera TEXT NOT NULL DEFAULT 'off' CHECK (camera IN ('off','optional','on')),
    microphone TEXT NOT NULL DEFAULT 'off' CHECK (microphone IN ('off','optional','on')),
    screen TEXT NOT NULL DEFAULT 'off' CHECK (screen IN ('off','optional','on')),
    fullscreen_required BOOLEAN NOT NULL DEFAULT false,
    focus_monitoring BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE proctoring_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_session_id UUID NOT NULL REFERENCES exam_sessions(id),
    policy_id UUID NOT NULL REFERENCES proctoring_policies(id),
    device_info JSONB
);

CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),  -- Drive feature: this is the *owner* for drive_permissions.rs purposes
    url TEXT NOT NULL,  -- re-signed fresh on every read (GET /assets*) — see Drive section below, don't trust this at rest
    type TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'private' CHECK (visibility IN ('public','private')),  -- P2-010, added migration 0013
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    filename TEXT,  -- Drive feature, migration 0016; NULL for pre-Drive rows
    folder_id UUID REFERENCES folders(id),  -- Drive feature, migration 0017; NULL = root
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),  -- Drive feature, migration 0017
    deleted_at TIMESTAMPTZ  -- Drive feature, migration 0017 — trash marker
);

CREATE TABLE proctoring_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proctoring_session_id UUID NOT NULL REFERENCES proctoring_sessions(id),
    type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low','medium','high')),
    "timestamp" TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata JSONB,
    evidence_id UUID REFERENCES assets(id)
);

-- === Auth Sessions (added 2026-08-23 for P1-001 — not in the original
-- ADR-0001 ERD dump above. Additive only: no existing table changed, so
-- per docs/STATE.md this didn't need a new ADR. See migrations/0010_auth_sessions.*
-- in titian-backend for the sqlx version of this (original Rust
-- implementation), or titian-backend-bun/src/db/schema.ts's
-- refreshTokens table for the Drizzle port — see ADR-0009. ===
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);

-- === Drive-style file management (added 2026-08-28, FE-driven, not a
-- numbered P2-XXX ticket — same status as the Content Studio backend
-- additions earlier this phase). Additive only, migrations
-- 0016_asset_filename / 0017_drive_folders / 0018_resource_sharing.
-- See service/drive_permissions.rs for the access model this backs. ===
CREATE TABLE folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    parent_folder_id UUID REFERENCES folders(id),  -- NULL = root
    owner_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at TIMESTAMPTZ  -- trash marker
);
CREATE INDEX idx_folders_parent ON folders(parent_folder_id);
CREATE INDEX idx_folders_owner ON folders(owner_id);

-- One polymorphic pair covering both `assets` and `folders` instead of
-- four near-duplicate tables. A grant on a folder cascades to everything
-- inside it (drive_permissions.rs walks the folder ancestry).
CREATE TABLE resource_shares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_type TEXT NOT NULL CHECK (resource_type IN ('asset','folder')),
    resource_id UUID NOT NULL,
    principal_type TEXT NOT NULL CHECK (principal_type IN ('user','role')),
    principal_id TEXT NOT NULL,  -- a user id (as text) or a role name, depending on principal_type
    permission TEXT NOT NULL CHECK (permission IN ('viewer','editor')),
    granted_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (resource_type, resource_id, principal_type, principal_id)
);
CREATE INDEX idx_resource_shares_resource ON resource_shares(resource_type, resource_id);
CREATE INDEX idx_resource_shares_principal ON resource_shares(principal_type, principal_id);

-- Ownership + activity trail — the ADR-style "collaboration" half of the
-- feature (create/upload/rename/move/delete/restore/share/unshare).
CREATE TABLE resource_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_type TEXT NOT NULL CHECK (resource_type IN ('asset','folder')),
    resource_id UUID NOT NULL,
    actor_id UUID NOT NULL REFERENCES users(id),
    action TEXT NOT NULL,
    detail JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_resource_activity_resource ON resource_activity(resource_type, resource_id, created_at DESC);
```

### Kampung Bahasa Pare (ADR-0016, migrasi `0080_pare_players.sql`)

Tabel game berawalan `pare_`; hanya `users` yang dipakai bersama. Tidak dibaca XP/liga/mastery Titian.

```sql
CREATE TABLE pare_players (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    username TEXT NOT NULL CHECK (username ~ '^[a-z0-9_.]{3,20}$'),   -- UNIQUE (lower(username))
    nickname TEXT NOT NULL CHECK (char_length(nickname) BETWEEN 1 AND 16),
    look JSONB NOT NULL,
    gender TEXT CHECK (gender IN ('m','f')),    -- 0086: Camp Putra / Camp Putri; null = pemain lama belum memilih
    zone TEXT NOT NULL DEFAULT 'camp',          -- camp|umum|en|zh|ar|ja|ko
    pos JSONB,
    xp INTEGER NOT NULL DEFAULT 0,              -- >= 0
    money BIGINT NOT NULL DEFAULT 0,            -- >= 0, rupiah game
    hearts NUMERIC(3,1) NOT NULL DEFAULT 5,     -- 0..5, kelipatan 0,5
    stamina REAL NOT NULL DEFAULT 100,          -- 0..100
    fullness REAL NOT NULL DEFAULT 70,          -- 0..120
    focus TEXT NOT NULL DEFAULT 'en', violations INTEGER NOT NULL DEFAULT 0, streak INTEGER NOT NULL DEFAULT 0,
    last_study DATE, last_seen TIMESTAMPTZ, sleeping_since TIMESTAMPTZ, bike_date DATE, laundry_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(), updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE pare_lang_progress (
    user_id UUID REFERENCES pare_players(user_id) ON DELETE CASCADE,
    lang TEXT NOT NULL,                          -- en|zh|ar|ja|ko
    level INTEGER NOT NULL DEFAULT 0, lang_xp INTEGER NOT NULL DEFAULT 0,
    level_start_xp INTEGER NOT NULL DEFAULT 0, exam_tries INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, lang)
);
CREATE TABLE pare_ledger (                       -- setiap perubahan uang/XP/nyawa game
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES pare_players(user_id) ON DELETE CASCADE,
    kind TEXT NOT NULL, delta_money BIGINT NOT NULL DEFAULT 0, delta_xp INTEGER NOT NULL DEFAULT 0,
    delta_hearts NUMERIC(3,1) NOT NULL DEFAULT 0, reason TEXT, ref TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Catatan implementasi: tulis sebagai migration bertahap per grup (identity → curriculum → concept → question → assessment → evaluation → learning engine → economy → exam/proctoring) supaya tiap migration kecil dan gampang di-rollback kalau ada error, bukan 1 file raksasa.

Pare-2 (migrasi `0081_pare_learning.sql`): `pare_words(user_id, lang, word_id, seen, correct)` (kata dikuasai setelah 3 benar), `pare_lessons(user_id, key, count, last_date)`, `pare_daily(user_id, date, counts jsonb, claimed text[])`, `pare_papers(id, user_id, kind, lang, key, level, graded, scored, assist, time_limit, questions jsonb (berisi kunci, tidak keluar dari server), state jsonb, correct, answered, earned_xp, earned_money, result jsonb, created_at, finished_at)`; kolom baru `pare_players.photos text[]` dan `pare_lang_progress.last_exam_at`. Konten bahasa (`data/pare/content.json`, dikompilasi ke binary) **bukan tabel** — lihat catatan penyimpangan di tiket P2-001.
Pare-9 (migrasi `0095_pare_path.sql`, `0096_pare_missions.sql`): `pare_path_nodes(user_id, lang, node_id, best_score, attempts, done_at, rewarded_at)` — hanya mencatat apa yang dilakukan pemain; id simpul diturunkan dari konten (`en-0-greet:w1:m`, `…:w1:l`, `…:practice`, `…:check`, `…:mission`); `pare_papers.node/reward` dan jenis kertas `path`. `pare_missions(user_id, lang, mission_id, status active|review|done, step, state jsonb, score jsonb, best_score, stars 0–3, attempts, started_at, done_at, rewarded_at)` — `state` memuat varian butir milik pemain beserta kuncinya (tidak keluar dari server); definisi misi ada di `data/pare/missions.json` (bukan tabel), diperiksa saat start (`pare_mission::validate`). `pare_unlocks(user_id, key, unlocked_at)` — stempel, wilayah, gelar.
Pare-3 (migrasi `0082_pare_life.sql`): kolom baru di `pare_players` — `rest_log jsonb` (periode istirahat [mulai_ms, akhir_ms], 48 jam), `meals_date/meals_count`, `snacks_date/snacks_count`, `cooldowns jsonb` (taman). Kolom nyawa/stamina/kenyang/`sleeping_since`/`bike_date`/`laundry_date`/`last_seen` dari 0080 kini ditulis hanya oleh `services/pare_life.rs`. Menu & harga toko: `data/pare/content.json` (`menus`, `prices`).
Pare-4 (migrasi `0083_pare_chat.sql`): `pare_conversations(id text, kind dm|group, name, created_by, last_message_at)`, `pare_conversation_members(conversation_id, user_id)`, `pare_messages(id bigserial, conversation_id, user_id, text <= 240)`, `pare_channel_messages(id bigserial, channel `zona#n`, user_id, text, lang, created_at)` (retensi 30 hari). Identitas publik pemain di chat = `username`.
P10-008 (migrasi `0104_pare_wardrobe.sql`, ADR-0023): `pare_players.look3d jsonb`; `pare_wardrobe(user_id, item_id "slot:key", source koin|toko, order_id, acquired_at)`; `orders.kind` + `'pare_wardrobe'` (item di `subscription_tier` sampai lunas). Barang gratis dan barang Plus/Pro tidak disimpan: hak pakainya dihitung dari katalog dan paket yang berjalan.

P11-002 (migrasi `0105_pare_engine.sql`): `pare_players.engine text not null default 'pixel'` (`pixel` | `3d`): tampilan bermain pilihan pemain; hanya menentukan pintu mana yang terbuka dari `/play`, bukan progres.

P11-008 (migrasi `0106_pare_client_reports.sql`): `pare_client_reports(id, created_at, user_id → users on delete cascade, kind perf|error|context_lost, engine, detail jsonb)`; indeks `(kind, created_at desc)` dan `(user_id, created_at desc)`. Contoh pertanyaan: kecepatan menurut kartu grafis: `select detail->>'gpu', detail->>'quality', avg((detail->>'fps')::float) from pare_client_reports where kind='perf' group by 1,2`.

Pare-8 (migrasi `0084_pare_premium.sql`, ADR-0018): `orders.kind` + `'pare_premium'`; `pare_premium(user_id, period_start, period_end, voucher, voucher_until, last_order_id)` (voucher diisi ulang malas per blok 30 hari); `pare_boosts(id, user_id, kind heart|rescue|double_pay, via ad|free, ref, day, started_at, claimed_at)`; `pare_players.fainted_at/faint_zone/faint_pos`; `pare_ledger.delta_voucher`.
Pare-5 (migrasi `0085_push.sql`): `push_subscriptions(id, user_id → users, app pare|titian, endpoint unik, p256dh, auth, user_agent, created_at, last_success_at)` (generik, bisa dipakai Titian); `pare_players.notify` (saklar per jenis) & `notify_state` (penanda harian, throttle, batas 12/hari).
Pare-7a (migrasi `0087_pare_voice.sql`, ADR-0017, tiket P7-001): `pare_voice_consents(user_id, version, accepted_at)`; `pare_voice_notes(id, conversation_id, user_id, lang, object_key, mime, duration_ms, status pending|transcribed|failed|expired, expires_at)`; `pare_voice_transcripts(id, note_id, user_id, lang_target, text, detected_lang, confidence, verdict jsonb)` (satu baris per potongan kalimat; hanya voice note — live tidak pernah disimpan, ADR-0017 §5); `pare_voice_strikes(id, user_id, ref, kind, created_at)` (`ref` teks bebas seperti `pare_ledger.ref`, bisa menunjuk voice note atau sesi live); `pare_voice_locks(user_id, until, reason)`; `pare_blocks(user_id, blocked_id)`; `pare_messages.kind text|voice` + `voice_note_id`. Konfigurasi gerbang di `data/pare/content.json` → `voice: {liveMinLevel: {en,zh,ar,ja,ko}, noteMaxSeconds: 60, retentionDays: 3}` (nilai `liveMinLevel` masih usulan, lihat ADR-0017 §11.1), dimuat ke `services/pare_content.rs::Voice` dan divalidasi lewat `voice_config_covers_every_language_with_a_level_that_exists`.
Pare-7a (migrasi `0088_pare_voice_zone.sql`, tiket P7-004): `pare_voice_notes.zone` (nullable) — zona TEMPAT PEMBICARA saat merekam (dari `pare_players.zone`, dicatat sekali di `create_note`), dipakai `services/pare_speech.rs::judge_speech` untuk menilai transkripnya saat `finish` — beda dari `lang` (bahasa yang dipilih untuk pengenal suara & gerbang level, tidak berubah). `pare_voice_transcripts` kini benar-benar diisi oleh `finish_note` (satu baris per potongan dari `POST .../finish {transcript: [{text, confidence}]}`); belum ada strike/penalti dari sini (P7-005). Hub dapat pesan `voice_transcript {room, parts}` (live, per 15-30 dtk) yang cuma dinilai & dibuang untuk sekarang (P7-010 mengumpulkan hasil sesi).
Pare-7b (migrasi `0089_pare_voice_moderation.sql`, tiket P7-007): `pare_voice_reports(id uuid, reporter_id, reported_id, conversation_id, ref 'note:<id>'|'live:<id>', reason ≤ 500, excerpt (kutipan transkrip disalin saat melapor), flagged, status open|actioned|dismissed, action, action_note, reviewed_by → users, reviewed_at)` dengan `unique(reporter_id, ref)`; `pare_voice_mutes(muter_id, muted_id, until)` (pelapor tak lagi mendengar terlapor 24 jam). Blokir memakai `pare_blocks` (0087). Tindakan moderator tercatat di `admin_audit_log` (`action = 'pare_voice_report.<dismiss|warn|lock>'`, `target_type = 'pare_voice_report'`).
Pare-7b (migrasi `0090_pare_voice_live.sql`, tiket P7-009): `pare_voice_sessions(id uuid, conversation_id, lang, initiator_id, status ringing|active|ended|cancelled|missed, created_at, started_at, ended_at)` dan `pare_voice_participants(session_id, user_id, response null|joined|declined, invited_at, joined_at, left_at)` — jejak siapa/kapan/berapa lama, **tanpa isi percakapan** (ADR-0017 §5); dipangkas > 1 tahun oleh job retensi. Status sementara di **Redis**: `pare:call:room:<session>` (JSON: penelepon, percakapan, bahasa, anggota; TTL 45 dtk selama berdering, 4 jam begitu ada yang masuk) dan `pare:call:player:<user>` (= sesi yang sedang diikuti pemain; SET NX → satu panggilan per pemain).
Pare-7b (migrasi `0091_pare_voice_system_flags.sql`, tiket P7-010): `pare_voice_reports.reporter_id` boleh NULL + `source text` (`player`|`system`; check: pelapor ada ⇔ `player`) + unik parsial `(reported_id, ref) where source = 'system'` (satu penandaan otomatis per pemain per panggilan). Penandaan sistem dibuat saat peserta live meninggalkan panggilan bila mikrofonnya menyala ≥ 30 dtk tanpa transkrip; antrean admin menampilkan pelapor `sistem`. Pengawasan berjalan di memori proses (`pare_voice_watch::TALLIES`, dibersihkan saat peserta keluar / setelah 6 jam) — tak ada isi ucapan di DB.

> Pare-7 (2026-09-26): evaluasi bahasa dari transkrip dilepas sementara — `pare_voice_transcripts`, `pare_voice_strikes`, `pare_voice_locks` (kunci otomatis), `pare_voice_reports.source='system'` dan `pare_voice_notes.zone` tidak lagi diisi; tabel/kolom dibiarkan untuk pemulihan (lihat ADR-0017 status).

Pare (2026-09-26, migrasi `0092_pare_chat_requests.sql`): `pare_conversation_members` + `last_read_at` (terakhir dibaca), `cleared_at` ("hapus chat": pesan sebelumnya disembunyikan untuk anggota itu), `accepted_at` (chat personal: NULL = masih permintaan pesan untuk anggota itu; pemulai & yang membalas terisi; data lama di-backfill terisi & terbaca). `pare_blocks` kini juga menahan chat (dua arah).

Pare (2026-09-26, migrasi `0093_pare_voice_talk_time.sql`): `pare_voice_participants` + `seg_started_at` (segmen bicara yang sedang berjalan) dan `talk_seconds` (akumulasi). Jatah telepon harian dihitung dari sini (WIB), lihat api-contract.

Pare (2026-10-02, migrasi `0094_pare_avatar.sql`): `pare_players` + `avatar_token` (uuid acak, unik, berganti tiap unggah = bagian URL publik), `avatar_key` (objek di storage `pare-avatars/<token>.<ext>`), `avatar_at`.
