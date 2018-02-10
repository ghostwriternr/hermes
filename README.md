# Hermes

The messenger of the gods himself delivering important notices from various IITKGP noticeboards

## Motivation

IITKGP has a lot of internal and public noticeboards that most students are not aware of, but will definitely benefit from. Hermes aims to solve this by monitoring the noticeboards and sending updates to students by email.

## Setup

### Install dependencies

Install all required python modules.

```bash
pip install -r requirements.txt
```

### Mailgun setup

Hermes uses Mailgun's APIs to send emails. Setting up an account and registering a new domain is easy and well explained in their [official documentation](https://documentation.mailgun.com/en/latest/quickstart.html).

### Required config variables

Hermes requires Mailgun specific environment variables to work.

```sh
MAILGUN_API_KEY="xxx" # API key from Mailgun dashboard
MAILGUN_DOMAIN="xxx" # Configured domain at Mailgun from which to send emails
FIRST_RUN="false" # Set to either "true" or "false". If true, the scrapers will check ALL notices. Only last 10 otherwise.
TARGET_EMAIL="xxx" # Target email address
VERITAS_URL="xxx" # URL for Veritas
```

Now the big trouble is, Hermes needs to be run within the institute (since the internal noticeboards are not accessible from outside campus). BUT the administration doesn't provide `sudo` access to a permanant server to set this up (because ¯\\\_(ツ)\_/¯). So, [Veritas](https://github.com/ghostwriternr/veritas) is another helper script that can handle storing the scraped notices (and their MD5 hashes) on an independent server hosted outside campus.

So, setup and run Veritas before running Hermes. Instructions for running Veritas is provided in it's README. The `VERITAS_URL` env variable required above should point to wherever Veritas is hosted.

## License

GPLv3. Issues and pull requests are welcome.
