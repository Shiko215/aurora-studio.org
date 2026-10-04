/**
 * Aurora Publishing / Submit Your Game
 * Run createAuroraPublishingForm() once in YOUR OWN Google Apps Script account:
 * https://script.google.com/home/projects/create
 *
 * Review the resulting form's settings and privacy notice before sharing.
 * Paste the published viewform URL logged below into /publishing/form-config.js.
 * Do not commit private response spreadsheets or credentials.
 */
function createAuroraPublishingForm() {
  const title = 'Aurora Publishing | Submit Your Game';
  const form = FormApp.create(title);
  form.setDescription(
    'Aurora Studio (Hong Kong) is exploring indie publishing partnerships. ' +
    'Submitting does not guarantee publishing, funding, an NDA or a response. ' +
    'Do not include confidential builds, source code, financial statements or sensitive personal details. ' +
    'For privacy or removal requests: shikosama215@gmail.com. ' +
    'English / 中文 / 日本語 accepted.'
  );
  form.setCollectEmail(false);
  form.setConfirmationMessage('Thank you. Your game pitch has been received for preliminary review. A submission does not guarantee a reply or publishing agreement.');
  const email = form.addTextItem().setTitle('Contact email / 聯絡電郵 / メール').setRequired(true);
  email.setValidation(FormApp.createTextValidation().requireTextIsEmail().build());
  form.addTextItem().setTitle('Developer / studio name').setRequired(true);
  form.addTextItem().setTitle('Country or region').setRequired(true);
  form.addTextItem().setTitle('Game title').setRequired(true);
  form.addParagraphTextItem().setTitle('Elevator pitch (2–5 sentences)').setRequired(true);
  form.addTextItem().setTitle('Genre and target platforms').setRequired(true);
  form.addMultipleChoiceItem().setTitle('Development stage').setChoiceValues(['Concept / Prototype','Playable demo','Alpha / Beta','Near release','Released']).setRequired(true);
  form.addTextItem().setTitle('Demo or gameplay video URL (no credentials)').setRequired(true);
  form.addTextItem().setTitle('Steam / itch.io / indienova page URL (optional)');
  form.addTextItem().setTitle('Expected launch period (approximate)');
  form.addTextItem().setTitle('Team size (optional)');
  form.addCheckboxItem().setTitle('Partnership interests').setChoiceValues(['Steam release planning','International marketing / PR','Japan / Hong Kong / Taiwan outreach','Localization','Creator / influencer campaigns','Co-publishing / funding discussion','Other']).setRequired(true);
  form.addParagraphTextItem().setTitle('What support are you looking for?').setRequired(true);
  form.addParagraphTextItem().setTitle('Budget, timetable, or other context (optional; no sensitive details)');
  form.addCheckboxItem().setTitle('Rights & privacy confirmation').setChoiceValues([
    'I am authorized to submit these materials and consent to Aurora Studio reviewing the information to assess a potential partnership and contacting me about this pitch.'
  ]).setRequired(true);
  const sheet = SpreadsheetApp.create('Aurora Publishing - Game Submissions (Private)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());
  Logger.log('Published URL: ' + form.getPublishedUrl());
  Logger.log('Edit URL: ' + form.getEditUrl());
  Logger.log('Private response spreadsheet: ' + sheet.getUrl());
}
