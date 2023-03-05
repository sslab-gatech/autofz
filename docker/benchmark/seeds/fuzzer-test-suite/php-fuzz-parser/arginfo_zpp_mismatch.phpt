<?php

foreach (get_defined_functions()["internal"] as $function) {
    try {
        @$function(null, null, null, null, null, null, null, null);
    } catch (ArgumentCountError|Error) {
    }
}

// var_dump() and debug_zval_dump() print all arguments
?>