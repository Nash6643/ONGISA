#!/usr/bin/env bash
# Completion script for forge-cli
_forge_completion() {
    eval "$(_FORGE_COMPLETE=bash_source forge)"
}
complete -F _forge_completion forge
