# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
This project focuses on Virginia Tech dining experiences and student opinions about campus food. While official dining websites provide menus and location information, they do not capture student perspectives on food quality, value, wait times, variety, and overall satisfaction. This knowledge is scattered across Reddit discussions, Google reviews, and informal recommendations, making it difficult for students to find in one place.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Google Maps | Student reviews of D2 Dining Hall | docs/google_reviews_d2.txt |
| 2 | Google Maps | Student reviews of Hokie Grill | docs/google_reviews_hokie_grill.txt |
| 3 | dining.vt.edu | Official VT Dining Services overview | docs/vt_dining_overview.txt |
| 4 | r/VirginiaTech | Thread: What are the best dining halls? | docs/reddit_best_dining_hall.txt |
| 5 | r/VirginiaTech | Thread: What do you think of Turner Place? | docs/reddit_turner_dining.txt |
| 6 | r/VirginiaTech | Thread: Best places to get vegetarian food on campus | docs/reddit_vegetarian_dining.txt |
| 7 | r/VirginiaTech | Thread: Best food spots at VT | docs/reddit_campus_food_recs.txt |
| 8 | r/VirginiaTech | Thread: Owen's Dining | docs/reddit_owens_food.txt |
| 9 | r/VirginiaTech | Thread: Is there any one food at D2 that's universally bad? | docs/reddit_d2_food.txt|
| 10 | r/VirginiaTech | Thread: What dining plan at Virginia Tech is worth it? | docs/reddit_dining_plan_worth_it.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
