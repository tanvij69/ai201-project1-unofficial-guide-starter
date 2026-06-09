# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
This project is focused on the Dining Experience at Virginia Tech and how students feel about the food offered on campus. There are official dining websites where you can view menu options and where to find each dining option, but you cannot see what students think of the quality of the food, value of the food, the amount of time it takes to get food, the variety of food, and an overall satisfaction level. Therefore, it is difficult for students to discover about these topics since many of the opinions are spread out across several locations including Reddit, Google Reviews, and some informal recommendations.

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

**Chunk size:** 300 Characters

**Overlap:** 50 Characters

**Reasoning:** Most of the sources are Reddit posts and Google reviews. These types of comments are typically brief and relate to only one primary issue, so a chunk size of 300 characters allows each individual opinion to stay together without combining unrelated topics. For example, a comment about wait times at D2 can remain separate from a comment about vegetarian options. A 50-character overlap helps maintain context if a sentence is split between two chunks. The Virginia Tech Dining website also provided some data, but due to the length of the paragraphs, smaller chunks would still provide the proper level of detail since each paragraph is addressing a different subject matter.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 5

**Production tradeoff reflection:** For a real-world deployment, I would consider using OpenAI's text-embedding-3-small model because it may improve retrieval quality for the informal language often found in Reddit comments and reviews, although it would increase both cost and response time. Since all of the documents are written in English, multilingual support is not necessary, and context length is not a concern because the chunks are only 300 characters long. For retrieval, using a very small top-k value such as 1 or 2 could miss relevant information that appears across multiple documents, while a large value such as 10 or more may introduce less relevant content. A top-k value of 5 provides a balance between retrieving enough information and maintaining relevance.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about wait times at D2 during lunch? | D2 gets crowded and noisy, especially when summer camps visit, but wait times are generally manageable |
| 2 | Which dining plan do students recommend for first-year students living on campus? | Get the smallest/cheapest plan and add dining dollars as needed — do not pay for premium upfront |
| 3 | What vegetarian options are available at Owens according to students? | Variabowl, Wan (tofu stir fry and vegan bulgogi), and occasional veggie burgers at Pops |
| 4 | What are the main complaints students have about Turner Place dining hall? | Long lines at Qdoba and Jamba Juice, understaffing, inconsistent portion sizes at Fire Grill, and limited seating |
| 5 | Is D2 considered good value according to student reviews? | Yes, all you can eat for around $5 with a student discount, but food quality is inconsistent |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The Turner Place thread is 14 years old and the D2 thread is 6 years old. Menu items, prices, and restaurant names have changed since then. The system may retrieve and present this outdated information as if it is current, which is misleading even though it is technically grounded in the documents.

2. Some threads on Reddit only have 6 or 7 comments or responses, which indicates that there will be very little information available for the search terms provided by individual users. If a user were to ask a specific question regarding "Owens", there may be insufficient data within the specific Owen's thread to allow the system to provide an answer, resulting in pieces being pulled from completely unrelated documents.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Raw .txt files (docs/)
        ↓
[Document Ingestion - ingest.py]
   Read all .txt files from docs/ folder
        ↓
[Chunking - 300 chars, 50 char overlap]
   Split each document into small chunks
   preserving individual opinions/reviews
        ↓
[Embedding - all-MiniLM-L6-v2 (sentence-transformers)]
   Embed each chunk into a vector
        ↓
[Vector Store - ChromaDB]
   Store all chunk vectors locally
        ↓
[Retrieval - top-5 semantic search]
   Given a user query, find the 5 most
   similar chunks by cosine similarity
        ↓
[Generation - Groq API / llama-3.3-70b-versatile]
   Generate answer using only retrieved
   chunks as context
        ↓
Answer + Source Attribution
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

I will provide Claude with my Chunking Strategy section and the list of files from my docs/ directory and request that it create a load_and_chunk() method to load all .txt files, divide each file into 300 character chunks with a 50 character overlap, and return a list of dictionaries with the keys text, source and chunk_id.

**Milestone 4 — Embedding and retrieval:**

I will give Claude my Retrieval Approach section and ask it to implement an embed_and_store() function using sentence-transformers all-MiniLM-L6-v2 and ChromaDB, and a retrieve() function that takes a query string and returns the top 5 most similar chunks with their source filenames included.

**Milestone 5 — Generation and interface:**

Claude will be given my entire planning document (planning.md), and I will ask it to create a function called query_rag(). It will take in an end user question as input and then call the retrieve() function to obtain the top 5 chunks from the database. These chunks will be returned from the retrieve() function and used to format a prompt that contains either a citation or the source file name of each of the retrieved chunks and is sent via the Groq API llama-3.3-70b-versatile to generate a response from the llama. I will check to ensure that every response generated will have at least one source file name in the citation.
