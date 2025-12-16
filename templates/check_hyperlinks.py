from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT

doc = Document('Content-Schedule-Template-v3-clean.docx')
t = doc.tables[1]

# Get the relationship part for hyperlinks
rels = doc.part.rels

print("Checking Photo Links column (index 3) for hyperlinks:\n")
for i, row in enumerate(t.rows[1:8]):
    cell = row.cells[3]
    print(f"Row {i+1}: Title='{row.cells[0].text[:30]}' | Display='{cell.text}'")
    
    # Check for hyperlinks in cell
    for p in cell.paragraphs:
        for hl in p._element.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink'):
            r_id = hl.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            if r_id and r_id in rels:
                print(f"   -> Hyperlink: {rels[r_id].target_ref}")
    print()
