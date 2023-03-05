<?php

$str = "foo";
try {
    Test::{$str . "bar"}();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>