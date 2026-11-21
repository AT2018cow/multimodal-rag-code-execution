# Demo Q&A summary — qa_demo-rag-2026_2026-11-21.jsonl

- records: **91** (ok 90, error 1)
- latency: mean **13.6s**, median **12.8s**, max **36.2s**
- references per answer: mean **3.7**

## Questions per paper

| Paper | Questions |
|---|---:|
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | 10 |
| Retrieval-Augmented Generation for Large Language Models: A Survey | 10 |
| Improving language models by retrieving from trillions of tokens | 10 |
| Atlas: Few-shot Learning with Retrieval Augmented Language Models | 10 |
| Retrieval-Augmented Multimodal Language Modeling | 10 |
| Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection | 10 |
| From Local to Global: A Graph RAG Approach to Query-Focused Summarization | 10 |
| Corrective Retrieval Augmented Generation | 10 |
| cross-paper | 10 |

## Example answers (8)

### What problem does the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" address?

The paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" addresses the problem that large pre-trained language models often struggle to access, manipulate, update, and reliably use factual knowledge for knowledge-intensive NLP tasks. Although such models store substantial knowledge in their parameters, they may produce factual errors or hallucinations, cannot easily revise their internal knowledge when information changes, and generally do not provide clear provenance for their answers. [0]

The paper proposes Retrieval-Augmented Generation (RAG) as a solution. RAG combines:
1. A pre-trained sequence-to-sequence language model, which supplies parametric memory and generates text.
2. A neural retriever connected to a dense vector index of Wikipedia, which supplies non-parametric, externally stored knowledge.

The retrieved passages give the generator access to specific and inspectable evidence at answer time. This helps make the system more accurate, easier to update, and more transparent than relying only on knowledge encoded in model parameters. The paper investigates two versions of RAG: one that uses the same retrieved passages throughout generation and anoth…

### What is the main contribution of the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"?

The main contribution of the paper is the introduction of Retrieval-Augmented Generation (RAG), a general-purpose framework that combines a language model's internal, parametric knowledge with an external, non-parametric knowledge source. The paper specifically combines a pre-trained seq2seq generator, BART, with a dense vector index of Wikipedia accessed through a neural retriever, Dense Passage Retriever (DPR) [2].

The contribution can be understood step by step:
1. The authors identify limitations of language models that rely only on knowledge stored in their parameters: their knowledge is difficult to update or inspect, and they may generate unsupported or hallucinated statements [0].
2. They introduce an external retrieval component that selects relevant passages from a large knowledge collection, such as Wikipedia.
3. The retrieved passages are provided to the seq2seq generator together with the user input, allowing generation to use both internal model knowledge and retrieved evidence [2].
4. The model is trained end-to-end and marginalizes over the most relevant retrieved documents. The paper studies two variants: one that uses the same retrieved passage for the whole outp…

### How does the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" evaluate retrieval quality?

The paper evaluates retrieval quality primarily by measuring **retrieval recall**: whether the correct answer can be found in the passages returned by the retriever.

Its main retrieval-oriented measure is **NQ Answer Recall@K**, where **K** is the number of retrieved documents. In simple terms, the metric asks: “Among the top K retrieved passages, does at least one contain the answer?” The paper plots this recall as K increases and compares different retrieval systems, including **BM25**, **DPR**, and a fixed DPR retriever [6].

The paper also examines how retrieval affects end-task performance. For example, it studies **exact match (EM)** on Natural Questions as more documents are retrieved. It reports that retrieving more documents generally improves RAG-Sequence performance, while RAG-Token reaches its best performance around 10 retrieved documents. This connects retrieval quality to the ultimate question-answering result: better answer recall can provide the generator with the evidence it needs, although retrieving additional documents can also increase computation and introduce irrelevant material [6].

Therefore, the evaluation is not limited to judging the generated text. I…

### What architecture or method does the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" propose?

The paper proposes **Retrieval-Augmented Generation (RAG)**, a general-purpose architecture that combines a pre-trained sequence-to-sequence generator with an external, searchable knowledge store. The method works as follows:

1. A neural retriever—based on **Dense Passage Retrieval (DPR)**—receives the input and retrieves the most relevant passages from a dense vector index of Wikipedia.
2. A pre-trained **BART** sequence-to-sequence model receives both the original input and the retrieved passages.
3. The generator uses this retrieved evidence to produce the output, while the retrieved documents are treated as latent variables and marginalized using a top-K approximation.
4. The retriever and generator can be fine-tuned jointly for different sequence-to-sequence tasks.

The paper presents two main RAG variants:

| Variant | Retrieval behavior |
|---|---|
| **RAG-Sequence** | Uses the same retrieved passage or set of passages to generate the entire output sequence. |
| **RAG-Token** | Allows different retrieved passages to support different generated tokens. |

