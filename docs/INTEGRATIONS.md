# Integration Stubs

This document lists integrations that can extend your AI assistant. These are "Level 2+" features - not needed to get started, but available when you're ready to expand.

---

## Currently Included

### Google Workspace (via gogcli)
- **Gmail** - Read, search, draft emails
- **Calendar** - View, create, modify events
- **Contacts** - Look up contact information
- **Drive** - Search and access files

**Status:** Included in starter kit

---

## Coming Soon / DIY

### Accounting Systems

| System | Use Cases | API Docs |
|--------|-----------|----------|
| **QuickBooks** | Invoices, expenses, P&L | [developer.intuit.com](https://developer.intuit.com/) |
| **Xero** | Financial reporting | [developer.xero.com](https://developer.xero.com/) |
| **Zoho Books** | Full accounting | [zoho.com/books/api](https://www.zoho.com/books/api/v3/) |

**Example queries:** "Show unpaid invoices over 30 days" / "What were expenses last month?"

---

### E-commerce

| System | Use Cases | API Docs |
|--------|-----------|----------|
| **Shopify** | Orders, inventory, customers | [shopify.dev](https://shopify.dev/docs/api) |
| **Amazon Seller** | Marketplace operations | [developer-docs.amazon.com](https://developer-docs.amazon.com/sp-api/) |
| **WooCommerce** | WordPress e-commerce | [woocommerce.github.io](https://woocommerce.github.io/woocommerce-rest-api-docs/) |

**Example queries:** "What were today's orders?" / "Check inventory for [product]"

---

### CRM

| System | Use Cases | API Docs |
|--------|-----------|----------|
| **HubSpot** | Contacts, deals, pipelines | [developers.hubspot.com](https://developers.hubspot.com/) |
| **Salesforce** | Enterprise CRM | [developer.salesforce.com](https://developer.salesforce.com/) |
| **Zoho CRM** | Sales automation | [zoho.com/crm/developer](https://www.zoho.com/crm/developer/) |
| **Pipedrive** | Sales pipeline | [developers.pipedrive.com](https://developers.pipedrive.com/) |

**Example queries:** "Find all contacts at [company]" / "What deals close this month?"

---

### Marketing & Advertising

| System | Use Cases | API Docs |
|--------|-----------|----------|
| **Meta Ads** | Facebook/Instagram ads | [developers.facebook.com](https://developers.facebook.com/docs/marketing-apis) |
| **Google Ads** | Search/display advertising | [developers.google.com/google-ads](https://developers.google.com/google-ads/api/docs/start) |
| **Klaviyo** | Email marketing | [developers.klaviyo.com](https://developers.klaviyo.com/) |
| **Mailchimp** | Email campaigns | [mailchimp.com/developer](https://mailchimp.com/developer/) |

**Example queries:** "How are ads performing this week?" / "What's our email open rate?"

---

### Team Communication

| System | Use Cases | API Docs |
|--------|-----------|----------|
| **Slack** | Team messaging | [api.slack.com](https://api.slack.com/) |
| **Microsoft Teams** | Enterprise collaboration | [docs.microsoft.com/graph](https://docs.microsoft.com/en-us/graph/teams-concept-overview) |
| **Discord** | Community/team chat | [discord.com/developers](https://discord.com/developers/docs) |
| **Zoho Cliq** | Business chat | [zoho.com/cliq/api](https://www.zoho.com/cliq/help/restapi/) |

**Example queries:** "Send update to [channel]" / "What's been discussed in [channel] today?"

---

### AI Content Tools

| Tool | Purpose | Access |
|------|---------|--------|
| **Google Gemini** | Text, image, multimodal | [ai.google.dev](https://ai.google.dev/) |
| **Veo** | Video generation | Via Google AI |
| **Kling** | AI video/animation | [klingai.com](https://klingai.com/) |
| **Midjourney** | Image generation | [midjourney.com](https://www.midjourney.com/) |
| **ElevenLabs** | Voice synthesis | [elevenlabs.io](https://elevenlabs.io/) |

**Example workflow:** AI helps craft prompts for these tools based on your creative vision.

---

### Productivity

| System | Use Cases | API Docs |
|--------|-----------|----------|
| **Todoist** | Task management | [developer.todoist.com](https://developer.todoist.com/) |
| **Notion** | Workspace/wiki | [developers.notion.com](https://developers.notion.com/) |
| **Linear** | Issue tracking | [linear.app/developers](https://linear.app/developers) |
| **Airtable** | Structured data | [airtable.com/developers](https://airtable.com/developers) |

---

### Infrastructure

| System | Use Cases | API Docs |
|--------|-----------|----------|
| **AWS** | Cloud infrastructure | [aws.amazon.com/documentation](https://aws.amazon.com/documentation/) |
| **GitHub** | Code repositories | [docs.github.com/rest](https://docs.github.com/en/rest) |
| **Cloudflare** | DNS, CDN | [developers.cloudflare.com](https://developers.cloudflare.com/) |

---

## Building Custom Integrations

Most services have REST APIs. Pattern for creating a new integration:

```python
# tools/my-service.py
import os
import requests

API_KEY = os.environ.get('MY_SERVICE_API_KEY')
BASE_URL = 'https://api.myservice.com/v1'

def get_data(endpoint):
    response = requests.get(
        f'{BASE_URL}/{endpoint}',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    import sys
    print(get_data(sys.argv[1] if len(sys.argv) > 1 else 'status'))
```

**Steps:**
1. Get API credentials from the service
2. Store securely (environment variable or AWS Secrets Manager)
3. Create Python tool that calls the API
4. Add to your toolkit

Your AI can help you build these integrations - just describe what you want to connect and it will help create the tool.

---

*This list will grow as the community builds and shares integrations.*
