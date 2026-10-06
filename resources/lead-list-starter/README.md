# Lead-list starter asset

The buyer-facing guide is `index.html`, published at `/resources/lead-list-starter/`. The blog index links to that guide; its download button serves `sample-leads.csv`. GitHub's rendering of this README is not the buyer experience.

The sample contains three fictional leads, two with an additional number, and one quoted company name containing a comma. Numbers are in NANPA's reserved 555-0100–0199 range; email addresses use IANA's example.com domain. Do not call or message them. Primary sources are linked in the HTML guide.

Parser acceptance: expect three matching names, company names and emails, three primary numbers and two preserved additional numbers. The blank additional number stays absent. Source-parser validation is not an iPhone UI import test.

The blog-index placement is additive; existing cards, conversion copy, prices, campaigns, privacy policy and analytics configuration remain unchanged. The resource adds no scripts or tracking configuration.
