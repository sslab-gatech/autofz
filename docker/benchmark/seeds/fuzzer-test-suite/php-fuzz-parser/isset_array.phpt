<?php

$array = [
    0 => true,
    "a" => true,
];

var_dump(isset($array[0]));

var_dump(isset($array["a"]));

var_dump(isset($array[false]));

var_dump(isset($array[0.6]));

var_dump(isset($array[true]));

var_dump(isset($array[null]));

var_dump(isset($array[STDIN]));

try {
    isset($array[[]]);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

try {
    isset($array[new stdClass()]);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}
?>