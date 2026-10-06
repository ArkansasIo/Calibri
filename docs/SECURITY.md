# AetherForge AI Security

## Secrets

Never commit API keys, cloud credentials, database passwords, SSH keys, certificates, or Wolfram App IDs.

Use environment variables or an appropriate local secret manager.

## Local models

Model files should be treated as untrusted external data until verified. Store large model files outside source control when practical.

## Agents

Agent permissions should default to safe mode and approval for consequential operations.

The development system should distinguish:

- read;
- analyze;
- propose;
- write;
- build;
- test;
- execute;
- destructive operations.

Destructive operations require explicit approval.

## Game-engine plugins

Keep local AI services outside shipping builds unless the developer intentionally chooses an embedded model architecture.

## External services

External providers such as Wolfram|Alpha and MiMoCode are optional integrations. AetherForge should never hard-code their credentials.

## Offline mode

The local AI path should continue to function without network access after the runtime and model assets have been installed.