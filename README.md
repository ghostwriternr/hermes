# Hermes

The messenger of the gods himself delivering important notices from various IITKGP noticeboards

## Motivation

IITKGP has a lot of internal and public noticeboards that most students are not aware of, but will definitely benefit from. Hermes aims to solve this by monitoring the noticeboards and sending updates to students by email.

## Setup

Hermes requires MongoDB and Mailgun specific environment variables to work.

### Required config variables

```sh
MAILGUN_API_KEY="xxx" # API key from Mailgun dashboard
MAILGUN_DOMAIN="xxx" # Configured domain at Mailgun from which to send emails
MONGODB_URI="xxx" # MongoDB URI
FIRST_RUN="false" # Set to either "true" or "false". If true, the scrapers will check ALL notices. Only last 10 otherwise.
TARGET_EMAIL="xxx" # Target email address
```

## License

GPLv3. Issues and pull requests are welcome.
