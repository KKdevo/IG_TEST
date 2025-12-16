from generate_report import *
from docx import Document

doc = Document('Content-Schedule-Template-v3-clean.docx')
ts = extract_tables_with_hyperlinks(doc)
ident = identify_tables(ts, doc)
posts = parse_posts_table(ident['posts_schedule'])

print("Posts with MediaURL:")
for p in posts[:10]:
    url = p.get("MediaURL", "NONE")
    print(f"{p['Title'][:35]:35} | {url[:70] if url else 'NONE'}")
