@echo off
setlocal
ECHO "This is meant to build a new poke.db in case there isn't one. Continue? [Y\N]"
SET /P INPUT=""
IF /I "%INPUT%" NEQ "Y" GOTO END (
	ECHO Making database...
	
	ECHO Populating Pokemon table
	py -3.8 populate_pokemon.py
	
	ECHO Populating Pokedex table
	py -3.8 populate_pokedex.py
)

:END
endlocal
pause