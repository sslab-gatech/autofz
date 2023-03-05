<?php

error_reporting(E_ALL & ~E_DEPRECATED);

function foo() {
    echo $undef;
    error_reporting(E_ALL);
}


foo(@$var);

var_dump(error_reporting());

echo "Done\n";
?>