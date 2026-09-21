# Privacy Policy – Cold Call X

Effective September 19, 2026 · Version 2026-09-19

This Privacy Policy explains how Berberian Enterprises Inc. (“Cold Call X,” “we,” “us,” or “our”) handles information when you use Cold Call X.

## The short version

Cold Call X works on your iPhone, not on our servers. There is no account to create, and we do not collect, receive, or store your lead lists, notes, call history, or any other information you put into it. The one server we operate exists only to complete the optional HubSpot sign-in handshake and never sees your contacts. The App contains no advertising and does not track you across apps or websites. It does report app-only usage statistics — which features get used, and the on/off state of your settings — so we know what to improve; that report never includes anything from your leads, and you can turn it off in Settings.

## Information stored on your device

Lead lists, contact details you import, notes, tags, call outcomes, follow-ups, your in-app Do Not Call suppression list, message templates, call scripts, statistics, and preferences are stored locally on your device. Nothing in that data is uploaded to us. You control the lead data you import and must have the right to use it.

Follow-up reminders are scheduled as local notifications on your device. They are not sent through any server. If you choose to add a follow-up to your calendar, the App asks for calendar access and creates or updates that event in the calendar app; it does not read your other events. When you export a list, the App creates a CSV file and hands it to the iOS share sheet, and you choose where it goes.

If you turn on Inbound Caller ID, the App gives iOS the phone numbers, names, and companies in your lists, together with the outcome and date of your last call to each, so that an incoming call from one of them can be labelled. That list stays on your device and is managed by iOS.

The App keeps automatic daily backups of your on-device data so you can restore it if something goes wrong. By default the App also writes an encrypted copy of each backup to your own iCloud Drive so you can restore it on another device. Those backups are encrypted on your device with a key stored in your iCloud Keychain, are held in your Apple account rather than ours, and are not readable by us or by Apple. The App tells you about iCloud Backup the first time you open it and does not upload anything until you have seen that notice and accepted the Terms. You can turn iCloud Backup off, or delete your backups, in Settings at any time; if you turn it off, backups stay on your device only. If your device is signed out of iCloud or iCloud Drive is off, nothing is uploaded. Your Google, HubSpot, and Salesforce sign-in credentials are deliberately excluded from backups.

## Calls, texts, and email

Calls are placed by your iPhone's Phone app through your carrier. Texts, WhatsApp messages, and emails are handed to the messaging or mail app you choose. The App does not carry, record, or store call audio or message content. To tell whether a call you placed connected, the App observes only what iOS reports on the device: that a call is in progress, and when it started and ended. It never receives the number, the other party, or any audio, and it does not read your call history. Your carrier and the apps you hand off to process that traffic under their own policies.

## Optional Google integration

Google Sheets import is optional. If you turn it on, you sign in to Google with OAuth and the App accesses the following Google user data, and nothing else:

- **Your Google account name and email address**, so the App can show which account is connected.
- **The names and IDs of the spreadsheets in your Google Drive**, so the App can show you a list to choose from. Google's consent screen describes this permission as access to your Drive files; the App uses it only to list spreadsheets by name and never opens or reads any file you do not select.
- **The cell contents of the spreadsheet tab you select**, which the App reads to build your calling list and, when you choose Refresh, to update it.
- **Notes sync**, which writes your call notes into the Notes column of a spreadsheet you imported. This is why the App asks Google for permission to edit your spreadsheets when you sign in. It writes only to the Notes column of a list you mapped one for, only for the leads in that list, and it changes no other cell, tab, or file. If you delete a lead's last note in the App, it clears that one cell so the sheet keeps matching the App. A list with no Notes column mapped is never written to.

This data is used only to provide the import and notes-sync features you asked for. It is stored only on your device, is never sent to us or to any third party, is not used for advertising, and is not sold. Your Google access token is stored in your device's keychain only and is excluded from backups. You can disconnect Google at any time in Settings, which removes the token from the App. Disconnecting does not withdraw the permission recorded in your Google account; you can revoke it at myaccount.google.com/permissions. Removing a list deletes the imported spreadsheet contents from the App.

