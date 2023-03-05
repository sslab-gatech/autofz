<?php

error_reporting(E_ALL & ~E_DEPRECATED);

function bar() {
    echo @$blah;
    echo $undef2;
}

function foo() {
    echo @$undef;
    error_reporting(E_ALL);
    echo $blah;
    return bar();
}

@foo();

var_dump(error_reporting());

echo "Done\n";
?>