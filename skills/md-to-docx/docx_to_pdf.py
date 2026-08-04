"""docx_to_pdf - convert Word documents to PDF via Word COM.

The second entry point of the md-to-docx skill, and the SHARED PDF engine for
the whole skill: md_to_docx.py --pdf calls straight into this file, so there is
only ever one implementation of the Word COM call to maintain.

Use this directly when the .docx did NOT come from markdown - the Freedom
Blueprint newsletter, the year-end accountant pack, webinar user guides, or
anything Mick has hand-edited in Word.

Usage:
    python docx_to_pdf.py "<file.docx>"
    python docx_to_pdf.py "<file.docx>" -o "<folder or file.pdf>"
    python docx_to_pdf.py "<folder>"                    (every .docx in it)
    python docx_to_pdf.py "<folder>" --recurse
    python docx_to_pdf.py "<a.docx>" "<b.docx>" "<folder>"
    python docx_to_pdf.py "<folder>" --skip-existing
    python docx_to_pdf.py "<file.docx>" --no-bookmarks --screen

Why ExportAsFixedFormat rather than SaveAs:
    SaveAs(FileFormat=17) produces a flat PDF. ExportAsFixedFormat can carry
    the Word heading structure through as PDF bookmarks, so an eight-page
    research report or a six-page newsletter opens with a working navigation
    pane instead of nothing. It also carries the document properties and
    writes a tagged (accessible) PDF.

Batch runs open Word ONCE and convert every file through the same instance,
which is far faster than one Word launch per document.

Version: 1.0 (2026-08-04)
"""

import argparse
import os
import sys

# --------------------------------------------------------- Word COM constants

WD_EXPORT_FORMAT_PDF = 17
WD_EXPORT_OPTIMIZE_PRINT = 0
WD_EXPORT_OPTIMIZE_SCREEN = 1
WD_EXPORT_ALL_DOCUMENT = 0
WD_EXPORT_DOCUMENT_CONTENT = 0
WD_EXPORT_CREATE_NO_BOOKMARKS = 0
WD_EXPORT_CREATE_HEADING_BOOKMARKS = 1
WD_FORMAT_PDF = 17           # SaveAs fallback


def open_word():
    """Start a PRIVATE hidden Word instance. Returns the COM object, or None.

    DispatchEx, not Dispatch, and this matters. Dispatch ATTACHES to a Word
    that is already running - which would be Mick's own session, with his
    documents open. Quitting it afterwards would close his Word, and with
    DisplayAlerts off his unsaved changes could go without a prompt.
    DispatchEx always creates a separate, dedicated instance, so this script
    can only ever close the one it started.
    """
    try:
        import win32com.client
    except ImportError:
        print("ERROR: pywin32 is not installed - cannot drive Word.")
        print("       Install with: python -m pip install pywin32")
        return None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        return word
    except Exception as exc:                                    # noqa: BLE001
        print("ERROR: could not start Word - %s" % exc)
        return None


def close_word(word):
    if word is None:
        return
    try:
        word.Quit()
    except Exception:                                           # noqa: BLE001
        pass


def export(docx_path, pdf_path, word, bookmarks=True, screen=False):
    """Export one already-open Word instance's document to PDF.

    Returns the pdf path on success, None on failure.
    """
    docx_path = os.path.abspath(docx_path)
    pdf_path = os.path.abspath(pdf_path)
    doc = None
    try:
        # Open read-only, no add-to-recent-files, so the source is never touched.
        doc = word.Documents.Open(docx_path, False, True)
        try:
            doc.ExportAsFixedFormat(
                pdf_path,                       # OutputFileName
                WD_EXPORT_FORMAT_PDF,           # ExportFormat
                False,                          # OpenAfterExport
                WD_EXPORT_OPTIMIZE_SCREEN if screen else WD_EXPORT_OPTIMIZE_PRINT,
                WD_EXPORT_ALL_DOCUMENT,         # Range
                1,                              # From (ignored for all-document)
                1,                              # To   (ignored)
                WD_EXPORT_DOCUMENT_CONTENT,     # Item - content, not markup
                True,                           # IncludeDocProps
                True,                           # KeepIRM
                WD_EXPORT_CREATE_HEADING_BOOKMARKS if bookmarks
                else WD_EXPORT_CREATE_NO_BOOKMARKS,
                True,                           # DocStructureTags (tagged PDF)
                True,                           # BitmapMissingFonts
                False,                          # UseISO19005_1 (PDF/A off)
            )
        except Exception as exc:                                # noqa: BLE001
            # Older Word builds, or an odd document, can refuse the rich export.
            print("  NOTE: ExportAsFixedFormat failed (%s) - falling back to "
                  "SaveAs (no bookmarks)." % exc)
            doc.SaveAs(pdf_path, FileFormat=WD_FORMAT_PDF)
        return pdf_path
    except Exception as exc:                                    # noqa: BLE001
        print("  FAILED: %s - %s" % (os.path.basename(docx_path), exc))
        return None
    finally:
        if doc is not None:
            try:
                doc.Close(False)
            except Exception:                                   # noqa: BLE001
                pass


