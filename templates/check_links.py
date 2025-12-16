from docx import Document
import re

doc = Document('Content-Schedule-Template-v3-clean.docx')
doc_rels = doc.part.rels

# Find posts table
for i, table in enumerate(doc.tables):
    headers = [c.text.strip().lower() for c in table.rows[0].cells]
    if 'title' in headers and 'type' in headers:
        print('Checking for hyperlinks in Photo Links column...\n')
        photo_idx = 3  # Photo Links column
        
        for row_idx, row in enumerate(table.rows[1:8], 1):
            cell = row.cells[photo_idx]
            cell_xml = cell._tc.xml
            
            # Find rId references for hyperlinks
            rids = re.findall(r'r:id="(rId\d+)"', cell_xml)
            urls = []
            for rid in rids:
                if rid in doc_rels:
                    rel = doc_rels[rid]
                    if 'hyperlink' in rel.reltype.lower():
                        urls.append(rel.target_ref)
            
            title = row.cells[0].text.strip()[:30]
            visible_text = cell.text.strip()[:30] if cell.text.strip() else "(empty)"
            print(f'Row {row_idx}: {title}')
            print(f'   Text: {visible_text}')
            print(f'   URLs: {urls if urls else "None found"}')
            print()
        break