Cold Call X's use and transfer of information received from Google APIs adheres to the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.

## Optional HubSpot integration

HubSpot import is optional. If you use it, you connect your HubSpot account by signing in with HubSpot (OAuth). The App then reads the HubSpot contacts you choose to import, every contact, only the ones assigned to you, or one of your HubSpot lists, and only these fields for each: first name, last name, phone, mobile phone, company, email, and the HubSpot record ID. To offer those choices it also reads the names and sizes of your contact lists and the record that identifies you as an owner.

The integration also writes to your HubSpot account, and only what you do in the App: each call outcome you record is logged on the contact as a call with the outcome you chose, the contact's lead status may move between HubSpot's standard statuses as a result (never over a status a person set, and you can turn this off), and the notes you type on a contact are saved as notes on that contact. Notes written on the contact in HubSpot are shown in the App. Clearing an outcome or deleting a note in the App removes the call or note the App created; the App never deletes anything it did not create. Nothing else in your HubSpot account is read or changed.

HubSpot's sign-in can only return to a web address, not directly to an app. So, when you sign in with HubSpot, a small server we operate (a Cloudflare Worker) receives the sign-in code from HubSpot, exchanges it for your access token using our app's credentials, and passes the token to the App on your device. The server does the same when the token needs renewing. It passes the tokens to the App and does not retain them, and it never receives your contacts or any other information from your HubSpot account. Like any web request, that handshake exposes your device's IP address to our server for the moment it takes. Everything else, reading contacts and logging calls and notes, goes directly between your device and HubSpot.

The imported contacts are stored on your device like any other list, and your HubSpot token is stored in your device's keychain only and is excluded from backups. You can log out of HubSpot at any time in Settings, which removes the token from the App; lists you imported stay on your device until you delete them. Logging out does not withdraw the permission recorded in your HubSpot account; you can remove it under Connected Apps in HubSpot.

## Optional Salesforce integration

Salesforce import is optional. If you use it, you connect your Salesforce org by signing in with Salesforce (OAuth). The App then reads the leads or contacts you choose to import, every record you can see, only the ones you own, or one of your list views, and only these fields for each: first name, last name, phone, mobile phone, company or account name, title, email, and the Salesforce record ID. To offer those choices it also reads the names of your list views, and to match your call outcomes it reads your org's list of call results and lead statuses.

The integration also writes to your Salesforce org, and only what you do in the App: each call outcome you record is logged on the lead or contact as a completed call task with the outcome you chose, the lead's status may move to the status you paired with that outcome (only from a status the App manages or your org's default, and only if you turn this on), and the notes you type on a lead or contact are saved as notes on that record. Notes written on the record in Salesforce are shown in the App. Clearing an outcome or deleting a note in the App removes the task or note the App created; the App never deletes anything it did not create. Nothing else in your Salesforce org is read or changed.

Salesforce's sign-in returns directly to the App, so no server of ours is involved: the sign-in, reading records, and logging calls and notes all go directly between your device and Salesforce.

The imported records are stored on your device like any other list, and your Salesforce token is stored in your device's keychain only and is excluded from backups. You can log out of Salesforce at any time in Settings, which removes the token from the App and asks Salesforce to revoke it; lists you imported stay on your device until you delete them. You can also remove the App's access under Connected Apps OAuth Usage in Salesforce Setup.

## Usage statistics

The App reports app-only usage statistics by default so we can see which features are used and which are not. You can turn this off at any time in Settings → Data → Share Analytics, and collection stops immediately. Unsent events are discarded and active upload requests are aborted; this cannot recall events the service has already received. Your choice is preserved when you restore a backup.

**What is sent.** Product-interaction events — which controls and screens are used, onboarding steps, settings changes, and whether operations such as imports, messages, connections, and backups complete, fail, or are cancelled — together with the state of your settings and a few counts (how many lists you have, how many message templates you have edited, your daily dial goal), and the size of an imported list as a band rather than an exact number. Errors are reported as a fixed code identifying what failed, such as "a refresh was refused" — never the error message itself.

