<?php
function test() {

    try {
        $func = 'extract';
        $func(['a' => 'b']);
    } catch (\Error $e) {
        echo $e->getMessage() . "\n";
    }

    try {
        $func = 'compact';
        $func(['a']);
    } catch (\Error $e) {
        echo $e->getMessage() . "\n";
    }

    try {
        $func = 'get_defined_vars';
        $func();
    } catch (\Error $e) {
        echo $e->getMessage() . "\n";
    }

    try {
        $func = 'func_get_args';
        $func();
    } catch (\Error $e) {
        echo $e->getMessage() . "\n";
    }

    try {
        $func = 'func_get_arg';
        $func(1);
    } catch (\Error $e) {
        echo $e->getMessage() . "\n";
    }

    try {
        $func = 'func_num_args';
        $func();
    } catch (\Error $e) {
        echo $e->getMessage() . "\n";
    }
}
test();

?>