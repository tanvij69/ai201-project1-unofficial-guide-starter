# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This project covers Virginia Tech dining experiences and student opinions about campus food. While official dining websites provide menus and location information, they do not capture student perspectives on food quality, value, wait times, variety, and overall satisfaction. This knowledge is scattered across Reddit threads, Google reviews, and informal recommendations, making it difficult for students to find in one place. A first-year student trying to decide which dining hall to use or which dining plan to buy cannot get that information from the official VT Dining website.


---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Google Maps | Reviews  | docs/google_reviews_d2.txt |
| 2 | Google Maps| Reviews  | docs/google_reviews_hokie_grill.txt |
| 3 | dining.vt.edu | Official page | docs/vt_dining_overview.txt |
| 4 | r/VirginiaTech | Reddit thread | docs/reddit_best_dining_hall.txt |
| 5 | r/VirginiaTech | Reddit thread | docs/reddit_turner_dining.txt |
| 6 | r/VirginiaTech | Reddit thread | docs/reddit_vegetarian_dining.txt |
| 7 | r/VirginiaTech | Reddit thread | docs/reddit_campus_food_recs.txt |
| 8 | r/VirginiaTech | Reddit thread | docs/reddit_owens_food.txt |
| 9 | r/VirginiaTech | Reddit thread | docs/reddit_d2_food.txt |
| 10 | r/VirginiaTech | Reddit thread | docs/reddit_dining_plan_worth_it.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 300 Characters

**Overlap:** 50 Characters

**Why these choices fit your documents:** Most documents were Reddit comments and Google reviews, which are usually short and focus on one opinion. A chunk size of 300 characters was chosen because it is large enough to capture a complete idea without combining different opinions. A 50 character overlap helps keep context when a sentence is split between chunks. Before chunking, the documents were cleaned by removing HTML tags, HTML entities, and extra blank lines.

**Final chunk count:** 117 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key required)

**Production tradeoff reflection:** For a real deployment, I would consider using OpenAI's text-embedding-3-small because it may provide more accurate results on informal text such as Reddit comments. However, it would increase both cost and response time. Since all documents are in English, multilingual support is not needed. The 300 character chunks are also small enough that context length is not a concern. One limitation of all-MiniLM-L6-v2 is that it is a general purpose model, so it may miss relevant results when users phrase questions differently from the wording used in the reviews.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt instructs the LLM to answer only using the retrieved chunks provided as context and to not use any outside knowledge. The exact instruction given is: "You are a helpful assistant for Virginia Tech students. Answer the question using ONLY the information provided in the context below. If the answer is not in the context, say you don't have enough information. At the end of your answer, cite the source filenames in parentheses."

**How source attribution is surfaced in the response:**

Each retrieved chunk is sent to the LLM along with its source filename. The model is instructed to include the filename at the end of its answer so users can see where the information came from. The retrieval function also displays all source filenames used in generating the response, making it easy to identify the documents that contributed to the answer.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about wait times at D2 during lunch? | D2 gets crowded and noisy, especially when summer camps visit, but wait times are generally manageable | System said "No wait" at D2 during lunch, pulling from a single Google review metadata tag rather than full context | Off-target | Inaccurate |
| 2 | Which dining plan do students recommend for first year students living on campus? | Get the smallest/cheapest plan and add dining dollars as needed | Students recommend the cheapest plan and adding dining dollars as needed, as many end up with money left over | Relevant | Accurate |
| 3 | What vegetarian options are available at Owens according to students? | Variabowl, Wan (tofu stir fry and vegan bulgogi), and occasional veggie burgers at Pops | Wan tofu stir fry, vegan bulgogi, Variabowl, and occasional veggie burgers at Pops | Relevant | Accurate |
| 4 | What are the main complaints students have about Turner Place dining hall? | Long lines at Qdoba and Jamba Juice, understaffing, inconsistent portion sizes at Fire Grill, and limited seating | Long lines, food under heat lamp, slow food preparation, impractical for quick meals between classes | Relevant | Partially accurate |
| 5 | Is D2 considered good value according to student reviews? | Yes, all you can eat for around $5 with a student discount, but food quality is inconsistent | D2 is the best value dining hall on campus, all you can eat for $5 | Relevant | Partially Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

What do students say about wait times at D2 during lunch?

**What the system returned:**

According to the reviews, there is "No wait" at D2 during lunch. 
[Source: google_reviews_d2.txt]

Sources: google_reviews_hokie_grill.txt, google_reviews_d2.txt, reddit_turner_dining.txt, vt_dining_overview.txt, reddit_dining_plan_worth_it.txt

**Root cause (tied to a specific pipeline stage):**

The error occurred at the chunking stage of the process where the D2 Google review had been broken down into separate pieces by the 300 character fixed-sized chunker. The "Wait Time: No Wait" tied to the D2 review was a metadata tag and had been entered as its own chunk and not tied back to the review it was associated with. When a search for wait times occurred the isolated metadata tag was matched to the query of wait times and passed to the LLM as if it was the complete opinion of a student. The chunk that contained the most semantically relevant information regarding wait times belonged to Hokie Grill and not to D2 since it contained an entire sentence for wait times of 10 - 20 minutes and was therefore matched against the fragmented chunks of D2's Google review.

**What you would change to fix it:**

Chunking is based on a measure of the individual reviews (or paragraph) to maintain the contextual relationship of metadata with each review. This prevents the isolated tags associated with a review (e.g. “Wait time: No wait”) from becoming stand-alone items that can lead to inaccurate retrieval or search results.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The chunking strategy section in planning.md guided the implementation of chunk_text() in ingest.py. Deciding on 300 character chunks and a 50 character overlap before writing any code gave the function a clear target. It also made it easier to prompt Claude to generate the ingestion code because providing the exact chunk size and overlap produced code that matched the plan without needing corrections.

**One way your implementation diverged from the spec, and why:**

The spec described the retrieval code as a single pipeline, but in the implementation it was split into two files, ingest.py and retriever.py. This happened because the embedding and retrieval logic needed to import code from ingest.py, and separating them made each part easier to test on its own. Although the diagram in the spec suggested one script, using two files turned out to be cleaner and more practical.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md and the list of files in my docs/ folder.
- *What it produced:* A load_and_chunk() function that read all .txt files and split them into fixed-size character chunks with overlap, returning a list of dictionaries with text, source, and chunk_id keys.
- *What I changed or overrode:* The original generated code combined loading and chunking into one function. I separated them into load_documents(), clean_text(), and chunk_text() as three distinct functions so each stage could be tested independently and reused in retriever.py.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach section from planning.md and the pipeline diagram.
- *What it produced:* An embed_and_store() function using sentence-transformers and ChromaDB, and a retrieve() function that returned the top 5 chunks with distance scores and source metadata.
- *What I changed or overrode:* The generated code initially used an in-memory ChromaDB client. I changed it to PersistentClient so embeddings are saved to disk and do not need to be recreated on every run. This was a deliberate improvement over what the AI produced.
