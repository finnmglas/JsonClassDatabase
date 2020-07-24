jcdb: src/jcdb.cpp lib/json.hpp
	@g++ -o src/jcdb src/jcdb.cpp lib/json.hpp

install: src/jcdb
	@sudo cp src/jcdb /usr/bin/jcdb 2> /dev/null && echo "Installed jcdb.\nYou can remove it using 'make remove'." || echo "Couldn't install jcdb.\nPlease try 'sudo make install'."

remove:
	@sudo rm /usr/bin/jcdb 2> /dev/null && echo "Uninstalled jcdb." || echo "Can't uninstall jcdb.\nPlease check if it even is installed."
