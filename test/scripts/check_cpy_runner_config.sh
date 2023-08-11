
function diff_dir() {
    src=$1
    dest=$2  
    diff -r $src $dest
}

function env_var_defined() {
    [ -v $1 ] || echo "Environment variable '$1' not set."
}

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function check_all() {
    diff_dir $SCRIPT_DIR/usbmount /etc/usbmount
    env_var_defined "CPY_SERIAL"
    env_var_defined "CPY_FS_UF2"
    env_var_defined "CPY_FS_CIRCUITPY"
    env_var_defined "CPY_PRODUCT_UID"
    env_var_defined "CIRCUITPYTHON_UF2"
    env_var_defined "CIRCUITPYTHON_UF2_URL"
}

errors=$(check_all)
if [ -n "$errors" ]; then
    echo "$errors"   # quoted to preserve newlines
    echo "There are configuration errors. See the log above for details."
    exit 1
fi

exit 0