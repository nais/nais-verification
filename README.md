nais-verification
=================

A fasit-feature to create nais-verification team/namespace via NAIS Teams

Rough outline of how it works:

1. Feature is enabled in fasit
2. Install creates a Job which uses NAIS Teams API to create `nais-verification` team
3. Post-install hook uses NAIS Teams API to get `nais-verification` deploy key and saves it in a secret in the namespace
4. Profit!

### Verifying the nais-verification images and their contents

The images are signed "keylessly" using [Sigstore cosign](https://github.com/sigstore/cosign).
To verify their authenticity run
```
cosign verify \
--certificate-identity "https://github.com/nais/nais-verification/.github/workflows/main.yml@refs/heads/main" \
--certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
ghcr.io/nais/nais-verification@sha256:<shasum>
```

The images are also attested with SBOMs in the [CycloneDX](https://cyclonedx.org/) format.
You can verify these by running
```
cosign verify-attestation --type cyclonedx  \
--certificate-identity "https://github.com/nais/nais-verification/.github/workflows/main.yml@refs/heads/main" \
--certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
ghcr.io/nais/nais-verification@sha256:<shasum>@sha256:<shasum>
```
