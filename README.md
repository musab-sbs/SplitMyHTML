# 🗂️ HTML Batch Splitter

Split large exported HTML files — AI chat histories, email archives, and similar exports — into smaller, AI-readable batches.

## Why?

Most AI tools have a context window limit. If you've ever tried to feed a full export of your ChatGPT history, Gmail archive, or any long HTML document into an AI, you've hit that wall. This tool chops those files into clean, numbered batches you can process one at a time.

**Works great with:**
- Exported AI chat histories (ChatGPT, Claude, etc.)
- Email archives (Gmail Takeout, Outlook exports)
- Browser-saved web pages
- Any large HTML file you need an AI to read

---

## Requirements

- Python 3.7+ (tested on 3.14)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

Install the dependency:

```bash
pip install beautifulsoup4
```

---

## Usage

### Basic — split by HTML tags (default)

```bash
python html_splitter.py myfile.html
```

Splits the file into batches of 50 top-level HTML elements each.

### Split by file size (KB)

Better for files with deeply nested or irregular structure:

```bash
python html_splitter.py myfile.html --split-by chars --batch-size 30
```

### All options

```bash
python html_splitter.py <input> [--output-dir DIR] [--batch-size N] [--split-by tags|chars]
```

| Argument | Default | Description |
|---|---|---|
| `input` | *(required)* | Path to your HTML file |
| `--output-dir` | `batches/` | Folder to save the output files |
| `--batch-size` | `50` | Tags per batch (or KB per batch if using `chars`) |
| `--split-by` | `tags` | Split strategy: `tags` or `chars` |

---

## Output

A `batches/` folder is created containing numbered files:

```
batches/
├── myfile_batch_001.html
├── myfile_batch_002.html
├── myfile_batch_003.html
└── ...
```

Each file includes a comment at the top indicating its position:

```html
<!-- Batch 1 of 12 -->
```

Your original file is never modified.

---

## Tips

- **For chat exports:** `--split-by tags` works best since each message is usually its own element.
- **For email archives:** try `--split-by chars --batch-size 20` if the tag structure is deeply nested.
- **Feeding to an AI:** tell the AI the batch number and total (e.g. *"This is batch 3 of 12"*) so it can keep track of context across your session.

---

## License

MIT