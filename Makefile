jcdb: src/jcdb.cpp lib/json.hpp
	g++ -o src/jcdb src/jcdb.cpp lib/json.hpp

run: src/jcdb
	./src/jcdb
