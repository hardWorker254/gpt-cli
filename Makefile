all:
	mkdir /usr/local/bin/gpt-clil
	cp ./main.py /usr/local/bin/gpt-clil/main.py
	cp ./promt.py /usr/local/bin/gpt-clil/promt.py
	g++ ./gpt-cli.cpp -o gpt-cli
	cp ./gpt-cli /usr/local/bin/gpt-cli