**What is never sent.** No lead data of any kind. No names, phone numbers, email addresses, business names, notes or comments, call scripts, message templates, list names, or search terms. Nothing from a connected CRM: no record IDs, portal or organization IDs, and none of your organization's own wording for its statuses or call outcomes — where the App needs to report that you used a CRM filter, it reports only that it was a CRM filter. Your device's IP address is not stored and your location is not collected or derived.

**How it is identified.** It is not. Every report carries the same fixed label, identical on every installation of the App, so reports cannot be grouped by device or by person. There is no installation identifier, no returning-user history, and no individual timeline of what you did: actions are combined into counters before they are sent, and each carries a reporting day rather than the moment you did them. We do not create analytics person profiles, record screens, or collect typed content. Nothing sent is your name, email, phone number, Apple ID, or your device's advertising identifier, and nothing is linked to an account, because the App has none.

**Who processes it.** PostHog, acting as our processor, on servers in the United States. It is not used for advertising, is not sold, and is not shared with data brokers or combined with information from other companies to track you. If you are in the United Kingdom, the European Union, or Australia, this means the statistics described above are transferred to the United States; no lead data is involved in that transfer.

**Before you have accepted the Terms**, nothing at all is sent. Section 6.6 of the Terms describes this feature, and a new or upgrading user is asked to accept the current Terms before any report is made.

## Purchases

Apple processes App Store purchases. We do not receive your name, Apple ID, or payment details.

## Support

If you write to us at support@coldcallx.app, we use your message and email address to respond. That correspondence is the only personal information about you that we hold, and we keep it only as long as needed to help you and to keep a record of the request.

## Retention

On-device information remains until you delete it, clear the App's data, or uninstall the App, subject to iOS backup behavior. While iCloud Backup is on, encrypted copies remain in your iCloud Drive until you delete them in Settings or remove them yourself from the Files app. Turning iCloud Backup off stops new uploads but keeps the copies already there until you delete them. App-only usage statistics are kept by our analytics provider for as long as they are useful for product decisions. They contain no lead data and no account identity, and because every report carries the same fixed label there is nothing in them that ties one report to another, to a device, or to you.

## Deletion and choices

You can delete lead lists, notes, follow-ups, and your Do Not Call list in the App, disconnect Google or log out of HubSpot or Salesforce in Settings, turn off or delete backups in Settings, and turn off Share Analytics in Settings → Data. Uninstalling the App removes its on-device data; encrypted backups already in your iCloud Drive remain until you delete them in Settings before uninstalling or remove them from the Files app.

## Australian privacy rights

If you are in Australia, you may ask us to give you access to, or correct, personal information about you that we hold, subject to any exceptions under applicable law. You may also complain about how we have handled your personal information. Contact us at support@coldcallx.app; we will respond within a reasonable period and explain any refusal where required. If you are not satisfied with our response, you may be able to complain to the Office of the Australian Information Commissioner at [oaic.gov.au](https://www.oaic.gov.au/).

Lead and calling data that remains only on your device or in your own iCloud account is not accessible to us. Requests concerning that data must be managed using the App, your device, or your Apple account.

## Security

Your data is protected by iOS device security and, for backups, by encryption with a key held in your keychain. No system is completely secure, and we cannot guarantee absolute security.

## Children

Cold Call X is not directed to children. You must be at least 18 years old to use the App.

## Availability and international processing

The App is offered for use in the United States, Canada, the United Kingdom, and Australia. We are established in the United States. Because the App does not send your lead data to us, the only information that can leave your country is support correspondence you choose to send, which we read and store in the United States; the app-only usage statistics described above, which our analytics provider processes in the United States and which you can switch off in Settings; and, if you sign in with HubSpot, the sign-in handshake described above, which passes through our server in the United States.

## Changes

We may update this policy as the App or law changes. We will update the effective date and, when a change is material, provide an in-app notice or require renewed acceptance where appropriate.

## Contact

Berberian Enterprises Inc.<br>
support@coldcallx.app
