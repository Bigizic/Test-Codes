sign up on pipe deream create a new workflow add a http triger, you will receivean endpoint to use, can send ajax post request to this endpoint without cors headers issues or axios post request or http post request, whichever yoou choose.

use the js code below to send an email using mailgun api and pipedream webhook 

```js
const API_KEY = ""
const SENDER = ""
const DOMAIN = ""
const RECIPIENT = "";

export default defineComponent({
  async run({ steps, $ }) {
    try {

      const inputData = steps.trigger.event.body;
      const userEmail = inputData.useremail || "No email provided";
      const userMessage = inputData.message || "No message provided";

      const url = `https://api.mailgun.net/v3/${DOMAIN}/messages`;
      const formBody = new URLSearchParams();
      formBody.append("from", ` <${SENDER}>`);
      formBody.append("to", RECIPIENT);
      formBody.append("subject", "New Contact Form Submission");
      formBody.append("text", `Email: ${userEmail}\n\nMessage:\n${userMessage}`);

      const response = await fetch(url, {
        method: "POST",
        headers: {
          Authorization: `Basic ${Buffer.from(`api:${API_KEY}`).toString("base64")}`,
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formBody.toString()
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Mailgun Error ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      return { status: "Email Sent!", mailgunResponse: data };

    } catch (error) {
      return { status: "Failed to send email", error: error.message };
    }
  }
});

```
