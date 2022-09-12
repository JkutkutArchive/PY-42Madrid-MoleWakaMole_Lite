#!/bin/bash

SECRETS_FILE="API42/__secrets__.py"
EXECUTABLE="main.py"

getSecrets() {
	rm -f $SECRETS_FILE
	echo "Credential's setup:"
	echo "Enter Molewakamole's credentials:"
	read -p "UID: " uid
	read -p "Secret: " secret

	mkdir -p 'API42'
	echo "uid=\"$uid\"" > $SECRETS_FILE
	echo "secret=\"$secret\"" >> $SECRETS_FILE
}

main() {
	echo "Installing submodules..."
	git submodule update --init --recursive

	if [ ! -f $SECRETS_FILE ] || [ "$1" = "--reset" ]; then
		getSecrets
	fi

	if [ ! -f $SECRETS_FILE ]; then
		echo "Not able to install without the secrets."
		return 1
	fi

	echo "Installing dependencies:"
	pip3 install requests
	pip3 install pytz

	echo "Done! Now you can molewakamole with:"
	echo "python3 $EXECUTABLE"
}


main $@