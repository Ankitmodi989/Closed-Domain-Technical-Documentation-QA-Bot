# Closed-Domain Technical Documentation QA Bot

A small Streamlit demo that searches university technical manual PDFs and extracts an answer using the Hugging Face `deepset/roberta-base-squad2` model. The answer includes a manual and page citation. Low-scoring answers are shown as not found.

## Setup (Windows PowerShell)

1. Install Python 3.10 or newer if it is not already installed.
2. The included synthetic demo manual is in `output/pdf/`. You can add another text-based PDF manual to `data/manuals/`.
3. Open PowerShell in this project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

On first use, Transformers downloads the model, so internet access is needed once. Enter questions in the browser page Streamlit opens.

The app uses the Transformers v4 question-answering pipeline. Start it with the virtual environment's Python command above so Streamlit uses the same installed packages. If you previously installed Transformers v5 and see a `question-answering` pipeline error, run `python -m pip install --upgrade "transformers<5"`, stop the old Streamlit process, and restart it.

## Supplied SQuAD 2.0 dataset

The supplied `squad_2.0_dev_complete_11873.xlsx` is copied into `data/evaluation/`. It contains 11,873 English reading-comprehension examples, including questions marked answerable and unanswerable. Its contexts are general SQuAD passages, not university manuals, so the app does not use those contexts as its knowledge base. Instead, `evaluate_squad.py` uses the file as a benchmark for the pretrained SQuAD 2.0 QA model. The default run evaluates a repeatable sample of 100 rows; use `--all` to evaluate the full sheet, which takes longer.

```powershell
python evaluate_squad.py
python evaluate_squad.py --all
```

The report prints Exact Match and token-level F1 for all, answerable, and unanswerable examples. The checkpoint is already SQuAD 2.0 fine-tuned, so this is evaluation, not fine-tuning. For university-specific quality, also create a small separate question set from the manual and check the app's cited answers manually.

## How it works

PyMuPDF extracts text page by page from PDFs in `data/manuals/` and `output/pdf/`. The app splits pages into overlapping passages, ranks them with a simple keyword match, and asks the pretrained extractive QA model to find an answer in the best passages. It displays the source filename and page and shows the supporting passage on request.

The included **Sample University Student IT Services Manual** is synthetic demonstration content, not an official university policy. See the notice on its cover.

## Current limitations

- Scanned PDFs need OCR first; this demo reads selectable PDF text.
- Keyword retrieval and the `0.15` score threshold are simple demo choices, not a guarantee of correctness. Check every answer against its cited passage.
- The model is not fine-tuned on university-specific questions. Fine-tuning and a larger labeled FAQ set are possible future work.
- Page citations refer to PDF page numbers, which may differ from printed page labels.

## Evaluation to include in the submission

Create a small table of questions from the manual, expected answers, the app's answers, cited pages, and whether each result was correct. Include both answerable and unanswerable questions. Report the number correct and discuss failures; do not present the demo threshold as a validated safety guarantee.
