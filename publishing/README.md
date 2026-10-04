# Aurora Publishing submission page / Google Forms setup

The page at https://www.aurora-studio.org/publishing/ has a working email fallback: **shikosama215@gmail.com**.

No published Google Form currently exists in the connected Google Drive, and Google Forms cannot be created through the available Drive connector. Never invent a public form URL.

## One-time setup (Google account owner)

1. Open https://script.google.com/home/projects/create while signed into the intended Google account.
2. Paste the code in `create-google-form.gs` and run `createAuroraPublishingForm()` once.
3. Grant the necessary Google Forms + Sheets access. Review the generated form, settings, response permissions and privacy notice before publishing.
4. Copy the **Published URL** (not edit URL) from Apps Script execution logs.
5. Put that URL inside the quotes in `form-config.js` and commit the change.
6. Verify that the public page shows the Google Form link/embedded form and submit a test response. Delete the test response when finished.
7. Keep the response spreadsheet restricted to authorized reviewers. Do not include credentials, pitch attachments, or internal submissions in GitHub.

The form asks for the game pitch, developer contact, build/demo link, development status and publishing assistance needed. Before the real launch, establish an internal data handling and deletion process.

The page is maintained as standalone static HTML; `build.py` generates other site pages, while `localize.py` generates the translated homepages. Running those scripts does not delete this page.
