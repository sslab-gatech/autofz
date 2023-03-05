<?php
namespace foo;
use Error;

try {
    $a = array(unknown => unknown);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

try {
    echo unknown;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

try {
    echo \unknown;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>