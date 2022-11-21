nais-verification
=================

A fasit-feature to create nais-verification team/namespace via Console

Rough outline of how it works:

1. Feature is enabled in fasit
2. Install creates a Job which uses Console API to create `nais-verification` team
3. Post-install hook uses Console API to get `nais-verification` deploy key and saves it in a secret in the namespace
4. Profit!
