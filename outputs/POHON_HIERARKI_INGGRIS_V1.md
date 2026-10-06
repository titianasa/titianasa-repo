# Pohon Hierarki Bahasa Inggris v1 (usulan unit)

Status: **usulan**, dihasilkan dari registry topik lama oleh `pemetaan-jalur-ujian/build_registry_inggris.py`. Nama unit, pemetaan ke konsep, dan label CEFR belum ditinjau penelaah Bahasa Inggris.
Mengikuti `POHON_HIERARKI_DOMAIN_LAIN_V1.md` bagian 2 (22 butir konsep) dan `STANDAR_KURIKULUM_TITIAN_ASA.md`. Butir pohon itu diperlakukan sebagai **konsep**, dan unit di bawahnya berasal dari topik lama.

```text
english
└─ bahasa_inggris
   ├─ receptive_listening
   │  ├─ english.explicit_information — Mengenali bunyi, kata, dan informasi eksplisit (3 unit)
   │  │  ├─ [A2] Menemukan informasi spesifik dari teks lisan
   │  │  ├─ [B2] Memahami berbagai aksen bahasa Inggris
   │  │  └─ [B2] Memahami ujaran cepat dan bersambung
   │  ├─ english.main_idea_inference_attitude — Memahami ide utama, detail, inferensi, dan sikap pembicara (3 unit)
   │  │  ├─ [A2] Menangkap gagasan pokok teks lisan
   │  │  ├─ [B1] Memahami percakapan dan wawancara
   │  │  └─ [B1] Mencatat informasi saat menyimak
   │  └─ english.evaluate_spoken_text — Mengevaluasi tujuan serta keandalan teks lisan (1 unit)
   │     └─ [C1] Memahami kuliah dan podcast
   ├─ receptive_reading
   │  ├─ english.vocabulary_in_context — Memahami kosakata dalam konteks (1 unit)
   │  │  └─ [B1] Menafsirkan kosakata dari konteks
   │  ├─ english.main_idea_supporting_detail — Menemukan gagasan utama dan detail pendukung (5 unit)
   │  │  ├─ [A2] Membaca untuk informasi terperinci
   │  │  ├─ [A2] Menerapkan skimming dan scanning
   │  │  ├─ [B1] Menentukan gagasan utama dan detail pendukung
   │  │  ├─ [B1] Menganalisis struktur teks
   │  │  └─ [B2] Membaca cepat secara efektif
   │  ├─ english.inference_argument — Membuat inferensi dan menilai argumen (2 unit)
   │  │  ├─ [B2] Membuat inferensi dan menangkap makna tersirat
   │  │  └─ [C1] Mengevaluasi argumen dalam bacaan
   │  └─ english.academic_functional_literary_texts — Membaca teks akademik, fungsional, dan sastra (0 unit)
   │     ├─ [A2] Membaca dan menulis Announcement, Invitation & Notice  (unit sekunder: konsep utamanya WRT2)
   │     ├─ [B1] Membaca dan menulis Explanation Text  (unit sekunder: konsep utamanya WRT2)
   │     ├─ [B1] Membaca dan menulis News Item  (unit sekunder: konsep utamanya WRT2)
   │     ├─ [B1] Membaca dan menulis Procedure Text  (unit sekunder: konsep utamanya WRT2)
   │     ├─ [B1] Membaca dan menulis Report Text  (unit sekunder: konsep utamanya WRT2)
   │     └─ [B1] Membaca dan menulis Review Text  (unit sekunder: konsep utamanya WRT3)
   ├─ productive_speaking
   │  ├─ english.sounds_stress_intonation — Mengucapkan bunyi, tekanan kata, dan intonasi (0 unit)
   │  │  └─ (belum ada topik lama; unit baru diperlukan)
   │  ├─ english.transactional_interpersonal_interaction — Berinteraksi dalam percakapan transaksional/interpersonal (16 unit)
   │  │  ├─ [A1] Menyapa dan berbasa-basi
   │  │  ├─ [A2] Berkomunikasi di sekolah dan kampus
   │  │  ├─ [A2] Berkomunikasi saat bepergian, di bandara, dan di hotel
   │  │  ├─ [A2] Berkomunikasi saat berbelanja dan makan di restoran
   │  │  ├─ [A2] Melakukan percakapan sehari-hari
   │  │  ├─ [A2] Membuat permintaan dan tawaran
   │  │  ├─ [A2] Meminta dan memberi informasi
   │  │  ├─ [A2] Menyatakan kesukaan, ketidaksukaan, dan preferensi
   │  │  ├─ [B1] Berkomunikasi di layanan kesehatan
   │  │  ├─ [B1] Berkomunikasi di tempat kerja
   │  │  ├─ [B1] Berkomunikasi melalui telepon dan daring
   │  │  ├─ [B1] Memberi saran dan nasihat
   │  │  ├─ [B1] Meminta maaf dan menyampaikan keluhan
   │  │  ├─ [B1] Menyatakan pendapat
   │  │  ├─ [B1] Menyatakan setuju dan tidak setuju
   │  │  └─ [B2] Menjawab pertanyaan wawancara
   │  ├─ english.opinion_argument — Menyampaikan opini dan argumen (2 unit)
   │  │  ├─ [B2] Menyampaikan dan mempertahankan opini
   │  │  └─ [C1] Berpartisipasi dalam diskusi dan debat
   │  └─ english.presentation_fluency — Mempresentasikan topik dengan kelancaran sesuai CEFR (3 unit)
   │     ├─ [A2] Mendeskripsikan orang, tempat, dan benda
   │     ├─ [B1] Menarasikan peristiwa dan bercerita
   │     └─ [B2] Mempresentasikan topik secara terstruktur
   ├─ productive_writing
   │  ├─ english.sentence_paragraph_coherence — Menulis kalimat, paragraf, dan teks koheren (10 unit)
   │  │  ├─ [A2] Menggunakan aturan Capitalization
   │  │  ├─ [A2] Menggunakan aturan Periods, Question & Exclamation Marks
   │  │  ├─ [A2] Menggunakan aturan Spelling Rules
   │  │  ├─ [A2] Menyusun kalimat menjadi paragraf
   │  │  ├─ [B1] Menggunakan aturan Apostrophes
   │  │  ├─ [B1] Menggunakan aturan Commas
   │  │  ├─ [B1] Menggunakan aturan Quotation Marks
   │  │  ├─ [B1] Menyusun paragraf yang padu
   │  │  ├─ [B2] Menggunakan aturan Colons & Semicolons
   │  │  └─ [B2] Menggunakan aturan Hyphens & Dashes
   │  ├─ english.descriptive_narrative_procedural_report — Menulis deskripsi, narasi, prosedur, dan laporan (11 unit)
   │  │  ├─ [A2] Membaca dan menulis Announcement, Invitation & Notice
   │  │  ├─ [A2] Membaca dan menulis Descriptive Text
   │  │  ├─ [A2] Membaca dan menulis Recount Text
   │  │  ├─ [B1] Membaca dan menulis Explanation Text
   │  │  ├─ [B1] Membaca dan menulis Narrative Text
   │  │  ├─ [B1] Membaca dan menulis News Item
   │  │  ├─ [B1] Membaca dan menulis Procedure Text
   │  │  ├─ [B1] Membaca dan menulis Report Text
   │  │  ├─ [B1] Menulis teks deskriptif
   │  │  ├─ [B1] Menulis teks naratif
   │  │  └─ [B2] Menulis teks ekspositori
   │  ├─ english.argumentation_academic_response — Menulis argumentasi serta tanggapan akademik (6 unit)
   │  │  ├─ [B1] Membaca dan menulis Review Text
   │  │  ├─ [B2] Membaca dan menulis Analytical Exposition
   │  │  ├─ [B2] Membaca dan menulis Discussion Text
   │  │  ├─ [B2] Membaca dan menulis Hortatory Exposition
   │  │  ├─ [B2] Menulis teks argumentatif dan persuasif
   │  │  └─ [B2] Meringkas dan memparafrasa teks
   │  └─ english.revision_rubric — Merevisi tulisan berdasarkan rubrik (1 unit)
   │     └─ [B2] Menyunting dan memeriksa tulisan
   ├─ grammar_vocabulary
   │  ├─ english.word_classes_tenses_modality — Menggunakan kelas kata, tenses, aspek, dan modalitas (48 unit)
   │  │  ├─ [A1] Menggunakan Present Continuous
   │  │  ├─ [A1] Menggunakan Simple Present
   │  │  ├─ [A2] Menggunakan Adjectives & Order of Adjectives
   │  │  ├─ [A2] Menggunakan Articles & Determiners
   │  │  ├─ [A2] Menggunakan As...as & Expressions of Equality
   │  │  ├─ [A2] Menggunakan Can, Could & Be Able To
   │  │  ├─ [A2] Menggunakan Comparative Adjectives
   │  │  ├─ [A2] Menggunakan Interferensi Bahasa Indonesia
   │  │  ├─ [A2] Menggunakan Must, Have To & Need To
   │  │  ├─ [A2] Menggunakan Nouns (Countable, Uncountable, Collective)
   │  │  ├─ [A2] Menggunakan Past Continuous
   │  │  ├─ [A2] Menggunakan Prepositions (Time, Place, Movement)
   │  │  ├─ [A2] Menggunakan Pronouns (Personal, Possessive, Reflexive)
   │  │  ├─ [A2] Menggunakan Pronunciation Traps
   │  │  ├─ [A2] Menggunakan Simple Future (will / be going to)
   │  │  ├─ [A2] Menggunakan Simple Past
   │  │  ├─ [A2] Menggunakan Superlative Adjectives
   │  │  ├─ [A2] Menggunakan Verbs (Action, Linking, Auxiliary)
   │  │  ├─ [B1] Menggunakan Active vs Passive Voice
   │  │  ├─ [B1] Menggunakan Adverbs & Adverb Placement
   │  │  ├─ [B1] Menggunakan Article Errors (a/an/the)
   │  │  ├─ [B1] Menggunakan Common Comparison Errors
   │  │  ├─ [B1] Menggunakan Comparative & Superlative Adverbs
   │  │  ├─ [B1] Menggunakan Conjunctions (Coordinating & Subordinating)
   │  │  ├─ [B1] Menggunakan Future Continuous
   │  │  ├─ [B1] Menggunakan Interjections
   │  │  ├─ [B1] Menggunakan Irregular Comparisons
   │  │  ├─ [B1] Menggunakan May & Might
   │  │  ├─ [B1] Menggunakan Past Perfect
   │  │  ├─ [B1] Menggunakan Preposition Errors
   │  │  ├─ [B1] Menggunakan Present Perfect
   │  │  ├─ [B1] Menggunakan Quantifiers
   │  │  ├─ [B1] Menggunakan Shall
   │  │  ├─ [B1] Menggunakan Should, Ought To & Had Better
   │  │  ├─ [B1] Menggunakan Tense & Time Reference Errors
   │  │  ├─ [B1] Menggunakan When to Use the Passive
   │  │  ├─ [B1] Menggunakan Will & Would
   │  │  ├─ [B1] Menggunakan Word Order Errors
   │  │  ├─ [B2] Menggunakan Causative (have/get something done)
   │  │  ├─ [B2] Menggunakan False Friends
   │  │  ├─ [B2] Menggunakan Future Perfect
   │  │  ├─ [B2] Menggunakan Modals of Deduction (Present & Past)
   │  │  ├─ [B2] Menggunakan Passive in All Tenses
   │  │  ├─ [B2] Menggunakan Passive with Modals
   │  │  ├─ [B2] Menggunakan Past Perfect Continuous
   │  │  ├─ [B2] Menggunakan Present Perfect Continuous
   │  │  ├─ [B2] Menggunakan Tense Review & Comparison
   │  │  └─ [C1] Menggunakan Future Perfect Continuous
   │  ├─ english.phrases_clauses_complex_sentences — Menggunakan frasa, klausa, serta kalimat kompleks (48 unit)
   │  │  ├─ [A1] Menggunakan Articles: a, an, the
   │  │  ├─ [A1] Menggunakan Basic Word Order
   │  │  ├─ [A1] Menggunakan Imperatives
   │  │  ├─ [A1] Menggunakan Negative Sentences
   │  │  ├─ [A1] Menggunakan Singular & Plural Nouns
   │  │  ├─ [A1] Menggunakan Subject + Verb Basics
   │  │  ├─ [A1] Menggunakan The Verb "To Be"
   │  │  ├─ [A1] Menggunakan There is / There are
   │  │  ├─ [A1] Menggunakan Wh- Questions
   │  │  ├─ [A1] Menggunakan Yes/No Questions
   │  │  ├─ [A2] Menggunakan Simple Sentences
   │  │  ├─ [A2] Menggunakan Subject-Verb Agreement
   │  │  ├─ [A2] Menggunakan Zero Conditional
   │  │  ├─ [B1] Menggunakan Backshifting Tenses
   │  │  ├─ [B1] Menggunakan Complex Sentences
   │  │  ├─ [B1] Menggunakan Compound Sentences
   │  │  ├─ [B1] Menggunakan Direct vs Indirect Speech
   │  │  ├─ [B1] Menggunakan First Conditional
   │  │  ├─ [B1] Menggunakan Gerunds as Subjects & Objects
   │  │  ├─ [B1] Menggunakan Independent & Dependent Clauses
   │  │  ├─ [B1] Menggunakan Infinitives of Purpose
   │  │  ├─ [B1] Menggunakan Question Tags
   │  │  ├─ [B1] Menggunakan Relative Clauses (Defining & Non-Defining)
   │  │  ├─ [B1] Menggunakan Second Conditional
   │  │  ├─ [B1] Menggunakan Verbs Followed by Gerund
   │  │  ├─ [B1] Menggunakan Verbs Followed by Infinitive
   │  │  ├─ [B2] Menggunakan Adverbial Clauses
   │  │  ├─ [B2] Menggunakan Bare Infinitive
   │  │  ├─ [B2] Menggunakan Compound-Complex Sentences
   │  │  ├─ [B2] Menggunakan Discourse Markers & Cohesive Devices
   │  │  ├─ [B2] Menggunakan Noun Clauses
   │  │  ├─ [B2] Menggunakan Reporting Commands & Requests
   │  │  ├─ [B2] Menggunakan Reporting Questions
   │  │  ├─ [B2] Menggunakan Reporting Verbs & Patterns
   │  │  ├─ [B2] Menggunakan Third Conditional
   │  │  ├─ [B2] Menggunakan Unless, As Long As, Provided That
   │  │  ├─ [B2] Menggunakan Verbs with Both (Meaning Change)
   │  │  ├─ [B2] Menggunakan Wish & If Only
   │  │  ├─ [B2] Menggunakan Word Order & Inversion Basics
   │  │  ├─ [C1] Menggunakan Cleft Sentences (It-cleft & Wh-cleft)
   │  │  ├─ [C1] Menggunakan Inversion for Emphasis
   │  │  ├─ [C1] Menggunakan Mixed Conditionals
   │  │  ├─ [C1] Menggunakan Nominalisation
   │  │  ├─ [C1] Menggunakan Participle Clauses
   │  │  ├─ [C1] Menggunakan Reduced Relative Clauses
   │  │  ├─ [C2] Menggunakan Advanced Passive Structures
   │  │  ├─ [C2] Menggunakan Ellipsis & Substitution
   │  │  └─ [C2] Menggunakan Subjunctive Mood
   │  ├─ english.general_academic_vocabulary_collocation — Mengembangkan kosakata umum, akademik, dan kolokasi (29 unit)
   │  │  ├─ [A1] Memperluas kosakata: Animals & Nature
   │  │  ├─ [A1] Memperluas kosakata: Body & Health
   │  │  ├─ [A1] Memperluas kosakata: Clothing & Personal Items
   │  │  ├─ [A1] Memperluas kosakata: Colors, Shapes & Sizes
   │  │  ├─ [A1] Memperluas kosakata: Dates, Days & Duration
   │  │  ├─ [A1] Memperluas kosakata: Family & Relationships
   │  │  ├─ [A1] Memperluas kosakata: Food & Drink
   │  │  ├─ [A1] Memperluas kosakata: House & Furniture
   │  │  ├─ [A1] Memperluas kosakata: Numbers, Dates & Time
   │  │  ├─ [A1] Memperluas kosakata: Numbers, Fractions & Decimals in English
   │  │  ├─ [A1] Memperluas kosakata: Places & Directions
   │  │  ├─ [A1] Memperluas kosakata: Telling the Time
   │  │  ├─ [A1] Memperluas kosakata: Weather & Seasons
   │  │  ├─ [A2] Memperluas kosakata: Adverbs of Frequency
   │  │  ├─ [A2] Memperluas kosakata: High-Frequency Word List
   │  │  ├─ [A2] Memperluas kosakata: Money, Prices & Percentages
   │  │  ├─ [B1] Memperluas kosakata: Commonly Confused Words
   │  │  ├─ [B1] Memperluas kosakata: Homophones & Homonyms
   │  │  ├─ [B1] Memperluas kosakata: Measurements & Units
   │  │  ├─ [B1] Memperluas kosakata: Phrasal Verbs: Separable & Inseparable
   │  │  ├─ [B1] Memperluas kosakata: Synonyms & Antonyms
   │  │  ├─ [B2] Memperluas kosakata: Collocations
   │  │  ├─ [B2] Memperluas kosakata: Common Idioms
   │  │  ├─ [B2] Memperluas kosakata: Phrasal Verbs by Topic
   │  │  ├─ [B2] Memperluas kosakata: Register: Formal vs Informal
   │  │  ├─ [B2] Memperluas kosakata: Word Roots (Latin & Greek)
   │  │  ├─ [C1] Memperluas kosakata: Academic Word List (AWL)
   │  │  ├─ [C1] Memperluas kosakata: Proverbs & Sayings
   │  │  └─ [C1] Memperluas kosakata: Slang & Colloquial Expressions
   │  └─ english.word_formation_guessing — Menggunakan strategi pembentukan dan penebakan kata (5 unit)
   │     ├─ [B1] Membentuk kata dengan Compound Words
   │     ├─ [B1] Membentuk kata dengan Prefixes
   │     ├─ [B1] Membentuk kata dengan Suffixes
   │     ├─ [B2] Membentuk kata dengan Word Families & Derivatives
   │     └─ [C1] Membentuk kata dengan Conversion (Noun ↔ Verb)
   └─ pronunciation
      ├─ english.phonemes_minimal_pairs — Membedakan fonem dan pasangan bunyi minimal (4 unit)
      │  ├─ [A1] Membedakan bunyi konsonan
      │  ├─ [A1] Membedakan bunyi vokal pendek dan panjang
      │  ├─ [A1] Mengenali abjad dan bunyi huruf
      │  └─ [B1] Membaca simbol fonetik (IPA)
      ├─ english.hard_sounds_rhythm_intonation — Memproduksi bunyi sulit, ritme, serta intonasi (5 unit)
      │  ├─ [A2] Melafalkan gugus konsonan dan digraf
      │  ├─ [A2] Menerapkan tekanan kata
      │  ├─ [B1] Melatih kelancaran dan pelafalan
      │  ├─ [B1] Menerapkan pola intonasi
      │  └─ [B1] Menerapkan tekanan dan ritme kalimat
      └─ english.pronunciation_self_monitoring — Memantau dan memperbaiki pelafalan mandiri (0 unit)
         └─ (belum ada topik lama; unit baru diperlukan)
```

Kode CEFR di depan unit adalah label (`cefr:`), bukan cabang pohon. Unit yang sama dirujuk oleh path CEFR, Cambridge, TKA, UTBK, dan persiapan tes; path tidak memiliki salinan.
