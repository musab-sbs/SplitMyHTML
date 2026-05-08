"""
html_splitter.py
Splits a large HTML file into smaller numbered batch files for AI processing.
"""

from bs4 import BeautifulSoup
import os
import math
import argparse

def split_html(input_file, output_dir="batches", batch_size=50, split_by="tags"):
    """
    Split an HTML file into smaller batches.

    Args:
        input_file  : path to the source HTML file
        output_dir  : folder where batch files are saved
        batch_size  : number of elements (or KB) per batch
        split_by    : "tags"  – split by number of top-level tags
                      "chars" – split by character count (batch_size = KB per chunk)
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # ── Split by top-level tags ────────────────────────────────────────────────
    if split_by == "tags":
        elements = soup.body.find_all(recursive=False) if soup.body else soup.find_all(recursive=False)

        if not elements:
            print("No top-level elements found. Try split_by='chars' instead.")
            return

        total_batches = math.ceil(len(elements) / batch_size)
        print(f"Found {len(elements)} top-level elements → {total_batches} batches")

        for i in range(total_batches):
            chunk = elements[i * batch_size : (i + 1) * batch_size]
            batch_html = "\n".join(str(el) for el in chunk)

            out_path = os.path.join(output_dir, f"{base_name}_batch_{i+1:03d}.html")
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(f"<!-- Batch {i+1} of {total_batches} -->\n")
                out.write(batch_html)

            print(f"  ✓ {out_path}  ({len(chunk)} elements)")

    # ── Split by character count (KB) ─────────────────────────────────────────
    elif split_by == "chars":
        chunk_size = batch_size * 1024  # convert KB → bytes
        total_batches = math.ceil(len(content) / chunk_size)
        print(f"File size: {len(content)//1024} KB → {total_batches} batches (~{batch_size} KB each)")

        for i in range(total_batches):
            chunk = content[i * chunk_size : (i + 1) * chunk_size]
            out_path = os.path.join(output_dir, f"{base_name}_batch_{i+1:03d}.html")
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(f"<!-- Batch {i+1} of {total_batches} -->\n")
                out.write(chunk)
            print(f"  ✓ {out_path}  ({len(chunk)//1024} KB)")

    else:
        raise ValueError("split_by must be 'tags' or 'chars'")

    print(f"\nDone! All batches saved to → ./{output_dir}/")


# ── CLI ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a large HTML file into AI-readable batches.")
    parser.add_argument("input",        help="Path to the HTML file")
    parser.add_argument("--output-dir", default="batches",  help="Output folder (default: batches/)")
    parser.add_argument("--batch-size", default=50, type=int, help="Tags per batch OR KB per batch (default: 50)")
    parser.add_argument("--split-by",   default="tags", choices=["tags", "chars"], help="Split strategy (default: tags)")
    args = parser.parse_args()

    split_html(args.input, args.output_dir, args.batch_size, args.split_by)