def convert_one(docx_path, pdf_path=None, bookmarks=True, screen=False):
    """Convert a single DOCX, handling the Word lifecycle. Returns pdf or None.

    This is the function md_to_docx.py calls for its --pdf flag.
    """
    if pdf_path is None:
        pdf_path = os.path.splitext(os.path.abspath(docx_path))[0] + ".pdf"
    word = open_word()
    if word is None:
        return None
    try:
        return export(docx_path, pdf_path, word, bookmarks, screen)
    finally:
        close_word(word)


def gather(targets, recurse=False):
    """Expand files and folders into a de-duplicated list of .docx paths."""
    found = []
    for target in targets:
        if os.path.isdir(target):
            if recurse:
                for root, _dirs, files in os.walk(target):
                    for name in files:
                        found.append(os.path.join(root, name))
            else:
                for name in os.listdir(target):
                    found.append(os.path.join(target, name))
        else:
            found.append(target)

    docs, seen = [], set()
    for path in found:
        if not os.path.isfile(path):
            print("SKIP (not found): %s" % path)
            continue
        name = os.path.basename(path)
        if name.startswith("~$"):
            continue                      # Word lock file
        if os.path.splitext(name)[1].lower() not in (".docx", ".doc"):
            continue
        key = os.path.abspath(path).lower()
        if key in seen:
            continue
        seen.add(key)
        docs.append(os.path.abspath(path))
    return docs


def main():
    ap = argparse.ArgumentParser(
        description="Convert Word documents to PDF via Word COM, with heading "
                    "bookmarks. Accepts files, folders, or a mix.")
    ap.add_argument("targets", nargs="+", help=".docx files and/or folders")
    ap.add_argument("-o", "--output",
                    help="output .pdf path (single file), or a folder for the "
                         "PDFs. Default: alongside each source document.")
    ap.add_argument("--recurse", action="store_true",
                    help="descend into subfolders when a folder is given")
    ap.add_argument("--skip-existing", action="store_true",
                    help="leave any PDF that already exists untouched")
    ap.add_argument("--no-bookmarks", dest="bookmarks", action="store_false",
                    help="do not create PDF bookmarks from Word headings")
    ap.add_argument("--screen", action="store_true",
                    help="optimise for on-screen (smaller file) instead of print")
    args = ap.parse_args()

    docs = gather(args.targets, args.recurse)
    if not docs:
        sys.exit("ERROR: no .docx files found in the given targets.")

    out_dir = None
    out_file = None
    if args.output:
        if os.path.isdir(args.output) or args.output.rstrip("\\/").endswith(
                (os.sep, "/")) or not os.path.splitext(args.output)[1]:
            out_dir = args.output
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)
        else:
            out_file = args.output
            if len(docs) > 1:
                sys.exit("ERROR: -o with a single .pdf filename needs exactly "
                         "one source document (%d found). Give a folder "
                         "instead." % len(docs))

    print("Converting %d document(s)%s..." %
          (len(docs), " with heading bookmarks" if args.bookmarks else ""))

    word = open_word()
    if word is None:
        sys.exit(1)

    done, skipped, failed = [], [], []
    try:
        for path in docs:
            if out_file:
                pdf = os.path.abspath(out_file)
            elif out_dir:
                pdf = os.path.join(os.path.abspath(out_dir),
                                   os.path.splitext(os.path.basename(path))[0]
                                   + ".pdf")
            else:
                pdf = os.path.splitext(path)[0] + ".pdf"

            if args.skip_existing and os.path.exists(pdf):
                print("  SKIP (exists): %s" % os.path.basename(pdf))
                skipped.append(pdf)
                continue

            result = export(path, pdf, word, args.bookmarks, args.screen)
            if result:
                size_kb = os.path.getsize(result) / 1024.0
                print("  OK: %s (%.0f KB)" % (os.path.basename(result), size_kb))
                done.append(result)
            else:
                failed.append(path)
    finally:
        close_word(word)

    print("\nConverted %d, skipped %d, failed %d." %
          (len(done), len(skipped), len(failed)))
    for path in failed:
        print("  FAILED: %s" % path)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
