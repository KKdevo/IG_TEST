# Social Media Report Generator

## What's Included

1. **content-schedule-template.docx** - Your Word template to fill in
2. **generate_report.py** - Python script that converts your Word doc to a slick HTML report

---

## Your Workflow

### Step 1: Fill Out the Word Template

Open `content-schedule-template.docx` and replace all the `[placeholder text]` with your actual content:

**Title Page**
- Account Name: Replace `[Enter Client/Account Name]`
- Date Created: Replace `[Enter Date - e.g., June 2025]`

**Section 1: Posting Schedule**
- Fill in each row with your posts
- Type options: `post`, `reel`, `highlight`
- Status options: `Draft`, `Approved`, `Posted`, `Needs Revision`
- Add more rows by copying existing rows

**Section 2: Draft Posts**
- Fill in the detail blocks for each post
- For images: Use direct URLs (see "Image URLs" below)
- Copy/paste the table blocks to add more posts

**Section 3: Stories**
- Fill in the stories table
- Add image URLs for story preview thumbnails

**Section 4: Interactions**
- Add accounts to engage with
- Mark days complete with `X` or `✓`

---

### Step 2: Run the Generator

```bash
python generate_report.py your-file.docx
```

This creates `your-file_report.html` in the same folder.

Or specify a custom output name:
```bash
python generate_report.py your-file.docx my-client-report.html
```

---

### Step 3: View & Share

- Open the HTML file in any browser
- Send to clients (they just need a browser)
- Print to PDF if needed (Ctrl+P / Cmd+P)

---

## Image URLs

The report displays images from URLs. Here's how to get them:

### Google Drive
1. Upload image to Google Drive
2. Right-click → Share → "Anyone with link can view"
3. Copy the share link, it looks like:
   `https://drive.google.com/file/d/ABC123XYZ/view`
4. Convert to direct URL:
   `https://drive.google.com/uc?export=view&id=ABC123XYZ`

### Imgur (Quick & Easy)
1. Go to imgur.com
2. Drag and drop your image
3. Right-click the image → "Copy image address"
4. Use that URL directly

### Already-hosted images
If your images are on a website, right-click → "Copy image address"

---

## Video URLs

For Reels, use YouTube or Vimeo links:
- YouTube: `https://youtube.com/watch?v=XXXXX`
- YouTube short: `https://youtu.be/XXXXX`
- Vimeo: `https://vimeo.com/XXXXX`

The report will auto-embed them.

---

## Requirements

- Python 3.x
- python-docx library

Install with:
```bash
pip install python-docx
```

---

## Tips

1. **Making more posts**: Copy any post table block and paste it below
2. **Adding more schedule rows**: Copy a table row and paste
3. **Titles must match**: The post title in the Schedule table should match the Title in the detail block for proper merging
4. **Empty rows are ignored**: Leave placeholder text in brackets `[like this]` and it won't show up

---

## Troubleshooting

**Images not showing?**
- Make sure the URL is a direct image link (ends in .jpg, .png, or is a Google Drive direct URL)
- Check that Google Drive images are shared as "Anyone with link"

**Script errors?**
- Make sure python-docx is installed: `pip install python-docx`
- Make sure you're passing a .docx file, not .doc

