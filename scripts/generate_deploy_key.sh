#!/bin/bash

# Helper script to generate SSH deploy keys for GitHub

set -e

KEY_NAME="${1:-.github/deploy_key}"
KEY_TYPE="${2:-rsa}"

echo "=== GitHub Deploy Key Generator ==="
echo ""
echo "Generating SSH key: $KEY_NAME"
echo "Key type: $KEY_TYPE"
echo ""

# Generate SSH key
ssh-keygen -t "$KEY_TYPE" -f "$KEY_NAME" -N "" -C "deploy-key-colab"

echo ""
echo "✓ Key generated successfully!"
echo ""
echo "Public key path: ${KEY_NAME}.pub"
echo "Private key path: ${KEY_NAME}"
echo ""
echo "To add to GitHub:"
echo "1. Go to your repository Settings > Deploy keys"
echo "2. Click 'Add deploy key'"
echo "3. Paste the contents of: $(cat ${KEY_NAME}.pub)"
echo "4. Check 'Allow write access' if needed"
echo ""
echo "To use in Colab:"
echo "1. Upload the private key to Colab"
echo "2. Configure SSH to use it"
echo "3. Set git remote to use SSH: git@github.com:user/repo.git"
