# Chandler Mahkorn 7/11/20 - 1:20 AM
import PokeOBJ

try:
	test = PokeOBJ.PokeOBJ(".gen6 shiny flygon mega")

except PokeOBJ.PokeError as err:
	print(err)

print(test)