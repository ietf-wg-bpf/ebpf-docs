ISA_REF := instruction-set.rst
JSON_TABLE := instructions.json

all: $(JSON_TABLE)

$(ISA_REF):
	./get-from-gh.sh

$(JSON_TABLE): $(ISA_REF)
	./docs-to-ops.py > $@

clean:
	$(RM) -- $(ISA_REF) $(JSON_TABLE)

.PHONY: all clean
