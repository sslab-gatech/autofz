<?php

$r = fopen(__FILE__, "r");

class test {
    function  __toString() {
        return "10";
    }
}

$o = new test;

$vars = array(
    "string",
    "8754456",
    "",
    "\0",
    9876545,
    0.10,
    array(),
    array(1,2,3),
    false,
    true,
    NULL,
    $r,
    $o
);

foreach ($vars as $var) {
    try {
        settype($var, "resource");
    } catch (ValueError $exception) {
        echo $exception->getMessage() . "\n";
    }
    var_dump($var);
}

echo "Done\n";
?>