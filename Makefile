# Copyright (c) Aptos
# SPDX-License-Identifier: Apache-2.0

test:
	- poetry run python -m unittest discover -s aptos_sdk/ -p '*.py' -t ..

fmt:
	- find . -type f -name "*.py" | xargs poetry run autoflake -i -r --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports
	- find . -type f -name "*.py" | xargs poetry run isort
	- find . -type f -name "*.py" | xargs poetry run black

examples:
	- poetry run python -m examples.transfer-coin
	- poetry run python -m examples.simple-nft

nft_issuer:
	- poetry run python nft_issuer.py --get_collection test  --priv 0x878e74c7ddb401b61de91506bae07ece5ff2a1a74ebdead01c230e9df25fa445
	- poetry run python nft_issuer.py --get_collection test --get_token hello_token  --priv 0x878e74c7ddb401b61de91506bae07ece5ff2a1a74ebdead01c230e9df25fa445
	- poetry run python nft_issuer.py --transfer_to 0x67fa9c9160ddee9c0490d7234cab4057d6e45af384aac8a627a7ed3fe7000c21  --get_collection test --get_token hello_token  --priv 0x878e74c7ddb401b61de91506bae07ece5ff2a1a74ebdead01c230e9df25fa445
	- python nft_issuer.py --get_balance 0x077a25e5733ee25ddb9b6d188533369e3f058c0a0e82b97b5d196f699413e4d1  --get_collection test --get_token hello_token --priv 0x878e74c7ddb401b61de91506bae07ece5ff2a1a74ebdead01c230e9df25fa445

.PHONY: test fmt examples
