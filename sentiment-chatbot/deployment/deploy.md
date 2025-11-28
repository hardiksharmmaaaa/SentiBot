# Deploy to Google Cloud Run

Follow these steps to deploy your Sentiment Chatbot to Google Cloud Run. This will give you a public URL (e.g., `https://sentibot-xyz.a.run.app`) that you can share with anyone.

## Prerequisites

1.  **Google Cloud Project**: Create a project at [console.cloud.google.com](https://console.cloud.google.com/).
2.  **Billing**: Enable billing for your project (Cloud Run has a generous free tier, but requires billing setup).
3.  **gcloud CLI**: Install and authenticate the Google Cloud CLI.
    ```bash
    gcloud auth login
    gcloud config set project YOUR_PROJECT_ID
    ```

## Deployment Steps

### 1. Enable Services
Enable the necessary Google Cloud APIs:
```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### 2. Build and Deploy
The previous method failed because Cloud Run tried to use Buildpacks instead of our Dockerfile. We will use the explicit 2-step method to force the Docker build.

**Step 2a: Build the Container Image**
Run this command to build the image using the `Dockerfile` in the current directory.
**Important**: Make sure you are in the `sentiment-chatbot` directory and include the `.` at the end of the command.

```bash
cd sentiment-chatbot
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/sentibot .
```

**Step 2b: Deploy the Image**
Once the build is successful, deploy that specific image.
*(Replace `YOUR_PROJECT_ID` and `YOUR_API_KEY`)*

```bash
gcloud run deploy sentibot \
  --image gcr.io/YOUR_PROJECT_ID/sentibot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_API_KEY
```

### 3. Access Your App
Once the deployment finishes, the command will output a Service URL.
Example: `https://sentibot-randomhash-uc.a.run.app`

Click that link to use your live chatbot!

## Troubleshooting

-   **Build Failures**: If the build fails, check the Cloud Build logs provided in the terminal.
-   **Application Errors**: If the app deploys but errors out, check the logs:
    ```bash
    gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=sentibot" --limit 20
    ```
