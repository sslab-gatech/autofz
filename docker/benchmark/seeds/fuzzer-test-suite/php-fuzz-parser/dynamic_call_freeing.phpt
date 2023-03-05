<?php

try {
    $bar = "bar";
    ("foo" . $bar)();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    $bar = ["bar"];
    (["foo"] + $bar)();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    (new stdClass)();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>