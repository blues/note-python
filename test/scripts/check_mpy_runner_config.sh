function env_var_defined() {
    [ -v $1 ] || echo "Environment variable '$1' not set."
}

function check_all() {
    env_var_defined "MPY_SERIAL"
    env_var_defined "MPY_PRODUCT_UID"
    # these are defined in the workflow, but no harm sanity checking them
    env_var_defined "MICROPYTHON_BIN"
    env_var_defined "MICROPYTHON_BIN_URL"
    env_var_defined "VENV"
    env_var_defined "MPY_BOARD"
}

errors=$(check_all)
if [ -n "$errors" ]; then
    echo "$errors"   # quoted to preserve newlines
    echo "There are configuration errors. See the log above for details."
    exit 1
fi

exit 0