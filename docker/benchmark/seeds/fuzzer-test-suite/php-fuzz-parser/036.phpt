<?php

try {
    $test[function(){}] = 1;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>