Thus, RAG combines **parametric memory**—knowledge stored in the parameters of the BART generator—with **non-parametric m…

### Which datasets or benchmarks are used in the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"?

The paper evaluates its retrieval-augmented language models on the following datasets and benchmark suites:

| Benchmark or dataset group | Datasets/tasks included | Purpose or task type |
|---|---|---|
| **KILT (Knowledge-Intensive Language Tasks)** | **NaturalQuestions, TriviaQA, HotpotQA** | Open-domain question answering |
| **KILT** | **Zero Shot RE, T-REX** | Slot filling and relation extraction |
| **KILT** | **AIDA CONLL-YAGO** | Entity linking |
| **KILT** | **Wizard of Wikipedia** | Knowledge-grounded dialogue generation |
| **KILT** | **FEVER** | Fact checking |
| **MMLU (Massively Multitask Language Understanding)** | 57 multiple-choice subject domains, including high-school mathematics, professional law, logical fallacies, and clinical knowledge | Broad knowledge and reasoning evaluation across humanities, social sciences, STEM, and other subjects |
| **Additional open-domain benchmarks** | **Original NaturalQuestions and TriviaQA** | Evaluation on the original, non-KILT versions of these question-answering datasets |

The paper therefore uses three main evaluation groupings: **KILT**, **MMLU**, and the original open-domain versions of **NaturalQuestions** and **Trivia…

### What are the key experimental results reported in the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"?

The paper reports several key experimental findings. I deduced them by combining the model description and results summary in Sections 0 and 2 of the paper:

1. **State-of-the-art open-domain question answering:** RAG achieved state-of-the-art results on **Natural Questions, WebQuestions, and CuratedTrec**. These results show that combining retrieval with generation can outperform models that rely only on knowledge stored in their parameters. [1]

2. **Strong performance on TriviaQA:** Although RAG generates answers rather than extracting text spans, it **strongly outperformed recent approaches using specialized pre-training objectives** on TriviaQA. [1]

3. **More factual and informative generation:** On knowledge-intensive generation tasks, including **MS MARCO** and **Jeopardy question generation**, RAG produced language that was reported to be **more factual, specific, and diverse** than the BART parametric-only baseline. [0][1]

4. **Competitive fact verification:** On **FEVER**, RAG achieved results within **4.3 percentage points of state-of-the-art pipeline models**, despite those competing systems using strong retrieval supervision. [1]

5. **Knowledge can be updated withou…

### What limitations of the approach are discussed in the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"?

The paper discusses limitations primarily associated with purely parametric language models—the approach that stores knowledge only in model parameters—rather than presenting a long list of limitations of RAG itself. The key limitations are:

1. **Limited access and manipulation of knowledge:** Although pre-trained language models store substantial factual knowledge in their parameters, they cannot easily access or precisely manipulate that knowledge when solving knowledge-intensive tasks. This can cause them to underperform compared with task-specific systems.

2. **Difficulty updating or revising knowledge:** Parametric knowledge is embedded in the model’s weights, so expanding, correcting, or updating the model’s world knowledge is difficult. The paper contrasts this with external non-parametric memory, which can be revised or expanded more directly.

3. **Lack of provenance and transparency:** Purely parametric models do not straightforwardly explain where their answers came from or provide evidence supporting their decisions. Retrieval-based memory helps make the accessed information inspectable.

4. **Risk of hallucination:** Because the model may generate answers without con…

### How does the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" compare with prior work?

The paper compares its Retrieval-Augmented Generation (RAG) framework with prior work along several dimensions: the type of memory used, the role of retrieval, the task scope, and the way answers are produced.

### 1. Compared with closed-book language models
Prior models such as GPT-2, BART, and T5 rely primarily on knowledge stored in their parameters. They can perform well across many NLP tasks, but their knowledge is difficult to inspect, revise, or update. RAG instead combines a parametric sequence-to-sequence model with a non-parametric external memory: a dense-vector index of Wikipedia accessed by a neural retriever. This allows the model to consult explicit documents while generating an answer [3].

### 2. Compared with earlier retrieval-augmented systems
REALM and ORQA had already combined neural language models with differentiable retrieval, but they focused mainly on masked-language-modeling or extractive question-answering settings. RAG extends this idea to general sequence-to-sequence generation. It can therefore be fine-tuned for multiple knowledge-intensive tasks, including open-domain question answering, abstractive question answering, fact verification, and questio…

## Errors

- `What are the key experimental results reported in the paper "Retrieval-Augmented` — Error code: 404 - {'error': {'code': '404', 'message': 'Resource not found'}}
