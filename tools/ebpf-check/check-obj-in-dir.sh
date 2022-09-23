#!/usr/bin/env bash

usage() {
    printf 'Usage: %s <dirname>\n' "$0"
    printf '\tCheck all sections in .o ELF object files directly under <dirname>\n'
    exit $1
}

if [[ $# -lt 1 ]]; then
    usage 1
fi

SCRIPT_DIR="$(dirname "$0")"

for file in "$1"/*.o; do
    sections=""

    for i in $(llvm-objdump -h "${file}" | awk '/TEXT$/ { print $2 }'); do
        if [[ -z "${sections}" ]]; then
            sections="$i"
        else
            sections="${sections},$i"
        fi
    done

    echo "File ${file}: ${SCRIPT_DIR}/ebpf-check.py ${file} --sections ${sections}"
    "${SCRIPT_DIR}"/ebpf-check.py "${file}" --sections "${sections}"
done
